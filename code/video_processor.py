import re
import os
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip
from image_generator import process_text
from blur_video import apply_beautiful_blur
import json


def add_animated_image(
    background,
    foreground,
    current_time,
    start_time,
    duration,
    x_offset=None,
    y_offset=None,
):
    """
    Add an animated image on top of a background image with a pop-in entrance animation.

    Args:
        background (numpy.ndarray): Background image.
        foreground (numpy.ndarray): Foreground image with alpha channel.
        current_time (float): Current time in the video.
        start_time (float): Start time of the current image.
        duration (float): Duration of the current image.
        x_offset (int, optional): Initial X-axis offset for the foreground image.
        y_offset (int, optional): Initial Y-axis offset for the foreground image.
    """
    bg_h, bg_w = background.shape[:2]
    fg_h, fg_w = foreground.shape[:2]

    # Calculate progress (0 to 1) for the current image
    progress = (current_time - start_time) / duration

    # Easing function for more dramatic pop-in effect
    ease_progress = min(
        1, 1 - (1 - min(1, progress * 3)) ** 4
    )  # Quartic ease-out, even faster

    # Scale animation (only for entrance)
    scale_start, scale_end = 0.1, 1.2  # Start smaller, end slightly larger
    current_scale = scale_start + (scale_end - scale_start) * ease_progress
    new_fg_w, new_fg_h = int(fg_w * current_scale), int(fg_h * current_scale)

    # Position animation
    if x_offset is None:
        x_offset = (bg_w - new_fg_w) // 2
    if y_offset is None:
        y_offset = (bg_h - new_fg_h) // 2

    # Quick fade-in
    alpha_factor = min(1, progress * 3)  # Even faster fade-in

    # Resize the foreground image
    foreground_resized = cv2.resize(
        foreground, (new_fg_w, new_fg_h), interpolation=cv2.INTER_LINEAR
    )

    # Calculate the overlapping region
    x_start = max(0, x_offset)
    y_start = max(0, y_offset)
    x_end = min(bg_w, x_offset + new_fg_w)
    y_end = min(bg_h, y_offset + new_fg_h)

    # If no overlap, return the background as is
    if x_start >= x_end or y_start >= y_end:
        return background

    # Extract the overlapping regions
    fg_region = foreground_resized[
        y_start - y_offset : y_end - y_offset, x_start - x_offset : x_end - x_offset
    ]
    bg_region = background[y_start:y_end, x_start:x_end]

    # Apply alpha blending
    alpha = fg_region[:, :, 3] / 255.0 * alpha_factor
    alpha = np.repeat(alpha[:, :, np.newaxis], 3, axis=2)
    blended_region = bg_region * (1 - alpha) + fg_region[:, :, :3] * alpha

    # Place the blended region back onto the background
    background[y_start:y_end, x_start:x_end] = blended_region

    return background


def extract_number(filename):
    """
    Extract the number from a filename.

    Args:
        filename (str): Name of the file.

    Returns:
        int: Extracted number from the filename.
    """
    match = re.search(r"\d+", filename)
    return int(match.group()) if match else 0


def calculate_subtitle_durations(audio_duration, all_script_words_list):
    """
    Calculate the durations of subtitles based on the audio duration and script words.

    Args:
        audio_duration (float): Duration of the audio in seconds.
        all_script_words_list (list): List of words in the script.

    Returns:
        list: Durations of each subtitle in seconds.
    """
    total_chars = sum(len(word) for word in all_script_words_list)
    base_char_duration = audio_duration / total_chars

    durations = []
    for word in all_script_words_list:
        word_length = len(word)
        word_duration = word_length * base_char_duration

        # Adjust for punctuation (e.g., pauses after sentences)
        if word.endswith((".", "!", "?")):
            word_duration *= 1.2  # Add a pause effect

        durations.append(word_duration)

    print("Durations of words: \n", durations)
    return durations


def add_voice_to_video(video_path, audio_path, output_path):
    """
    Add voice to a video.

    Args:
        video_path (str): Path to the input video file.
        audio_path (str): Path to the input audio file.
        output_path (str): Path to the output video file.
    """
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    video = video.set_audio(audio)
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    video.close()
    audio.close()


import re
import os
import cv2
import numpy as np
import json
from moviepy.editor import VideoFileClip, AudioFileClip


def parse_eleven_labs_timing(timing_data):
    """
    Parse the Eleven Labs timing data and calculate word durations,
    handling spaces and punctuation correctly.

    Args:
        timing_data (dict): JSON data from Eleven Labs containing character timings.

    Returns:
        list: Tuples of (word, start_time, end_time) for each word.
    """
    characters = timing_data["characters"]
    start_times = timing_data["character_start_times_seconds"]
    end_times = timing_data["character_end_times_seconds"]

    word_timings = []
    current_word = ""
    word_start_time = start_times[0]
    last_char_end_time = start_times[0]

    for char, start, end in zip(characters, start_times, end_times):
        if char in [" ", "،", "."]:  # Add more punctuation as needed
            if current_word:
                word_timings.append((current_word, word_start_time, last_char_end_time))
                current_word = ""
            word_start_time = end
        else:
            current_word += char
            last_char_end_time = end

    # Add the last word if there is one
    if current_word:
        word_timings.append((current_word, word_start_time, end_times[-1]))

    return word_timings


def process_video_with_animated_images(
    video_path, image_paths, output_path, timing_data
):
    """
    Process a video by adding animated images on top of each frame.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    word_timings = parse_eleven_labs_timing(timing_data)
    total_duration = word_timings[-1][2]  # End time of the last word
    total_frames = int(total_duration * fps)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    foregrounds = [
        cv2.imread(image_path, cv2.IMREAD_UNCHANGED) for image_path in image_paths
    ]

    for fg in foregrounds:
        if fg is None or fg.shape[-1] != 4:
            print(f"Error: Image file does not have an alpha channel (RGBA)")
            return

    frame_count = 0
    current_image_index = 0

    while cap.isOpened() and frame_count < total_frames:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = frame_count / fps

        # Check if it's time to show or hide an image
        if current_image_index < len(word_timings):
            word, start_time, end_time = word_timings[current_image_index]

            if start_time <= current_time < end_time:
                # Show the image
                if current_image_index < len(image_paths):
                    foreground = foregrounds[current_image_index]
                    frame = add_animated_image(
                        frame,
                        foreground,
                        current_time,
                        start_time,
                        end_time - start_time,
                    )
            elif current_time >= end_time:
                # Move to the next word
                current_image_index += 1

        out.write(frame)
        frame_count += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"Processed {frame_count} frames. Last image index: {current_image_index}")
    print(f"Total images: {len(image_paths)}")
    print(f"Total duration processed: {frame_count / fps} seconds")
    print(f"Target duration: {total_duration} seconds")


# The rest of the code remains the same...


def process_final_video(
    video_path, images_folder, output_path, final_output_path, timing_data, is_blur
):
    """
    Process the final video by adding images and voice.

    Args:
        video_path (str): Path to the input video file.
        images_folder (str): Path to the folder containing the image files.
        output_path (str): Path to the intermediate output video file.
        final_output_path (str): Path to the final output video file.
        timing_data (dict): JSON data from Eleven Labs containing character timings.
        is_blur (bool): Whether to apply blur to the video.
    """
    image_paths = sorted(
        [
            os.path.join(images_folder, f).replace("\\", "/")
            for f in os.listdir(images_folder)
            if os.path.isfile(os.path.join(images_folder, f))
        ],
        key=extract_number,
    )

    if is_blur:
        output_path_new = "results/processed_video_blurred.mp4"
        apply_beautiful_blur(video_path, output_path_new, blur_strength=65)
        process_video_with_animated_images(
            output_path_new, image_paths, output_path, timing_data
        )
    else:
        process_video_with_animated_images(
            video_path, image_paths, output_path, timing_data
        )

    # Add voice to the processed video
    add_voice_to_video(output_path, "audios/audio1.mp3", final_output_path)

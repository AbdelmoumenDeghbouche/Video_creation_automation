import re
import os
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip
from image_generator import process_text


def add_transparent_image(
    background, foreground, x_offset=None, y_offset=None, scale_factor=1.0
):
    """
    Add a transparent image on top of a background image.

    Args:
        background (numpy.ndarray): Background image.
        foreground (numpy.ndarray): Foreground image with alpha channel.
        x_offset (int, optional): X-axis offset for the foreground image. Defaults to None.
        y_offset (int, optional): Y-axis offset for the foreground image. Defaults to None.
        scale_factor (float, optional): Scale factor for the foreground image. Defaults to 1.0.
    """
    # Get dimensions of background and foreground images
    bg_h, bg_w, bg_channels = background.shape
    fg_h, fg_w, fg_channels = foreground.shape

    # Check if the number of channels is correct
    assert (
        bg_channels == 3
    ), f"Background image should have exactly 3 channels (RGB). Found: {bg_channels}"
    assert (
        fg_channels == 4
    ), f"Foreground image should have exactly 4 channels (RGBA). Found: {fg_channels}"

    # Resize the foreground image based on the scale factor
    new_fg_w, new_fg_h = int(fg_w * scale_factor), int(fg_h * scale_factor)
    foreground_resized = cv2.resize(
        foreground, (new_fg_w, new_fg_h), interpolation=cv2.INTER_AREA
    )

    # Calculate the offsets if not provided
    x_offset = x_offset or (bg_w - new_fg_w) // 2
    y_offset = y_offset or (bg_h - new_fg_h) // 2

    # Calculate the overlapping region between the foreground and background images
    w = min(new_fg_w, bg_w, new_fg_w + x_offset, bg_w - x_offset)
    h = min(new_fg_h, bg_h, new_fg_h + y_offset, bg_h - y_offset)

    # If the overlapping region is invalid, return
    if w < 1 or h < 1:
        return

    # Calculate the regions of interest in the foreground and background images
    bg_x, bg_y = max(0, x_offset), max(0, y_offset)
    fg_x, fg_y = max(0, x_offset * -1), max(0, y_offset * -1)
    foreground_resized = foreground_resized[fg_y : fg_y + h, fg_x : fg_x + w]
    background_subsection = background[bg_y : bg_y + h, bg_x : bg_x + w]

    # Extract the foreground colors and alpha channel
    foreground_colors = foreground_resized[:, :, :3]
    alpha_channel = foreground_resized[:, :, 3] / 255.0
    alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))

    # Composite the foreground and background images
    composite = (
        background_subsection * (1 - alpha_mask) + foreground_colors * alpha_mask
    )
    background[bg_y : bg_y + h, bg_x : bg_x + w] = composite


def process_video_with_images(
    video_path, image_paths, output_path, target_duration, image_durations
):
    """
    Process a video by adding images on top of each frame.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    total_frames = int(target_duration * fps)
    total_images = len(image_paths)

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
    current_image_start_time = 0

    while cap.isOpened() and frame_count < total_frames:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = frame_count / fps

        # Check if it's time to switch to the next image
        if current_image_index < total_images:
            current_image_end_time = (
                current_image_start_time + image_durations[current_image_index]
            )

            if current_time >= current_image_end_time:
                current_image_index += 1
                current_image_start_time = current_image_end_time

            if current_image_index < total_images:
                foreground = foregrounds[current_image_index]
                progress = (current_time - current_image_start_time) / image_durations[
                    current_image_index
                ]
                scale_factor = min(1.0, 0.5 + progress * 0.5)

                try:
                    add_transparent_image(frame, foreground, scale_factor=scale_factor)
                except Exception as e:
                    print(
                        f"Error processing image {image_paths[current_image_index]}: {e}"
                    )
                    return

        out.write(frame)
        frame_count += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"Processed {frame_count} frames. Last image index: {current_image_index}")
    print(f"Total images: {total_images}")
    print(f"Total duration processed: {frame_count / fps} seconds")
    print(f"Target duration: {target_duration} seconds")


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
    durations = []

    for word in all_script_words_list:
        word_length = len(word)
        word_duration = (word_length / total_chars) * audio_duration
        durations.append(word_duration)
    print("durations of words : \n", durations)
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


def process_final_video(
    video_path, images_folder, output_path, final_output_path, arabic_text
):
    """
    Process the final video by adding images and voice.

    Args:
        video_path (str): Path to the input video file.
        images_folder (str): Path to the folder containing the image files.
        output_path (str): Path to the intermediate output video file.
        final_output_path (str): Path to the final output video file.
        arabic_text (str): Arabic text for generating subtitles.
    """
    # Get the paths of the image files in the folder
    image_paths = sorted(
        [
            os.path.join(images_folder, f).replace("\\", "/")
            for f in os.listdir(images_folder)
            if os.path.isfile(os.path.join(images_folder, f))
        ],
        key=extract_number,
    )

    # Load the audio clip and calculate subtitle durations
    audio_clip = AudioFileClip("audios/audio1.mp3")
    target_duration = audio_clip.duration
    all_script_words_list = process_text(arabic_text)
    image_durations = calculate_subtitle_durations(
        audio_clip.duration, all_script_words_list
    )

    # Process the video with images
    process_video_with_images(
        video_path, image_paths, output_path, target_duration, image_durations
    )

    # Add voice to the processed video
    add_voice_to_video(output_path, "audios/audio1.mp3", final_output_path)

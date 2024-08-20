import re
import os
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip
from generate_ai_voice import generate_ai_voice


def add_transparent_image(
    background, foreground, x_offset=None, y_offset=None, scale_factor=1.0
):
    bg_h, bg_w, bg_channels = background.shape
    fg_h, fg_w, fg_channels = foreground.shape

    assert (
        bg_channels == 3
    ), f"Background image should have exactly 3 channels (RGB). Found: {bg_channels}"
    assert (
        fg_channels == 4
    ), f"Foreground image should have exactly 4 channels (RGBA). Found: {fg_channels}"

    new_fg_w, new_fg_h = int(fg_w * scale_factor), int(fg_h * scale_factor)
    foreground_resized = cv2.resize(
        foreground, (new_fg_w, new_fg_h), interpolation=cv2.INTER_AREA
    )

    x_offset = x_offset or (bg_w - new_fg_w) // 2
    y_offset = y_offset or (bg_h - new_fg_h) // 2

    w = min(new_fg_w, bg_w, new_fg_w + x_offset, bg_w - x_offset)
    h = min(new_fg_h, bg_h, new_fg_h + y_offset, bg_h - y_offset)

    if w < 1 or h < 1:
        return

    bg_x, bg_y = max(0, x_offset), max(0, y_offset)
    fg_x, fg_y = max(0, x_offset * -1), max(0, y_offset * -1)
    foreground_resized = foreground_resized[fg_y : fg_y + h, fg_x : fg_x + w]
    background_subsection = background[bg_y : bg_y + h, bg_x : bg_x + w]

    foreground_colors = foreground_resized[:, :, :3]
    alpha_channel = foreground_resized[:, :, 3] / 255.0
    alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))

    composite = (
        background_subsection * (1 - alpha_mask) + foreground_colors * alpha_mask
    )
    background[bg_y : bg_y + h, bg_x : bg_x + w] = composite


def process_video_with_images(
    video_path, image_paths, output_path, target_duration, duration_per_image
):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    original_duration = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / fps

    total_frames = int(min(original_duration, target_duration) * fps)
    frames_per_image = int(fps * duration_per_image)

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
    total_images = len(foregrounds)
    total_image_frames = total_images * frames_per_image

    while cap.isOpened() and frame_count < total_frames:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count < total_image_frames:
            image_index = frame_count // frames_per_image
            foreground = foregrounds[image_index]

            image_frame_index = frame_count % frames_per_image
            scale_factor = (
                0.5 + (image_frame_index / (frames_per_image // 4)) * 0.5
                if image_frame_index < frames_per_image // 4
                else 1.0
            )

            try:
                add_transparent_image(frame, foreground, scale_factor=scale_factor)
            except Exception as e:
                print(f"Error processing image {image_paths[image_index]}: {e}")
                return

        out.write(frame)
        frame_count += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def extract_number(filename):
    match = re.search(r"\d+", filename)
    return int(match.group()) if match else 0

def calculate_subtitle_durations(audio_duration, all_script_words_list):
    total_chars = sum(len(word) for word in all_script_words_list)
    durations = []

    for word in all_script_words_list:
        word_length = len(word)
        word_duration = (word_length / total_chars) * audio_duration
        durations.append(word_duration)
    
    return durations


def add_voice_to_video(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    video = video.set_audio(audio)
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    video.close()
    audio.close()


def process_final_video(
    video_path, images_folder, output_path, final_output_path, arabic_text
):
    image_paths = sorted(
        [
            os.path.join(images_folder, f).replace("\\", "/")
            for f in os.listdir(images_folder)
            if os.path.isfile(os.path.join(images_folder, f))
        ],
        key=extract_number,
    )


    audio_clip = AudioFileClip("audios/audio1.mp3")
    target_duration = audio_clip.duration
    duration_per_image = (audio_clip.duration - 0.01) / len(image_paths)

    process_video_with_images(
        video_path, image_paths, output_path, target_duration, duration_per_image
    )
    add_voice_to_video(output_path, "audios/audio1.mp3", final_output_path)

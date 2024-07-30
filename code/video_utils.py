import re
from moviepy.editor import VideoFileClip, AudioFileClip
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
import cv2
import numpy as np
import os
from generate_ai_voice import generate_ai_voice


def add_transparent_image(background, foreground, x_offset=None, y_offset=None):
    bg_h, bg_w, bg_channels = background.shape
    fg_h, fg_w, fg_channels = foreground.shape

    assert (
        bg_channels == 3
    ), f"Background image should have exactly 3 channels (RGB). Found: {bg_channels}"
    assert (
        fg_channels == 4
    ), f"Foreground image should have exactly 4 channels (RGBA). Found: {fg_channels}"

    # Center by default
    if x_offset is None:
        x_offset = (bg_w - fg_w) // 2
    if y_offset is None:
        y_offset = (bg_h - fg_h) // 2

    w = min(fg_w, bg_w, fg_w + x_offset, bg_w - x_offset)
    h = min(fg_h, bg_h, fg_h + y_offset, bg_h - y_offset)

    if w < 1 or h < 1:
        return

    # Clip foreground and background images to the overlapping regions
    bg_x = max(0, x_offset)
    bg_y = max(0, y_offset)
    fg_x = max(0, x_offset * -1)
    fg_y = max(0, y_offset * -1)
    foreground = foreground[fg_y : fg_y + h, fg_x : fg_x + w]
    background_subsection = background[bg_y : bg_y + h, bg_x : bg_x + w]

    # Separate alpha and color channels from the foreground image
    foreground_colors = foreground[:, :, :3]
    alpha_channel = foreground[:, :, 3] / 255.0  # 0-255 => 0.0-1.0

    # Construct an alpha_mask that matches the image shape
    alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))

    # Combine the background with the overlay image weighted by alpha
    composite = (
        background_subsection * (1 - alpha_mask) + foreground_colors * alpha_mask
    )

    # Overwrite the section of the background image that has been updated
    background[bg_y : bg_y + h, bg_x : bg_x + w] = composite


def process_video_with_images(
    video_path, image_paths, output_path, target_duration, duration_per_image
):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    original_duration = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / fps

    # If the video duration is longer than the target duration, set the target duration
    if original_duration > target_duration:
        total_frames = int(target_duration * fps)
    else:
        total_frames = int(original_duration * fps)

    # Calculate the number of frames each image should be displayed
    frames_per_image = int(fps * duration_per_image)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    # Load all images with alpha channel (RGBA)
    foregrounds = []
    for image_path in image_paths:
        foreground = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if foreground is None:
            print(f"Error: Could not read image file {image_path}")
            return
        if foreground.shape[-1] != 4:
            print(
                f"Error: Image file {image_path} does not have an alpha channel (RGBA). Shape: {foreground.shape}"
            )
            return
        foregrounds.append(foreground)

    frame_count = 0
    total_images = len(foregrounds)
    total_image_frames = total_images * frames_per_image

    while cap.isOpened() and frame_count < total_frames:
        ret, frame = cap.read()
        if not ret:
            break

        # Determine which image to use based on the current frame count
        if frame_count < total_image_frames:
            image_index = frame_count // frames_per_image
            foreground = foregrounds[image_index]
            # Add transparent image to the frame
            try:
                add_transparent_image(frame, foreground)
            except Exception as e:
                print(f"Error processing image {image_paths[image_index]}: {e}")
                return

        # Write the frame to the output video
        out.write(frame)
        frame_count += 1

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()


def extract_number(filename):
    match = re.search(r"\d+", filename)
    return int(match.group()) if match else 0


def add_voice_to_video(video_path, arabic_text):

    video = VideoFileClip(video_path)
    audio = AudioFileClip("audios/audio1.mp3")
    video = video.set_audio(audio)
    video.write_videofile(
        "results/output_with_audio.mp4", codec="libx264", audio_codec="aac"
    )
    video.close()
    audio.close()


# Hard-coded file paths
video_path = "videos/Subway Surfers (2024) - Gameplay [4K 9x16] No Copyright.mp4"
images_dir = "images"

# Generate full paths for each image file and replace backslashes with forward slashes
image_files = [
    f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))
]
image_paths = [
    os.path.join(images_dir, file).replace("\\", "/") for file in image_files
]


# Sort the list using the custom key
sorted_image_paths = sorted(image_paths, key=extract_number)
print(sorted_image_paths)
num_images = len(sorted_image_paths)

output_path = "results/output.mp4"


video_clip = VideoFileClip(video_path)
arabic_text = "السلام عليكم و رحمة الله تعالى و بركاته 🧙‍♀️ and hello"
generate_ai_voice(arabic_text)
audio_clip = AudioFileClip("audios/audio1.mp3")
target_duration = audio_clip.duration
# Process the video with the selected images
duration_per_image = (
    audio_clip.duration - 0.01
) / num_images  # frame duration in seconds which is the audio duration divided by the number of words in the text script
process_video_with_images(
    video_path, sorted_image_paths, output_path, target_duration, duration_per_image
)

add_voice_to_video(output_path, arabic_text)

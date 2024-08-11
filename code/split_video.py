import os
import random
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.VideoFileClip import AudioFileClip
from take_center_vertical import center_crop_video


def cut_random_part(input_path, output_folder, cut_duration):
    # Load the video
    video = VideoFileClip(input_path)
    video_duration = video.duration

    # Ensure the cut duration is less than the video duration
    if cut_duration > video_duration:
        raise ValueError("Cut duration is longer than the video duration.")

    # Calculate the maximum possible starting point
    max_start_time = video_duration - cut_duration

    # Randomly select a starting point
    start_time = random.uniform(0, max_start_time)
    end_time = start_time + cut_duration

    # Extract the clip
    mini_clip = video.subclip(start_time, end_time)

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Save the clip
    output_path = os.path.join(output_folder, "random_cut_video.mp4")
    mini_clip.write_videofile(output_path, codec="libx264")

    # Close the clips
    mini_clip.close()
    video.close()


audio_clip = AudioFileClip("audios/audio1.mp3")
audio_duration = audio_clip.duration
input_video_path = "E:/AI/Video editing Automation project/videos/subbway.mp4"
output_folder = "videos/clips"
cut_duration = audio_duration + 3

# Cut a random part of the video
cut_random_part(input_video_path, output_folder, cut_duration)
center_crop_video(
    "videos/clips/random_cut_video.mp4", "videos/clips/center_cropped_random_clip.mp4"
)
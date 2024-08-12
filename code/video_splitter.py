import os
import random
from moviepy.video.io.VideoFileClip import VideoFileClip, AudioFileClip
from take_center_vertical import center_crop_video

def cut_random_part(input_path, output_folder, cut_duration):
    with VideoFileClip(input_path) as video:
        video_duration = video.duration
        
        if cut_duration > video_duration:
            raise ValueError("Cut duration is longer than the video duration.")
        
        max_start_time = video_duration - cut_duration
        start_time = random.uniform(0, max_start_time)
        end_time = start_time + cut_duration
        
        mini_clip = video.subclip(start_time, end_time)
        
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, "random_cut_video.mp4")
        mini_clip.write_videofile(output_path, codec="libx264")

def process_video(input_video_path, output_folder):
    audio_clip = AudioFileClip("audios/audio1.mp3")
    audio_duration = audio_clip.duration
    cut_duration = audio_duration + 3

    cut_random_part(input_video_path, output_folder, cut_duration)
    center_crop_video(os.path.join(output_folder, "random_cut_video.mp4"), 
                      os.path.join(output_folder, "ready_clip.mp4"))
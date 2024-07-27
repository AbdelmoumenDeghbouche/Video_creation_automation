"""
This script splits a video into 26 equal parts and saves them in a folder.
 this is useful when you want to split a video into smaller parts for further processing.
 The number 26 will be changed to the number of parts you want to split the video into.
"""
from moviepy.video.io.VideoFileClip import VideoFileClip

def split_video(input_path, output_folder):
    
    video = VideoFileClip(input_path)
    duration = video.duration
    mini_duration = duration / 26
    
    for i in range(26):
        start_time = i * mini_duration
        end_time = (i + 1) * mini_duration
        mini_clip = video.subclip(start_time, end_time)
        mini_clip.write_videofile(f"{output_folder}/mini_video_{i+1}.mp4", codec="libx264")
        mini_clip.close()

    video.close()

input_video_path = "E:/AI/Video editing Automation project/videos/subbway.mp4"
output_folder = "videos/clips"
split_video(input_video_path, output_folder)

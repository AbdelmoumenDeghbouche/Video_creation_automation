from moviepy.video.io.VideoFileClip import VideoFileClip
import os


def cut_video(input_path, output_path, start_cut, end_cut):
    # Load the video file
    if os.path.exists(output_path):
        os.remove(output_path)  # Delete the existing file

    video = VideoFileClip(input_path)

    # Calculate the new start and end times
    start_time = start_cut
    end_time = video.duration - end_cut

    # Cut the video
    trimmed_video = video.subclip(start_time, end_time)

    # Write the result to the output file
    trimmed_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # Close the video files
    video.close()
    trimmed_video.close()

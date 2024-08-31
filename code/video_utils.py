from moviepy.video.io.VideoFileClip import VideoFileClip
import os
from search_yt import get_first_video_under_x_seconds
from download_yt import download_video
from download_mp3 import download_audio
from translator_ar_en import translate_arabic_to_english
from overlay_video_processor import overlay_video
from add_sound_to_video import add_sound_to_video
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips
import cv2
import ffmpeg

overlay_and_sound_duration = 4


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


def add_green_screen(arabic_green_screen_text_search, start_time):
    translated_text = translate_arabic_to_english(arabic_green_screen_text_search)
    search_query_video = f"{translated_text} green screen"
    video_link = get_first_video_under_x_seconds(search_query_video, 11)
    download_video(video_link, "videos/assets/Green_screnns", "green_screen_video.mp4")
    search_query_audio = f"{translated_text} sound effect"
    audio_link = get_first_video_under_x_seconds(search_query_audio, 7)
    download_audio(audio_link, "videos/assets/audios", "vfxs")
    overlay_video(
        background_video_path="results/output_with_audio.mp4",
        overlay_video_path="videos/assets/Green_screnns/green_screen_video.mp4",
        output_path="results/output_with_green_screen.mp4",
        scale_factor=1.0,
        overlay_start_time=start_time,
        bottom_margin=0,
        green_screen_color=[1, 214, 0],
        duration=overlay_and_sound_duration,
    )

    add_sound_to_video(
        video_path="results/output_with_green_screen.mp4",
        sound_path="videos/assets/audios/vfxs.mp3",
        output_path="results/final_output_video.mp4",
        start_time=start_time,  # Start the sound at 5 seconds into the video
        duration=overlay_and_sound_duration,  # Play the sound for 10 seconds (optional)
        volume_level=30,  # Set the volume to 30% (optional)
    )


def concatenate_videos_in_random_order(video_files, output_file):
    # Load all video clips
    video_clips = [VideoFileClip(f) for f in video_files]

    # Get the resolution and frame rate of the first video
    target_resolution = video_clips[0].size
    target_fps = video_clips[0].fps

    # Resize and set the frame rate of all video clips to match the first video
    video_clips = [
        clip.resize(newsize=target_resolution).set_fps(target_fps)
        for clip in video_clips
    ]

    # Shuffle the list of video clips to randomize the order
    random.shuffle(video_clips)

    # Concatenate the video clips
    final_clip = concatenate_videoclips(video_clips)

    # Write the output video file
    final_clip.write_videofile(output_file)

    # Close the clips to release resources
    for clip in video_clips:
        clip.close()


def speed_up_video_60_fps(input_path, output_path, target_fps=60):

    # Open the input video
    cap = cv2.VideoCapture(input_path)

    # Get video properties
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the number of frames to interpolate
    multiplier = target_fps / original_fps

    # Set up the output video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, target_fps, (width, height))

    # Read the first frame
    ret, prev_frame = cap.read()
    if not ret:
        print("Failed to read the video")
        return

    frame_count = 0
    while True:
        # Read the next frame
        ret, next_frame = cap.read()
        if not ret:
            break

        # Write the previous frame
        out.write(prev_frame)

        # Interpolate frames
        for i in range(1, int(multiplier)):
            alpha = i / multiplier
            interpolated_frame = cv2.addWeighted(
                prev_frame, 1 - alpha, next_frame, alpha, 0
            )
            out.write(interpolated_frame)

        prev_frame = next_frame
        frame_count += 1
        print(f"Processed frame {frame_count}/{total_frames}")

    # Write the last frame
    out.write(next_frame)

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print("Video interpolation completed.")


def change_video_metadata(input_file, output_file, metadata):
    # Open the input file
    stream = ffmpeg.input(input_file)

    # Apply metadata changes
    stream = ffmpeg.output(stream, output_file, **metadata)

    # Run the ffmpeg command
    ffmpeg.run(stream)
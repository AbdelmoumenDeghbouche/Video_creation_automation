from overlay_video_processor import overlay_video
from moviepy.editor import AudioFileClip
from video_processor import calculate_subtitle_durations
from image_generator import process_text


def calculate_overlay_start_time(audio_duration, arabic_text):
    # Example inputs
    all_script_words_list = process_text(arabic_text)

    # Calculate the duration for each word
    all_script_words_list_lower = [word.lower() for word in all_script_words_list]
    durations = calculate_subtitle_durations(
        audio_duration, all_script_words_list_lower
    )
    print(all_script_words_list_lower)
    # Find the index of the word "zoba"
    zoba_index = all_script_words_list_lower.index("zoba")
    print(zoba_index)
    # Calculate the start time for "zoba"
    zoba_start_time = sum(durations[:zoba_index])
    print(zoba_start_time)
    print("durations \n ", durations)
    print("total duration \n ", sum(durations))
    return zoba_start_time


# Function to add call to action video overlay
def add_c2a_overlay(arabic_text):
    background_video = "results/output_with_audio.mp4"
    overlay_video_path = "videos/assets/Green_screnns/zoba overlay-vmake.mp4"
    output_video = "results/output_overlay.mp4"

    # Preprocess text to get word list
    audio_voice_over = AudioFileClip("audios/audio1.mp3")
    audio_duration = audio_voice_over.duration
    overlay_start_time_caluculated = calculate_overlay_start_time(
        audio_duration, arabic_text
    )
    # Calculate the start time for the overlay based on audio duration and text length
    print(overlay_start_time_caluculated)
    # Add the overlay with specified parameters
    overlay_video(
        background_video_path=background_video,
        overlay_video_path=overlay_video_path,
        output_path=output_video,
        scale_factor=1.5,
        overlay_start_time=overlay_start_time_caluculated,
        bottom_margin=0,
        green_screen_color=[1, 214, 0],  # Specify the green color to remove
    )


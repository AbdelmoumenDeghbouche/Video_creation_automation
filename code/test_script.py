from search_yt import get_first_video_under_x_seconds
from download_yt import download_video
from download_mp3 import download_audio
from translator_ar_en import translate_arabic_to_english
from overlay_video_processor import overlay_video
from add_sound_to_video import add_sound_to_video

overlay_and_sound_duration = 4


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

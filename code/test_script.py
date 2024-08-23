from search_yt import get_first_video_under_x_seconds
from download_yt import download_video
from download_mp3 import download_audio
from translator_ar_en import translate_arabic_to_english
from overlay_video_processor import overlay_video


def add_green_screen(arabic_text, start_time):
    translated_text = translate_arabic_to_english(arabic_text)
    search_query_video = f"{translated_text} green screen"
    video_link = get_first_video_under_x_seconds(search_query_video, 11)
    download_video(video_link,"videos/assets/Green_screnns","green_screen_video.mp4")
    search_query_audio = f"{translated_text} sound effect"
    audio_link = get_first_video_under_x_seconds(search_query_audio, 6)
    download_audio(audio_link,"videos/assets/audios")
    overlay_video(
        "downloaded_videos/video.mp4",
        "downloaded_audios/audio.mp3",
        "results/output_overlay.mp4",
        0.5,
        start_time,
        50,
    )

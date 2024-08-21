from overlay_video_processor import overlay_video
from image_generator import preprocess_text, zoba_image_index
from moviepy.editor import AudioFileClip


# Function to add call to action video overlay
def add_c2a_overlay():
    background_video = "results/output_with_audio.mp4"
    overlay_video_path = "videos/assets/Green_screnns/zoba overlay-vmake.mp4"
    output_video = "results/output_overlay.mp4"

    # Preprocess text to get word list
    audio_voice_over = AudioFileClip("audios/audio1.mp3")

    # Calculate the start time for the overlay based on audio duration and text length

    # Add the overlay with specified parameters
    overlay_video(
        background_video_path=background_video,
        overlay_video_path=overlay_video_path,
        output_path=output_video,
        scale_factor=1.5,
        overlay_start_time=15,
        bottom_margin=0,
        green_screen_color=[1, 214, 0],  # Specify the green color to remove
    )


# Example usage:
add_c2a_overlay()

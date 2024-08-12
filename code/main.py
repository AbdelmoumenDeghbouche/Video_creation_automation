import os
from video_splitter import process_video
from image_generator import generate_images_from_text
from video_processor import process_final_video
from generate_ai_voice import generate_ai_voice

arabic_text = "السلام عليكم و رحمة الله تعالى و بركته 🧙‍♀️ and hello"


def main():
    # Step 1: Generate ai audio , Split and crop video
   

    # Step 2: Generate images from text
    images_folder = "images"
    generate_images_from_text(arabic_text, images_folder)

    # Step 3: Process final video with images and audio
    video_path = "videos/clips/ready_clip.mp4"
    output_path = "results/output.mp4"
    final_output_path = "results/output_with_audio.mp4"
    process_final_video(
        video_path, images_folder, output_path, final_output_path, arabic_text
    )


if __name__ == "__main__":
    main()

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel
from video_splitter import process_video
from image_generator import generate_images_from_text
from video_processor import process_final_video
from generate_ai_voice import generate_ai_voice
from utils import is_url
from search_yt import get_first_video_under_x_seconds
from download_yt import download_video
from video_utils import cut_video
from concatinate_short_videos import concatenate_random_order_videos
from c2a_overlay import add_c2a_overlay
from typing import Optional
from utils import clear_files_folder
from video_utils import speed_up_video_60_fps
from change_meta_data_dynamic import change_video_metadata_dynamic
import os
import json
import logging
import traceback

arabic_text = None
# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()


class TextRequest(BaseModel):
    arabic_text: str
    background_video: str
    blur: bool
    eleven_labs_api_key: str
    ngrok_auth_token: str


@app.post("/generate-video/")
async def generate_video(
    request: TextRequest = Depends(),
    arabic_font_file: UploadFile = File(None),
    font_size: Optional[int] = Form(None),
):
    arabic_text = request.arabic_text
    background_video_folder = request.background_video
    is_blur = request.blur
    eleven_labs_api_key = request.eleven_labs_api_key
    ngrok_auth_token = request.ngrok_auth_token

    try:
        logging.info(
            f"Received request with text: {arabic_text} and background folder: {background_video_folder}"
        )

        clear_files_folder("results")
        if is_url(background_video_folder):
            # Download the video from the URL
            video_link = background_video_folder
            download_video(video_link, "videos/other", "background_downloaded_video")
            speed_up_video_60_fps(
                "videos/other/background_downloaded_video.mp4",
                "videos/other/background_downloaded_video_interpolated.mp4",
                60,
            )
            selected_video_path = (
                "videos/other/background_downloaded_video_interpolated.mp4"
            )
            cut_video(
                selected_video_path,
                "videos/other/background_downloaded_video_cutten.mp4",
                15,
                15,
            )
            selected_video_path = "videos/other/background_downloaded_video_cutten.mp4"
            background_video_folder = "other"
        else:
            # Choose a random video
            selected_video_path = concatenate_random_order_videos(
                background_video_folder
            )
            logging.info(f"Selected video: {selected_video_path}")

        # Step 1: Generate AI audio, Split, and crop the selected random video
        logging.info("Starting video processing...")
        # Uncomment if needed
        # generate_ai_voice(arabic_text, eleven_labs_api_key)
        process_video(selected_video_path, f"videos/{background_video_folder}/clips")

        # Step 2: Generate images from text
        images_folder = "images"
        logging.info(
            f"Generating images for text: {arabic_text} in folder: {images_folder}"
        )
        if not arabic_font_file:
            if not font_size:
                generate_images_from_text(arabic_text, images_folder)
            else:
                generate_images_from_text(
                    arabic_text, images_folder, font_size=font_size
                )
        else:
            if not font_size:
                generate_images_from_text(
                    arabic_text, images_folder, arabic_font_file=arabic_font_file
                )
            else:
                generate_images_from_text(
                    arabic_text,
                    images_folder,
                    arabic_font_file=arabic_font_file,
                    font_size=font_size,
                )

        # Step 4: Process final video with images and audio
        video_path = f"videos/{background_video_folder}/clips/ready_clip.mp4"
        output_path = "results/output.mp4"
        final_output_path = "results/output_with_audio.mp4"
        logging.info("Starting final video processing...")
        with open("zz.json", encoding="utf-8") as f:
            timing_data = json.load(f)

        process_final_video(
            video_path,
            images_folder,
            output_path,
            final_output_path,
            timing_data,
            is_blur,
        )
        # adding c2a overlay
        add_c2a_overlay(arabic_text=arabic_text)
        # Check if the file exists
        if not os.path.exists(final_output_path):
            logging.error("Final video file does not exist after processing")
            raise HTTPException(status_code=500, detail="Video creation failed")
        final_output_path = "results/output_overlay.mp4"
        logging.info(f"Video successfully created: {final_output_path}")
        change_video_metadata_dynamic(
            final_output_path, "results/output_overlay_metadata.mp4"
        )
        final_output_path = "results/output_overlay_metadata.mp4"
        # Return the video file as a response
        return FileResponse(
            final_output_path,
            media_type="video/mp4",
            filename="output_overlay_metadata.mp4",
        )

    except Exception as e:
        # Log the exception and return detailed traceback information
        logging.error(f"Error occurred: {str(e)}")
        logging.error(traceback.format_exc())  # Log full traceback for debugging
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

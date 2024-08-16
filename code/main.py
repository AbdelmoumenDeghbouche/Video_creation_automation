from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from video_splitter import process_video
from image_generator import generate_images_from_text
from video_processor import process_final_video
from generate_ai_voice import generate_ai_voice
import os
import random

app = FastAPI()

class TextRequest(BaseModel):
    arabic_text: str
    background_video: str

@app.post("/generate-video/")
async def generate_video(request: TextRequest):
    arabic_text = request.arabic_text
    background_video_folder = request.background_video
    try:
        # Get the path to the background video folder
        video_folder_path = f"videos/{background_video_folder}/videos"
        
        # List all video files in the folder
        video_files = [f for f in os.listdir(video_folder_path) if f.endswith(('.mp4', '.avi', '.mkv'))]
        
        if not video_files:
            raise HTTPException(status_code=404, detail="No videos found in the specified folder")
        
        # Choose a random video
        selected_video = random.choice(video_files)
        selected_video_path = os.path.join(video_folder_path, selected_video)

        # Step 1: Generate AI audio, Split, and crop the selected random video
        generate_ai_voice(arabic_text)
        process_video(selected_video_path, f"videos/{background_video_folder}/clips")
        
        # Step 2: Generate images from text
        images_folder = "images"
        generate_images_from_text(arabic_text, images_folder)

        # Step 3: Process final video with images and audio
        video_path = f"videos/{background_video_folder}/clips/ready_clip.mp4"
        output_path = "results/output.mp4"
        final_output_path = "results/output_with_audio.mp4"
        process_final_video(
            video_path, images_folder, output_path, final_output_path, arabic_text
        )

        # Check if the file exists
        if not os.path.exists(final_output_path):
            raise HTTPException(status_code=500, detail="Video creation failed")

        # Return the video file as a response
        return FileResponse(
            final_output_path, media_type="video/mp4", filename="output_with_audio.mp4"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
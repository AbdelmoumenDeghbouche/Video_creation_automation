import yt_dlp
import os


def download_audio(url, output_path, new_filename="new_sound"):
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": os.path.join(output_path, new_filename),
    }

    if new_filename:
        new_filename_with_ext = os.path.join(output_path, f"{new_filename}.mp4")
        if os.path.exists(new_filename_with_ext):
            os.remove(new_filename_with_ext)  # Delete the existing file

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Example usage

import yt_dlp
import os


def download_video(video_url, output_path, new_filename="new_video"):
    # Set options for 720p download
    ydl_opts = {
        "format": "bestvideo[height<=720]+bestaudio/best[height<=720]",  # Download best 720p video with audio
        "merge_output_format": "mp4",  # Merge video and audio in mp4 format
        "outtmpl": os.path.join(output_path, new_filename),  # Set output path
    }
    # If a new filename is provided, rename the file

    new_filename_with_ext = os.path.join(output_path, f"{new_filename}.mp4")
    if os.path.exists(new_filename_with_ext):
        os.remove(new_filename_with_ext)  # Delete the existing file

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Example usage
# download_video('https://www.youtube.com/watch?v=example', '/path/to/save/video', 'new_video_name')

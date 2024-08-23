import yt_dlp
import os

def download_video(video_url, output_path, new_filename=None):
    # Set options for 720p download
    ydl_opts = {
        'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',  # Download best 720p video with audio
        'merge_output_format': 'mp4',  # Merge video and audio in mp4 format
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s')  # Set output path
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        # Get the original downloaded file path
        info = ydl.extract_info(video_url, download=False)
        original_filename = os.path.join(output_path, f"{info['title']}.mp4")
        
        # If a new filename is provided, rename the file
        if new_filename:
            new_filename_with_ext = os.path.join(output_path, f"{new_filename}.mp4")
            if os.path.exists(new_filename_with_ext):
                os.remove(new_filename_with_ext)  # Delete the existing file
            os.rename(original_filename, new_filename_with_ext)
            print(f"Download completed and saved as {new_filename_with_ext}!")
        else:
            print(f"Download completed and saved as {original_filename}!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
# download_video('https://www.youtube.com/watch?v=example', '/path/to/save/video', 'new_video_name')

# Example usage
download_video('https://www.youtube.com/watch?v=Cg1CStyHiz0', 'videos/assets/Green_screnns/',"new_video_name")

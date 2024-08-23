import yt_dlp
import os

def download_audio(url, output_path, new_filename=None):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Get the original downloaded file path
        info = ydl.extract_info(url, download=False)
        original_filename = os.path.join(output_path, f"{info['title']}.mp3")
        
        # If a new filename is provided, rename the file
        if new_filename:
            new_filename_with_ext = os.path.join(output_path, f"{new_filename}.mp3")
            if os.path.exists(new_filename_with_ext):
                os.remove(new_filename_with_ext)  # Delete the existing file
            os.rename(original_filename, new_filename_with_ext)
            print(f"Download completed and saved as {new_filename_with_ext}!")
        else:
            print(f"Download completed and saved as {original_filename}!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
# download_audio('https://www.youtube.com/watch?v=example', '/path/to/save/audio', 'new_audio_name')

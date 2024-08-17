import yt_dlp

def download_video(video_url):
    # Set options for 720p download
    ydl_opts = {
        'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',  # Download best 720p video with audio
        'merge_output_format': 'mp4',  # Merge video and audio in mp4 format
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print("Download completed at 720p!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

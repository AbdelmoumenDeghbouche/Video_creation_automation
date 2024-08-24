from utils import is_url
from search_yt import get_first_video_under_x_seconds
from download_yt import download_video
from video_utils import cut_video

background_video_folder = "https://www.youtube.com/watch?v=cFrvVUn_mGI"
if is_url(background_video_folder):
    # Download the video from the URL
    video_link = background_video_folder
    download_video(video_link, "videos/other", "background_downloaded_video")
    selected_video_path = "videos/other/background_downloaded_video.mp4"
    cut_video(
        selected_video_path,
        "videos/other/background_downloaded_video_cutten.mp4",
        15,
        15,
    )

from video_utils import concatenate_videos_in_random_order
import json
from download_yt import download_video
from video_utils import speed_up_video_60_fps


def concatenate_random_order_videos(background_video_type):
    video_files = []
    output_video = f"videos/{background_video_type}/videos/output_random_orders.mp4"
    # Assuming the JSON data is stored in a file called 'data.json'
    with open("videos.json") as json_file:
        data = json.load(json_file)

    # Accessing the URL and type
    for i in range(len(data[background_video_type]["videos"])):
        url = data[background_video_type]["videos"][i]["url"]
        video_type = data[background_video_type]["videos"][i]["type"]
        if video_type == "short":
            download_video(
                url, f"videos/{background_video_type}/videos", f"video{i}.mp4"
            )
            video_files.append(f"videos/{background_video_type}/videos/video{i}.mp4")

    concatenate_videos_in_random_order(video_files, output_video)
    final_output_video = (
        f"videos/{background_video_type}/videos/output_random_orders_interpolated.mp4"
    )
    speed_up_video_60_fps(output_video, final_output_video, 60)
    return final_output_video

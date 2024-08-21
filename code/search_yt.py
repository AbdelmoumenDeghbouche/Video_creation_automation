from youtubesearchpython import VideosSearch
from download_yt import download_video
from download_mp3 import download_audio

def get_first_video_under_59_seconds(search_query):
    try:
        # Create a VideosSearch object with the search query, setting a higher limit to search multiple videos
        search = VideosSearch(search_query, limit=10)

        # Get the results
        results = search.result()

        # Check if we have any results
        if results and "result" in results and results["result"]:
            # Loop through the results to find the first video under 59 seconds
            for video in results["result"]:
                duration = video.get("duration")
                if duration:
                    # Convert duration to seconds
                    minutes, seconds = map(int, duration.split(":"))
                    total_seconds = minutes * 60 + seconds
                    if total_seconds < 11:
                        video_link = f"https://www.youtube.com/watch?v={video['id']}"
                        return video_link
            return "No video found under 59 seconds."
        else:
            return "No results found."

    except Exception as e:
        return f"An error occurred: {str(e)}"


# Use the function
search_query = "time green screen"
video_link = get_first_video_under_59_seconds(search_query)
print(f"First video under 59 seconds for '{search_query}': {video_link}")
download_video(video_link)

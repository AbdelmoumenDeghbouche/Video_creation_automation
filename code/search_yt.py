from youtubesearchpython import VideosSearch


def get_first_video_under_x_seconds(search_query, video_length):
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
                    if total_seconds < video_length:
                        video_link = f"https://www.youtube.com/watch?v={video['id']}"
                        return video_link
            return "No video found under 59 seconds."
        else:
            return "No results found."

    except Exception as e:
        return f"An error occurred: {str(e)}"


from youtubesearchpython import VideosSearch


def get_first_video_under_x_seconds(search_query, video_max_length, video_min_length=0):
    try:
        # Create a VideosSearch object with the search query, setting a higher limit to search multiple videos
        search = VideosSearch(search_query, limit=20)

        # Get the results
        results = search.result()

        # Check if we have any results
        if results and "result" in results and results["result"]:
            # Loop through the results to find the first video under the specified length
            for video in results["result"]:
                duration = video.get("duration")
                if duration:
                    # Split the duration into parts
                    duration_parts = duration.split(":")
                    # Convert duration to seconds based on the number of parts
                    if len(duration_parts) == 3:  # Hours:Minutes:Seconds
                        hours, minutes, seconds = map(int, duration_parts)
                        total_seconds = hours * 3600 + minutes * 60 + seconds
                    elif len(duration_parts) == 2:  # Minutes:Seconds
                        minutes, seconds = map(int, duration_parts)
                        total_seconds = minutes * 60 + seconds
                    elif len(duration_parts) == 1:  # Seconds only
                        total_seconds = int(duration_parts[0])
                    else:
                        total_seconds = 0

                    if (
                        total_seconds < video_max_length
                        and total_seconds > video_min_length
                    ):
                        video_link = f"https://www.youtube.com/watch?v={video['id']}"
                        return video_link
            return f"No video found under {video_max_length} seconds."
        else:
            return "No results found."

    except Exception as e:
        return f"An error occurred: {str(e)}"

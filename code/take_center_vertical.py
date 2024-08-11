from moviepy.editor import VideoFileClip


def center_crop_video(input_path, output_path, target_width=1080, target_height=1920):
    """
    Center crops a video to the specified 9:16 aspect ratio (1080x1920) if needed.

    Parameters:
    - input_path: Path to the input video file.
    - output_path: Path where the output video will be saved.
    - target_width: Target width for the output video (default is 1080).
    - target_height: Target height for the output video (default is 1920).
    """
    # Load the video file
    video = VideoFileClip(input_path)

    # Get the original dimensions of the video
    original_width, original_height = video.size

    # Check if the video is already in the target resolution and aspect ratio
    if original_width == target_width and original_height == target_height:
        print(
            "The video is already in the desired 9:16 aspect ratio with 1080x1920 resolution."
        )
        final_video = video  # No need to crop or resize
    else:
        # Calculate the aspect ratio
        aspect_ratio = target_height / target_width
        crop_height = int(original_width * aspect_ratio)

        # Make sure the crop height doesn't exceed the original height
        if crop_height > original_height:
            crop_height = original_height
            crop_width = int(original_height / aspect_ratio)
        else:
            crop_width = original_width

        # Calculate the position to crop (center crop)
        x_center = original_width // 2
        y_center = original_height // 2

        x1 = x_center - (crop_width // 2)
        y1 = y_center - (crop_height // 2)
        x2 = x_center + (crop_width // 2)
        y2 = y_center + (crop_height // 2)

        # Crop and resize the video to 1080x1920
        final_video = video.crop(x1=x1, y1=y1, x2=x2, y2=y2).resize(
            (target_width, target_height)
        )

    # Save the output video
    final_video.write_videofile(output_path, codec="libx264")


from moviepy.editor import VideoFileClip, CompositeVideoClip
from moviepy.video.fx.all import mask_color


def overlay_video(
    background_video_path,
    overlay_video_path,
    output_path,
    scale_factor=1.0,
    overlay_start_time=0,
    bottom_margin=0,
    green_screen_color=[0, 255, 0],  # Default green color
):
    # Load the background video
    background_clip = VideoFileClip(background_video_path)

    # Load the overlay video
    overlay_clip = VideoFileClip(overlay_video_path)

    # Resize the overlay clip if a scale factor is provided
    if scale_factor != 1.0:
        overlay_clip = overlay_clip.resize(scale_factor)

    # Remove the green screen (chroma keying) from the overlay
    overlay_clip = overlay_clip.fx(mask_color, color=green_screen_color, thr=100, s=5)

    # Calculate the position (center horizontally, bottom with margin vertically)
    video_height = background_clip.h
    overlay_height = overlay_clip.h
    bottom_y_position = video_height - overlay_height - bottom_margin

    # Position the overlay video at the center bottom with a margin
    overlay_clip = overlay_clip.set_position(("center", bottom_y_position))

    # Set when the overlay video should start
    overlay_clip = overlay_clip.set_start(overlay_start_time)

    # Create the composite video
    composite_clip = CompositeVideoClip([background_clip, overlay_clip])

    # Write the result to a file
    composite_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")


# Example usage:
background_video = (
    "videos/Subway/videos/SPIDERMAN INTO SPIDERVERSE 4K LIVE WALLPAPER..mp4"
)
overlay_video_path = (
    "videos/assets/no_bg_assets/Green Screen/Caught-in-4K-(Green-Screen).mp4"
)

output_video = "results/output_overlay.mp4"

# Set overlay_start_time to 15 seconds, position to center bottom with margin, and resize to 50%
overlay_video(
    background_video,
    overlay_video_path,
    output_video,
    scale_factor=0.3,  # Resize to 50% of its original size
    overlay_start_time=15,  # Overlay video starts at second 15
    bottom_margin=50,  # 50 pixels margin from the bottom
    green_screen_color=[0, 255, 0],  # Specify the green color to remove
)

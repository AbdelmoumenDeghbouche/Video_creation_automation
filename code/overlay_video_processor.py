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
    duration=None,  # Duration for which the overlay stays
    position="center",  # Position of the overlay
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

    # Apply the duration to the overlay clip if provided
    if duration:
        overlay_clip = overlay_clip.set_duration(duration)

    # Calculate the position (center horizontally, bottom with margin vertically)
    video_height = background_clip.h
    overlay_height = overlay_clip.h
    if position == "bottom":
        position = video_height - overlay_height - bottom_margin

    # Position the overlay video at the center bottom with a margin
    overlay_clip = overlay_clip.set_position(("center", position))

    # Set when the overlay video should start
    overlay_clip = overlay_clip.set_start(overlay_start_time)

    # Create the composite video
    composite_clip = CompositeVideoClip([background_clip, overlay_clip])

    # Write the result to a file
    composite_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

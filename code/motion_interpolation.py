import subprocess

def encode_video_high_quality(input_path, output_path):
    # Construct the FFmpeg command with veryslow preset for maximum quality
    command = [
        'ffmpeg',
        '-i', input_path,
        '-c:v', 'libx264',          # Use H.264 codec
        '-preset', 'veryslow',      # Maximum quality preset
        '-crf', '18',               # Constant Rate Factor for high quality
        '-c:a', 'copy',             # Copy audio stream without re-encoding
        output_path
    ]

    # Run the command
    subprocess.run(command, check=True)

# Example usage
input_video = "input_video.mp4"
output_video = "output_video_high_quality.mp4"
encode_video_high_quality(input_video, output_video)

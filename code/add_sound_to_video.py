from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

def add_sound_to_video(video_path, sound_path, output_path, start_time=0, duration=None, volume_level=100):
    try:
        # Load the video clip
        video = VideoFileClip(video_path)

        # Load the audio clip
        audio = AudioFileClip(sound_path)
        
        # If duration is not specified, use the full duration of the audio clip
        if duration is None:
            duration = audio.duration
        
        # Cut the audio to the specified duration
        audio = audio.subclip(0, duration)
        
        # Adjust the audio volume (scaling it to a 0-1 range)
        volume_factor = volume_level / 100
        audio = audio.volumex(volume_factor)

        # Set the start time of the audio in the video
        audio = audio.set_start(start_time)
        
        # Composite the original video audio with the new audio
        new_audio = CompositeAudioClip([video.audio, audio])

        # Set the composite audio to the video
        final_video = video.set_audio(new_audio)

        # Write the result to the output file
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

        print(f"Video saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

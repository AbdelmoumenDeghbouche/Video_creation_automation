from elevenlabs import save
from elevenlabs.client import ElevenLabs
import pandas as pd
import os
import random
from elevenlabs import VoiceSettings


def generate_ai_voice(arabic_text):
    audio_folder = "audios/"
    for file_name in os.listdir(audio_folder):
        file_path = os.path.join(audio_folder, file_name)
        os.remove(file_path)
        
    client = ElevenLabs(api_key=os.environ.get("API_KEY"))

    voices = [
        "jsCqWAovK2LkecY7zXl4",
        "jBpfuIE2acCO8z3wKNLl",
    ]
    response = client.voices.get_all()
    stablity_range = random.uniform(0.45, 0.55)
    similarity_boost_range = random.uniform(0.70, 0.80)

    audio = client.generate(
        text=arabic_text,
        voice=voices[random.choice(range(2))],
        model="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=stablity_range,
            similarity_boost=similarity_boost_range,
            use_speaker_boost=True,
        ),
    )
    save(audio, f"audios/audio1.mp3")

    print("Audio file saved as audio1.mp3")

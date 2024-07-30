from elevenlabs import save
from elevenlabs.client import ElevenLabs
import pandas as pd
import os
import random
from elevenlabs import VoiceSettings

client = ElevenLabs(api_key=os.environ.get("API_KEY"))

voices = [
    "jsCqWAovK2LkecY7zXl4",
    "jBpfuIE2acCO8z3wKNLl",
]
response = client.voices.get_all()
arabic_text = "السلام عليكم و رحمة الله تعالى و بركاته 🧙‍♀️ and hello"
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
save(audio, f"audio1.mp3")

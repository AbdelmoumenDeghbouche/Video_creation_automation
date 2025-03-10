import requests
import os
import random

# XI_API_KEY = "sk_dd9bd2cd63cb05c15efb1862d4cd1c3c0d7070216f76228a"
BASE_URL = "https://api.elevenlabs.io/v1"


def generate_ai_voice(arabic_text, eleven_labs_api_key):
    XI_API_KEY = eleven_labs_api_key
    audio_folder = "audios/"
    for file_name in os.listdir(audio_folder):
        file_path = os.path.join(audio_folder, file_name)
        os.remove(file_path)

    voices = [
        "jsCqWAovK2LkecY7zXl4",
        "jBpfuIE2acCO8z3wKNLl",
    ]
    stablity_range = random.uniform(0.45, 0.55)
    similarity_boost_range = random.uniform(0.70, 0.80)
    voice = voices[random.choice(range(2))]
    VOICE_ID = voice
    headers = {"Accept": "application/json", "xi-api-key": XI_API_KEY}
    url = f"{BASE_URL}/text-to-speech/{VOICE_ID}"

    payload = {
        "text": arabic_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": stablity_range,
            "similarity_boost": similarity_boost_range,
        },
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        audio_file_path = "audios/audio1.mp3"
        if not os.path.exists(audio_file_path):
            with open(audio_file_path, "wb") as audio_file:
                audio_file.write(response.content)
            print("Audio file generated successfully.")
        else:
            print("Audio file already exists.")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

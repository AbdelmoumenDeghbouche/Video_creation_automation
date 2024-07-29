import requests
from PIL import Image as PILImage
from io import BytesIO

def download_emoji_image(emoji):
    url = f"https://emojicdn.elk.sh/{emoji}"
    response = requests.get(url)
    if response.status_code == 200:
        return PILImage.open(BytesIO(response.content)).convert("RGBA")
    else:
        print("Failed to download the emoji image")
        return None

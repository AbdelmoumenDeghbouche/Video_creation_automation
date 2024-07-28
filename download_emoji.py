import requests
from PIL import Image
from io import BytesIO

# Mapping dictionary for emojis
emoji_mapping = {
    "💢": "anger_symbol",
    "😀": "grinning_face",
    "😂": "face_with_tears_of_joy",
    "❤️": "red_heart",
    # Add more emojis and their corresponding names here
}

def download_and_resize_emoji_image(emoji, emoji_size):
    # Get the emoji name from the mapping dictionary
    emoji_name = emoji_mapping.get(emoji)
    if not emoji_name:
        print(f"No mapping found for emoji: {emoji}")
        return
    
    # Construct the URL
    url = f"https://emojiapi.dev/api/v1/{emoji_name}/{emoji_size}.png"
    
    # Download the image
    response = requests.get(url)
    if response.status_code == 200:
        # Open the image using PIL
        emoji_image = Image.open(BytesIO(response.content))
        
        # Create a new image with transparent background and fixed size 1080x1920 pixels
        background_width, background_height = 1080, 1920
        new_image = Image.new("RGBA", (background_width, background_height), (255, 255, 255, 0))
        
        # Resize the emoji image
        emoji_image = emoji_image.resize((emoji_size, emoji_size), Image.LANCZOS)
        
        # Calculate position to paste the emoji in the center
        x = (background_width - emoji_size) // 2
        y = (background_height - emoji_size) // 2
        
        # Paste the emoji onto the new image
        new_image.paste(emoji_image, (x, y), emoji_image)
        
        # Save the final image
        new_image.save(f"emojis/{emoji_name}_1080x1920.png")
        print(f"Image for emoji '{emoji}' ({emoji_name}) downloaded, resized, and saved successfully.")
    else:
        print(f"Failed to download image for emoji '{emoji}' ({emoji_name}). HTTP Status Code: {response.status_code}")

# Example usage
emoji = "💢"
emoji_size = 200  # Change this value to resize the emoji
download_and_resize_emoji_image(emoji, emoji_size)

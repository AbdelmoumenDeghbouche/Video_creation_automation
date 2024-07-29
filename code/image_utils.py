from PIL import Image as PILImage
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

def create_centered_image(emoji_image, file_name, width=1080, height=1920):
    if emoji_image is None:
        return

    emoji_image = emoji_image.resize(
        (emoji_image.width * 2, emoji_image.height * 2), PILImage.LANCZOS
    )

    background = PILImage.new("RGBA", (width, height), (0, 0, 0, 0))

    emoji_width, emoji_height = emoji_image.size
    position = ((width - emoji_width) // 2, (height - emoji_height) // 2)

    background.paste(emoji_image, position, emoji_image)
    background.save(file_name, "PNG")
    print(f"Image saved as {file_name}")

def get_text_size(draw, text):
    with Image(width=1080, height=1920) as img:
        metrics = draw.get_font_metrics(img, text)
    return metrics.text_width, metrics.text_height

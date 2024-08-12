import os
import re
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

from emoji_utils import download_emoji_image
from image_utils import create_centered_image, get_text_size
from text_utils import (
    preprocess_text,
    is_english,
    is_arabic,
    contains_emoji,
)

def clear_images_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def process_text(text):
    preprocessed_text = preprocess_text(text)
    punctuation = "،.؟!؛:"
    pattern = f"[{punctuation}]"
    text_without_punctuation = re.sub(pattern, "", preprocessed_text)
    return text_without_punctuation.split()

def generate_images(words_list, images_folder):
    colors = ["#FDFA54", "#72F459", "white"]
    outline_color = "black"
    outline_thickness = 23
    shadow_color = "rgba(0, 0, 0, 0.5)"
    shadow_offset = (10, 10)

    english_font = "E:/arialbd.ttf"
    arabic_font = "E:/18728-arabicmodern-bold.otf"
    emoji_font = "E:/Noto_Color_Emoji/NotoColorEmoji-Regular.ttf"

    for index, text in enumerate(words_list):
        if contains_emoji(text):
            emoji_image = download_emoji_image(text)
            create_centered_image(emoji_image, f"{images_folder}/test_output_{index}.png")
            print(f"Emoji image saved for {text}")
            continue

        with Image(width=1080, height=1920, background=Color("transparent")) as img:
            with Drawing() as draw:
                draw.font = arabic_font if is_arabic(text) else english_font if is_english(text) else emoji_font
                draw.font_size = 125

                color = colors[index % len(colors)]
                text_width, text_height = get_text_size(draw, text)
                x = int((img.width - text_width)) // 2
                y = int((img.height + text_height)) // 2

                # Draw shadow
                draw.fill_color = Color(shadow_color)
                draw.stroke_color = Color("transparent")
                draw.text(x=x + shadow_offset[0], y=y + shadow_offset[1], body=text)

                # Draw outline
                draw.fill_color = Color("transparent")
                draw.stroke_color = Color(outline_color)
                draw.stroke_width = outline_thickness
                draw.text(x=x, y=y, body=text)

                # Draw text
                draw.fill_color = Color(color) if not contains_emoji(text) else Color("transparent")
                draw.stroke_color = Color("transparent")
                draw.text(x=x, y=y, body=text)
                draw(img)

            img.save(filename=f"{images_folder}/test_output_{index}.png")
            print(f"Text image saved for {text}")

def generate_images_from_text(arabic_text, images_folder):
    clear_images_folder(images_folder)
    words_list = process_text(arabic_text)
    generate_images(words_list, images_folder)
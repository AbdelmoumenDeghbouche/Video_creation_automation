import os
import re
from moviepy.editor import VideoFileClip
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
import cv2
import numpy as np

from emoji_utils import download_emoji_image
from image_utils import create_centered_image, get_text_size
from text_utils import (
    preprocess_text,
    remove_word,
    is_english,
    is_arabic,
    contains_emoji,
)

# Define the path to the images folder
images_folder = "images"

# Delete all files in the images folder
for filename in os.listdir(images_folder):
    file_path = os.path.join(images_folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            os.rmdir(file_path)
    except Exception as e:
        print(f"Failed to delete {file_path}. Reason: {e}")

arabic_text = "السلام عليكم و رحمة الله تعالى و بركته 🧙‍♀️ and hello"

preprocessed_text = preprocess_text(arabic_text)

punctuation = "،.؟!؛:"
pattern = f"[{punctuation}]"
text_without_punctuation = re.sub(pattern, "", preprocessed_text)

words_list = text_without_punctuation.split()

colors = ["#FDFA54", "#72F459", "white"]
outline_color = "black"
outline_thickness = 15
shadow_color = "rgba(0, 0, 0, 0.5)"
shadow_offset = (4, 4)

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
            if is_arabic(text):
                draw.font = arabic_font
            elif is_english(text):
                draw.font = english_font
            elif contains_emoji(text):
                draw.font = emoji_font
            draw.font_size = 82

            color = colors[index % len(colors)]
            text_width, text_height = get_text_size(draw, text)
            x = int((img.width - text_width)) // 2
            y = int((img.height + text_height)) // 2

            draw.fill_color = Color(shadow_color)
            draw.stroke_color = Color("transparent")
            draw.text(x=x + shadow_offset[0], y=y + shadow_offset[1], body=text)

            draw.fill_color = Color("transparent")
            draw.stroke_color = Color(outline_color)
            draw.stroke_width = outline_thickness
            draw.text(x=x, y=y, body=text)

            if not contains_emoji(text):
                draw.fill_color = Color(color)
            else:
                draw.fill_color = Color("transparent")

            draw.stroke_color = Color("transparent")
            draw.text(x=x, y=y, body=text)
            draw(img)

        img.save(filename=f"{images_folder}/test_output_{index}.png")
        print(f"Text image saved for {text}")

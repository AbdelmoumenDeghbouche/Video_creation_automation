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
from emoji_utils import words_list_final

# Global variable to store the index of the "zoba" image
zoba_image_index = None
new_word_list = []


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


def separate_linked_arabic_english(text):
    return re.sub(r"([ا-ي]+)([a-zA-Z]+)|([a-zA-Z]+)([ا-ي]+)", r"\1\3 \2\4", text)


def process_text(text):
    preprocessed_text = preprocess_text(text)
    separated_text = separate_linked_arabic_english(preprocessed_text)
    punctuation = "،.؟!؛:"
    pattern = f"[{punctuation}]"
    text_without_punctuation = re.sub(pattern, "", separated_text)
    return text_without_punctuation.split()


def generate_images(
    words_list,
    images_folder,
    arabic_font="assets/fonts/18728-arabicmodern-bold.otf",
    english_font="assets/fonts/arialbd.ttf",
    emoji_font="assets/fonts/NotoColorEmoji-Regular.ttf",
    font_size=175,
):
    global zoba_image_index

    colors = ["#FDFA54", "#72F459", "white"]
    outline_color = "black"
    outline_thickness = 23
    shadow_color = "rgba(0, 0, 0, 1.5)"
    shadow_offset = (30, 20)  # Increased offset for more noticeable shadow
    shadow_blur = 10  # Added blur to soften the shadow

    for index, text in enumerate(words_list):
        if contains_emoji(text):
            emoji_image = download_emoji_image(text)
            create_centered_image(
                emoji_image, f"{images_folder}/test_output_{index}.png"
            )
            print(f"Emoji image saved for {text}")
            continue

        with Image(width=1080, height=1920, background=Color("transparent")) as img:
            with Drawing() as draw:
                draw.font = (
                    arabic_font
                    if is_arabic(text)
                    else english_font if is_english(text) else emoji_font
                )
                draw.font_size = font_size

                color = colors[index % len(colors)]
                text_width, text_height = get_text_size(draw, text)
                x = int((img.width - text_width)) // 2
                y = int((img.height + text_height)) // 2

                # Draw shadow
                with img.clone() as shadow:
                    with Drawing() as shadow_draw:
                        shadow_draw.font = draw.font
                        shadow_draw.font_size = font_size
                        shadow_draw.fill_color = Color(shadow_color)
                        shadow_draw.stroke_color = Color("transparent")
                        shadow_draw.text(x=x, y=y, body=text)
                        shadow_draw(shadow)
                    shadow.blur(sigma=shadow_blur)
                    img.composite(shadow, left=shadow_offset[0], top=shadow_offset[1])

                # Draw outline
                draw.fill_color = Color("transparent")
                draw.stroke_color = Color(outline_color)
                draw.stroke_width = outline_thickness
                draw.text(x=x, y=y, body=text)

                # Draw text
                draw.fill_color = (
                    Color(color) if not contains_emoji(text) else Color("transparent")
                )
                draw.stroke_color = Color("transparent")
                draw.text(x=x, y=y, body=text)
                draw(img)

            img.save(filename=f"{images_folder}/test_output_{index}.png")
            print(f"Text image saved for {text}")

            if text == "zoba":
                zoba_image_index = index
                print(f"'zoba' word found at index: {zoba_image_index}")


def generate_images_from_text(
    arabic_text,
    images_folder,
    arabic_font_file="assets/fonts/18728-arabicmodern-bold.otf",
    font_size=175,
):
    clear_images_folder(images_folder)
    words_list = words_list_final
    generate_images(
        words_list, images_folder, arabic_font=arabic_font_file, font_size=font_size
    )

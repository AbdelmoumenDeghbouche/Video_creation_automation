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
from text_utils import preprocess_text, remove_word, is_english, is_arabic, contains_emoji

arabic_text = "حاولوا حظري وإسكاتي عندما كشفت هذه الخدعة للحصول على سكنات ببجي غير محدودة مجانا، و التي يستعملها أشهر اللاعبين، لكن مع زوبا لا للاحتكار سوف نجعل كل من يشاهد الفيديو يحصل على اي سكن يريد سواءا كان زي الغراب الاحمر او سكن المومياء و حتى سكن الدجاجة المضحك 😂، لكن من فضلكم لا تختاروا نفس السكن، لا نريد ان يحصل تضخم في اللعبة 😂😂، نعم الامر لا يصدق لكن ساثبت لك ان الطريقة تشتغل، فجيش زوبا في التعليقات سيخبرونك 👇، لذا أحضر بعض الفشار و شاهد العجب يحدث، كل ما عليكم 😂😂 فعله لتحقيق أمنيتكم 🧙‍♀️😂، هو دعمي أولا بلايك و follow، من فضلكم 🥺، اذا أتممت الخطوة الاولى، كل ما عليكم فعله هو زيارة موقع Zoba dot games واختيار شعار بابجي ثم إتباع الخطوات الموضحة في الموقع. فقط قوموا بإدخال معرف اللاعب ال ID أو اسم المستخدم الخاص بكم في اللعبة. ومبروك عليكم"

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
        create_centered_image(emoji_image, f"images/test_output_{index}.png")
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

        img.save(filename=f"images/test_output_{index}.png")
        print(f"Text image saved for {text}")

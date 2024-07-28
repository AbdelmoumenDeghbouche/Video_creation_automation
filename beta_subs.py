import re
from moviepy.editor import VideoFileClip
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
import cv2
import numpy as np
import os
import requests
from PIL import Image as PILImage
from io import BytesIO

# Mapping dictionary for emojis
emoji_mapping = {
    "💢": "anger_symbol",
    "😀": "grinning_face",
    "😂": "face_with_tears_of_joy",
    "❤️": "red_heart",
    # Add more emojis and their corresponding names here
    "❓❗": "exclamation_question_mark",
    "™️": "trade_mark",
    "ℹ️": "information",
    "↔️": "leftright_arrow",
    "↕️": "updown_arrow",
    "↖️": "upleft_arrow",
    "↗️": "upright_arrow",
    "↘️": "downright_arrow",
    "↙️": "downleft_arrow",
    "⌨️": "keyboard",
    "☀️": "sun",
    "☁️": "cloud",
    "☂️": "umbrella",
    "☃️": "snowman",
    "☄️": "comet",
    "☑️": "check_box_with_check",
    "☔️": "umbrella_with_rain_drops",
    "☕️": "hot_beverage",
    "☘️": "shamrock",
    "☠️": "skull_and_crossbones",
    "☢️": "radioactive",
    "☣️": "biohazard",
    "☦️": "orthodox_cross",
    "☸️": "wheel_of_dharma",
    "☹️": "frowning_face",
    "♀️": "female_sign",
    "♂️": "male_sign",
    "♈️": "aries",
    "♉️": "taurus",
    "♐️": "sagittarius",
    "♑️": "capricorn",
    "♒️": "aquarius",
    "♓️": "pisces",
    "♠️": "spade_suit",
    "♣️": "club_suit",
    "♥️": "heart_suit",
    "♦️": "diamond_suit",
    "♨️": "hot_springs",
    "⚒️": "hammer_and_pick",
    "⚓️": "anchor",
    "⚔️": "crossed_swords",
    "⚕️": "medical_symbol",
    "⚖️": "balance_scale",
    "⚗️": "alembic",
    "⚙️": "gear",
    "✂️": "scissors",
    "✔️": "check_mark_button",
    "✈️": "airplane",
    "✉️": "envelope",
    "✒️": "black_nib",
    "✔️": "check_mark",
    "✖️": "multiply",
    "✡️": "star_of_david",
    "✨": "sparkles",
    "✳️": "eightspoked_asterisk",
    "✴️": "eightpointed_star",
    "❄️": "snowflake",
    "❇️": "sparkle",
    "❓": "red_question_mark",
    "❔": "white_question_mark",
    "❕": "white_exclamation_mark",
    "❗️": "red_exclamation_mark",
    "❣️": "heart_exclamation",
    "❤️": "red_heart",
    "➕": "plus",
    "➖": "minus",
    "➗": "divide",
    "⤴️": "right_arrow_curving_up",
    "⤵️": "right_arrow_curving_down",
    "〰️": "wavy_dash",
    "㊗️": "japanese_congratulations_button",
    "㊙️": "japanese_secret_button",
    "😀": "grinning_face",
    "😃": "grinning_face_with_big_eyes",
    "😄": "grinning_face_with_smiling_eyes",
    "😁": "beaming_face_with_smiling_eyes",
    "😆": "grinning_squinting_face",
    "😅": "grinning_face_with_sweat",
    "🤣": "rolling_on_the_floor_laughing",
    "😂": "face_with_tears_of_joy",
    "🙂": "slightly_smiling_face",
    "🙃": "upsidedown_face",
    "😉": "winking_face",
    "😊": "smiling_face_with_smiling_eyes",
    "😇": "smiling_face_with_halo",
    "🥰": "smiling_face_with_hearts",
    "😍": "smiling_face_with_hearteyes",
    "🤩": "starstruck",
    "😘": "face_blowing_a_kiss",
    "😗": "kissing_face",
    "☺️": "smiling_face",
    "😚": "kissing_face_with_closed_eyes",
    "😙": "kissing_face_with_smiling_eyes",
    "🥲": "smiling_face_with_tear",
    "😋": "face_savoring_food",
    "😛": "face_with_tongue",
    "😜": "winking_face_with_tongue",
    "🤪": "zany_face",
    "😝": "squinting_face_with_tongue",
    "🤑": "moneymouth_face",
    "🤗": "hugging_face",
    "🤭": "face_with_hand_over_mouth",
    "🤫": "shushing_face",
    "🤔": "thinking_face",
    "🤐": "zippermouth_face",
    "🤨": "face_with_raised_eyebrow",
    "😐️": "neutral_face",
    "😑": "expressionless_face",
    "😶": "face_without_mouth",
    "😶‍🌫️": "face_in_clouds",
    "😏": "smirking_face",
    "😒": "unamused_face",
    "🙄": "face_with_rolling_eyes",
    "😬": "grimacing_face",
    "😮‍💨": "face_exhaling",
    "🤥": "lying_face",
    "😌": "relieved_face",
    "😔": "pensive_face",
    "😪": "sleepy_face",
    "🤤": "drooling_face",
    "😴": "sleeping_face",
    "😷": "face_with_medical_mask",
    "🤒": "face_with_thermometer",
    "🤕": "face_with_headbandage",
    "🤢": "nauseated_face",
    "🤮": "face_vomiting",
    "🤧": "sneezing_face",
    "🥵": "hot_face",
    "🥶": "cold_face",
    "🥴": "woozy_face",
    "😵": "knockedout_face",
    "😵‍💫": "face_with_spiral_eyes",
    "🤯": "exploding_head",
    "🤠": "cowboy_hat_face",
    "🥳": "partying_face",
    "🥸": "disguised_face",
    "😎": "smiling_face_with_sunglasses",
    "🤓": "nerd_face",
    "🧐": "face_with_monocle",
    "😕": "confused_face",
    "😟": "worried_face",
    "🙁": "slightly_frowning_face",
    "😮": "face_with_open_mouth",
    "😯": "hushed_face",
    "😲": "astonished_face",
    "😳": "flushed_face",
    "🥺": "pleading_face",
    "😦": "frowning_face_with_open_mouth",
    "😧": "anguished_face",
    "😨": "fearful_face",
    "😰": "anxious_face_with_sweat",
    "😥": "sad_but_relieved_face",
    "😢": "crying_face",
    "😭": "loudly_crying_face",
    "😱": "face_screaming_in_fear",
    "😖": "confounded_face",
    "😣": "persevering_face",
    "😞": "disappointed_face",
    "😓": "downcast_face_with_sweat",
    "😩": "weary_face",
    "😫": "tired_face",
    "🥱": "yawning_face",
    "😤": "face_with_steam_from_nose",
    "😡": "pouting_face",
    "😠": "angry_face",
    "🤬": "face_with_symbols_on_mouth",
    "😈": "smiling_face_with_horns",
    "👿": "angry_face_with_horns",
    "💀": "skull",
    "💩": "pile_of_poo",
    "🤡": "clown_face",
    "👹": "ogre",
    "👺": "goblin",
    "👻": "ghost",
    "👽": "alien",
    "👾": "alien_monster",
    "🤖": "robot",
    "😺": "grinning_cat",
    "😸": "grinning_cat_with_smiling_eyes",
    "😹": "cat_with_tears_of_joy",
    "😻": "smiling_cat_with_hearteyes",
    "😼": "cat_with_wry_smile",
    "😽": "kissing_cat",
    "🙀": "weary_cat",
    "😿": "crying_cat",
    "😾": "pouting_cat",
    "🙈": "see_no_evil_monkey",
    "🙉": "hear_no_evil_monkey",
    "🙊": "speak_no_evil_monkey",
    "💋": "kiss_mark",
    "💌": "love_letter",
    "💘": "heart_with_arrow",
    "💝": "heart_with_ribbon",
    "💖": "sparkling_heart",
    "💗": "growing_heart",
    "💓": "beating_heart",
    "💞": "revolving_hearts",
    "💕": "two_hearts",
    "💟": "heart_decoration",
    "❣️": "heart_exclamation",
    "💔": "broken_heart",
    "❤️‍🔥": "heart_on_fire",
    "❤️‍🩹": "mending_heart",
    "🧡": "orange_heart",
    "💛": "yellow_heart",
    "💚": "green_heart",
    "💙": "blue_heart",
    "💜": "purple_heart",
    "🤎": "brown_heart",
    "🖤": "black_heart",
    "🤍": "white_heart",
    "💯": "hundred_points",
    "💢": "anger_symbol",
    "💥": "collision",
    "💫": "dizzy",
    "💦": "sweat_droplets",
    "💨": "dashing_away",
    "🕳️": "hole",
    "💣": "bomb",
    "💬": "speech_balloon",
    "👁️‍🗨️": "eye_in_speech_bubble",
    "🗨️": "left_speech_bubble",
    "🗯️": "right_anger_bubble",
    "💭": "thought_balloon",
    "💤": "zzz",
    "🦾": "mechanical_arm",
    "🦿": "mechanical_leg", 
    "🧠": "brain",
    "🫀": "anatomical_heart",
    "🫁": "lungs",
    "🦷": "tooth",
    "🦴": "bone",
    "👁️": "eyes",
    "👁": "eye",
    "👅": "tongue",
    "👄": "mouth",
    "🧞": "genie",
    "🧟": "zombie",
    "👯": "people_with_bunny_ears",
    "🤺": "person_fencing",
    "⛷️": "skier",
    "👪": "family",
    "🗣️": "speaking_head",
    "👤": "bust_in_silhouette",
    "👥": "busts_in_silhouette",
    "🫂": "people_hugging",
    "👣": "footprints",
    "🏻": "light_skin_tone",
    "🏼": "mediumlight_skin_tone",
    "🏽": "medium_skin_tone",
    "🏾": "mediumdark_skin_tone",
    "🏿": "dark_skin_tone",
    "🦰": "red_hair",
    "🦱": "curly_hair",
    "🦳": "white_hair",
    "🦲": "bald",
    "🐵": "monkey_face",
    "🐒": "monkey",
    "🦍": "gorilla",
    "🦧": "orangutan",
    "🐶": "dog_face",
    "🐕": "dog",
    "🦮": "guide_dog",
    "🐕‍🦺": "service_dog",
    "🐩": "poodle",
    "🐺": "wolf",
    "🦊": "fox",
    "🦝": "raccoon",
    "🐱": "cat_face",
    "🐈": "cat",
    "🐈‍⬛": "black_cat",
    "🦁": "lion",
    "🐯": "tiger_face",
    "🐅": "tiger",
    " Leopard ": "leopard",
    "🐎": "horse_face",
    "🐘": "elephant",
    "🦣": "mammoth",
    "🦏": "rhinoceros",
    "🦛": "hippopotamus",
    "🐭": "mouse_face",
    "🐁": "mouse",
    "🐀": "rat",
    "🐹": "hamster",
    "🐰": "rabbit_face",
    "🐇": "rabbit",
    "🐿️": "chipmunk",
    "🦫": "beaver",
    "🦔": "hedgehog",
    "🦇": "bat",
    "🐻": "bear",
    "🐼": "panda",
    "🦥": "sloth",
    "🦦": "otter",
    "🦨": "skunk",
    "🦘": "kangaroo",
    "🦡": "badger",
    "🐾": "paw_prints",
    "🦃": "turkey",
    "🐔": "chicken",
    "🐓": "rooster",
    "🐥": "hatching_chick",
    "🐤": "baby_chick",
    "🐣": "frontfacing_baby_chick",
    "🐦": "bird",
    "🐧": "penguin",
    "🕊️": "dove",
    "🦅": "eagle",
    "🦆": "duck",
    "🦢": "swan",
    "🦉": "owl",
    "🦤": "dodo",
    "🌺": "hibiscus",
    "🌻": "sunflower",
    "🌼": "blossom",
    "🌷": "tulip",
    "🌱": "seedling",
    "🪴": "potted_plant",
    "🌲": "evergreen_tree",
    "🌳": "deciduous_tree",
    "🌴": "palm_tree",
    "🌵": "cactus",
    "🌾": "sheaf_of_rice",
    "🌿": "herb",
    "🍀": "four_leaf_clover",
    "🍁": "maple_leaf",
    "🍂": "fallen_leaf",
    "🍃": "leaf_fluttering_in_wind",
    "🍇": "grapes",
    "🍈": "melon",
    "🍉": "watermelon",
    "🍊": "tangerine",
    "🍋": "lemon",
    "🍌": "banana",
    "🍍": "pineapple",
    "🥝": "kiwi_fruit",
    "🍎": "red_apple",
    "🍏": "green_apple",
    "🍐": "pear",
    "🍑": "peach",
    "🍒": "cherries",
    "🍓": "strawberry",
    "🫐": "blueberries",
    "🥭": "mango",
    "🍅": "tomato",
    "🫒": "olive",
    "🥥": "coconut",
    "🥑": "avocado",
    "🍆": "eggplant",
    "🥔": "potato",
    "🥕": "carrot",
    "🌽": "ear_of_corn",
    "🌶️": "hot_pepper",
    "🫑": "bell_pepper",
    "🥒": "cucumber",
    "🥬": "leafy_green",
    "🥦": "broccoli",
    "🧄": "garlic",
    "🧅": "onion",
    "🍄": "mushroom",
    "🥜": "peanuts",
    "🌰": "chestnut",
    "🍞": "bread",
    "🥐": "croissant",
    "🥖": "baguette_bread",
    "🫛": "flatbread",
    "🥨": "pretzel",
    "🥯": "bagel",
    "🥞": "pancakes",
    "🧇": "waffle",
    "🧀": "cheese_wedge",
    "🍖": "meat_on_bone",
    "🍗": "poultry_leg",
    "🥩": "cut_of_meat",
    "🥓": "bacon",
    "🍔": "hamburger",
    "🍟": "french_fries",
    "🍕": "pizza",
    "🌭": "hot_dog",
    "🥪": "sandwich",
    "🌮": "taco",
    "🌯": "burrito",
    "🫔": "tamale",
    "🥙": "stuffed_flatbread",
    "🧆": "falafel",
    "🥚": "egg",
    "🍳": "cooking",
    "🥘": "shallow_pan_of_food",
    "🍲": "pot_of_food",
    "🫕": "fondue",
    "🥣": "bowl_with_spoon",
    "🥗": "green_salad",
    "🍿": "popcorn"
}

def download_and_resize_emoji_image(emoji, emoji_size):
    emoji_name = emoji_mapping.get(emoji)
    if not emoji_name:
        print(f"No mapping found for emoji: {emoji}")
        return None

    url = f"https://emojiapi.dev/api/v1/{emoji_name}/{emoji_size}.png"
    response = requests.get(url)
    if response.status_code == 200:
        emoji_image = PILImage.open(BytesIO(response.content))
        background_width, background_height = 1080, 1920
        new_image = PILImage.new("RGBA", (background_width, background_height), (255, 255, 255, 0))
        emoji_image = emoji_image.resize((emoji_size, emoji_size), PILImage.LANCZOS)
        x = (background_width - emoji_size) // 2
        y = (background_height - emoji_size) // 2
        new_image.paste(emoji_image, (x, y), emoji_image)
        return new_image
    else:
        print(f"Failed to download image for emoji '{emoji}' ({emoji_name}). HTTP Status Code: {response.status_code}")
        return None

def remove_word(word_list, word_to_remove):
    return [word for word in word_list if word != word_to_remove]

def preprocess_text(text):
    emoji_pattern = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]')
    split_text = emoji_pattern.split(text)
    emojis = emoji_pattern.findall(text)
    
    combined_text = []
    for part, emoji in zip(split_text, emojis + [""]):
        combined_text.append(part)
        if emoji:
            combined_text.append(emoji)
    return "".join(combined_text)

arabic_text = "حاولوا حظري وإسكاتي عندما كشفت هذه الخدعة للحصول على سكنات ببجي غير محدودة مجانا، و التي يستعملها أشهر اللاعبين، لكن مع زوبا لا للاحتكار سوف نجعل كل من يشاهد الفيديو يحصل على اي سكن يريد سواءا كان زي الغراب الاحمر او سكن المومياء و حتى سكن الدجاجة المضحك 😂، لكن من فضلكم لا تختاروا نفس السكن، لا نريد ان يحصل تضخم في اللعبة 😂😂، نعم الامر لا يصدق لكن ساثبت لك ان الطريقة تشتغل، فجيش زوبا في التعليقات سيخبرونك 👇، لذا أحضر بعض الفشار و شاهد العجب يحدث، كل ما عليكم 😂😂 فعله لتحقيق أمنيتكم 🧙‍♀️😂، هو دعمي أولا بلايك و follow، من فضلكم 🥺، اذا أتممت الخطوة الاولى، كل ما عليكم فعله هو زيارة موقع Zoba dot games واختيار شعار بابجي ثم إتباع الخطوات الموضحة في الموقع. فقط قوموا بإدخال معرف اللاعب ال ID أو اسم المستخدم الخاص بكم في اللعبة. ومبروك عليكم"

# Preprocess text to handle emojis
preprocessed_text = preprocess_text(arabic_text)

# Remove punctuation
punctuation = "،.؟!؛:"
pattern = f"[{punctuation}]"
text_without_punctuation = re.sub(pattern, "", preprocessed_text)

# Split the text into words
words_list = text_without_punctuation.split()

def get_text_size(draw, text):
    with Image(width=1080, height=1920) as img:
        metrics = draw.get_font_metrics(img, text)
    return metrics.text_width, metrics.text_height

colors = ["#FDFA54", "#72F459", "white"]
outline_color = "black"
outline_thickness = 15
shadow_color = "rgba(0, 0, 0, 0.5)"
shadow_offset = (4, 4)

english_font = "E:/arialbd.ttf"
arabic_font = "E:/18728-arabicmodern-bold.otf"
emoji_font = "E:/Noto_Color_Emoji/NotoColorEmoji-Regular.ttf"

def is_english(word):
    return bool(re.match(r"^[a-zA-Z0-9]+$", word))

def is_arabic(word):
    return bool(re.match(r'^[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+$', word))

def contains_emoji(word):
    return bool(re.search(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]', word))

for index, text in enumerate(words_list):
    if contains_emoji(text):
        emoji_image = download_and_resize_emoji_image(text, 200)
        if emoji_image:
            emoji_image.save(f"images/test_output_{index}.png")
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

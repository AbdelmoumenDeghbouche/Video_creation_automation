import requests
from PIL import Image as PILImage
from io import BytesIO
from text_utils import preprocess_text
import re

words_list_final = None


def separate_linked_arabic_english(text):
    return re.sub(r"([ا-ي]+)([a-zA-Z]+)|([a-zA-Z]+)([ا-ي]+)", r"\1\3 \2\4", text)


def process_text(text):
    preprocessed_text = preprocess_text(text)
    separated_text = separate_linked_arabic_english(preprocessed_text)
    punctuation = "،.؟!؛:"
    pattern = f"[{punctuation}]"
    text_without_punctuation = re.sub(pattern, "", separated_text)
    return text_without_punctuation.split()


arabic_text = "محبي لعبة ببجي ، لماذا تضييع الوقت في اللعب من اجل الحصول على سكنات مملة مثل هذا السكن.... ، بدلا من ذلك حرب طريقة زوبا التي ستستغرق منك دقائق فقط و ستحصل على سكنات اسطورية مثل بذلة المعاقب الثلجي و بذلة الفرعون الاسطورية و حتى سكن الامفور الثلجي ، بمعنى آخر ، كل السكنات النادرة ستحصل عليها دون دفع اي قرش ، كل ما عليكم فعله هو نسخ الفيديو أولا ،و من ثم زيارة موقع Zoba dot games واختيارُ شعارِ بَابْجِي ثم إتِّبَاعُ الخطوات الموضحة في الموقع. لن تحتاجوا إلى توفير أي تكاليف ، فقط قوموا بإدخال مُعَرِّفِ اللاعب الID أو اسم المستخدم الخاص بكم في اللعبة. ومبروك عليكم. لا تقلقوا فهذا الموقع موثوق وآمن، فمن غير المنطقي أن يتم حَظْرُ حسابكم بسبب إدخال الID الخاص بكم فقط.و كالعادة لا تنسو زوبا الطيب من دعائكم الخير يا محبي"
words_list_final = process_text(arabic_text)


def download_emoji_image(emoji):
    url = f"https://emojicdn.elk.sh/{emoji}"
    response = requests.get(url)
    if response.status_code == 200:
        return PILImage.open(BytesIO(response.content)).convert("RGBA")
    else:
        print(f"Failed to download the emoji image for: {emoji}")
        # Remove the emoji from words_list if download fails
        if emoji in words_list_final:
            words_list_final.remove(emoji)
            print("new wordlist without failed emoji ", words_list_final)
        return None

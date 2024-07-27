import re

"""
this script converts text into a list of words and saves it in a file.
and it's mandatory to if you want to generate subtitles for a video 
where you process the text word by word. each word with its own style.
converting theme to images to add them as overlay to the video.
"""


def remove_diacritics(text):
    arabic_diacritics = re.compile(r"[\u064B-\u0652]")
    cleaned_text = re.sub(arabic_diacritics, "", text)
    return cleaned_text


text_with_diacritics = """
السلامُ عليكم ورحمة الله وبركاته
"""
text_without_punctuation = re.sub(r"[^\w\s]", "", text_with_diacritics)
words_list = text_without_punctuation.split()
f = open("demofile2.txt", "a", encoding="utf-16")
f.write(str(words_list))
f.close()

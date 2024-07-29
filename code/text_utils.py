import re

def preprocess_text(text):
    emoji_pattern = re.compile(
        r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]"
    )
    split_text = emoji_pattern.split(text)
    emojis = emoji_pattern.findall(text)

    combined_text = []
    for part, emoji in zip(split_text, emojis + [""]):
        combined_text.append(part)
        if emoji:
            combined_text.append(emoji)
    return "".join(combined_text)

def remove_word(word_list, word_to_remove):
    return [word for word in word_list if word != word_to_remove]

def is_english(word):
    return bool(re.match(r"^[a-zA-Z0-9]+$", word))

def is_arabic(word):
    return bool(re.match(r"^[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+$", word))

def contains_emoji(word):
    return bool(
        re.search(
            r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]",
            word,
        )
    )

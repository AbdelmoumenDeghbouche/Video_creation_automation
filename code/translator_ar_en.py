from googletrans import Translator


def translate_arabic_to_english(arabic_text):
    # Create a translator object
    translator = Translator()

    # Translate Arabic text to English
    translation = translator.translate(arabic_text, src="ar", dest="en")

    # Print the translated text
    print(f"Original: {arabic_text}")
    print(f"Translated: {translation.text}")
    return translation.text

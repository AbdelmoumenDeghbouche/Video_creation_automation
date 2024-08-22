from googletrans import Translator

# Create a translator object
translator = Translator()

# Arabic text to translate
arabic_text = "تصفيق"

# Translate Arabic text to English
translation = translator.translate(arabic_text, src="ar", dest="en")

# Print the translated text
print(f"Original: {arabic_text}")
print(f"Translated: {translation.text}")

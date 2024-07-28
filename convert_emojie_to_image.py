from PIL import Image, ImageDraw, ImageFont
import emoji

def emoji_to_image(emoji_char, font_path='E:/Noto_Emoji/NotoColorEmoji-Regular.ttf', font_size=100, image_size=(200, 200), output_file='emoji_image.png'):
    # Create an image with white background
    image = Image.new('RGBA', image_size, (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Load a font
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        # If the specified font is not available, use the default font
        font = ImageFont.load_default()

    # Calculate text size and position
    text_bbox = draw.textbbox((0, 0), emoji_char, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (image_size[0] - text_width) / 2
    text_y = (image_size[1] - text_height) / 2

    # Draw the emoji on the image
    draw.text((text_x, text_y), emoji_char, font=font, fill=(0, 0, 0, 255))

    # Save the image
    image.save(output_file)

# Example usage
emoji_name = ':smiling_face_with_sunglasses:'
emoji_char = emoji.emojize(emoji_name)
emoji_to_image(emoji_char)

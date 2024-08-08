# Video_creation_automation
# Subtitle Generation and Image Creation Project

This project is designed to generate images with stylized subtitles for videos. It handles various types of text, including Arabic, English, and emojis, and processes them into centered, transparent images with custom colors, outlines, and shadows.

## Features

- **Text Preprocessing:** Removes punctuation from input text and handles both Arabic and English text, as well as emojis.
- **Image Creation:** Generates images with centered text or emojis, with customizable colors, outlines, shadows, and fonts.
- **Emoji Handling:** Automatically downloads and processes emoji images, saving them as standalone images.

## Installation

To set up the project, follow these steps:

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/your-username/subtitle-image-creation.git
    cd subtitle-image-creation
    ```

2. **Install Dependencies:**

    This project requires the following Python libraries:

    - `moviepy`
    - `wand`
    - `opencv-python`
    - `numpy`

    Install them using pip:

    ```bash
    pip install moviepy Wand opencv-python numpy
    ```

3. **Font Setup:**

    Ensure you have the following fonts available:

    - `arialbd.ttf` for English text
    - `arabicmodern-bold.otf` for Arabic text
    - `NotoColorEmoji-Regular.ttf` for emojis

    Update the paths to these fonts in the script as needed.

## Usage

The script processes a given string, removing punctuation and creating images for each word or emoji in the string. Images are saved in the `images` folder.

### Example

1. **Define Your Text:**

    ```python
    arabic_text = "السلام عليكم و رحمة الله بركته 🧙‍♀️ and hello"
    ```

2. **Run the Script:**

    Simply run the script, and it will generate images for each word or emoji in the text.

    ```bash
    python create_subtitles.py
    ```

    The generated images will be saved in the `images` folder.

### Cleanup

The script automatically deletes any existing files in the `images` folder before generating new images, ensuring that only the latest output is stored.

## Customization

You can customize the following:

- **Colors:** Modify the `colors` list to change the color sequence used for the text.
- **Fonts:** Change the font paths to use different fonts.
- **Text Styles:** Adjust the `outline_color`, `outline_thickness`, `shadow_color`, and `shadow_offset` to customize the text appearance.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgements

Thanks to the contributors of the libraries used in this project: `moviepy`, `wand`, `opencv-python`, and `numpy`.

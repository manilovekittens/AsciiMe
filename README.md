Asciime - ASCII and Braille Image Accessibility Converter
=========================================================

Asciime is a Python-based accessibility tool that converts images into ASCII art and generates alt text using Braille characters. It aims to support visually impaired users by making image content more accessible. It also evaluates image contrast and includes a playful feature: sharing a random cat fact if cat-related keywords are found in the description.

---------------------------------------------------------
System Requirements
---------------------------------------------------------
- Python 3.9 or higher
- Operating System: Windows, macOS, or Linux

---------------------------------------------------------
Installation Instructions
---------------------------------------------------------

1. Clone or download this project directory.
2. Open a terminal (or command prompt) and navigate to the project folder.
3. Install the required dependencies using:

   pip install -r requirements.txt

---------------------------------------------------------
Running Asciime
---------------------------------------------------------

To run the program:

   python asciime.py

You will be prompted to enter:
- An image file path (local file) or an image URL.
- A short description of the image.
- Whether you want to save the output to a text file (y/n).

---------------------------------------------------------
Features
---------------------------------------------------------
- Converts images to ASCII art for terminal display.
- Generates Unicode Braille alt text from the provided description.
- Analyzes grayscale contrast to flag accessibility concerns.
- Outputs results to the terminal and optionally saves to file.
- If your description includes "cat", "kitten", or "cats", a fun cat fact will be displayed.

---------------------------------------------------------
Limitations
---------------------------------------------------------
- Supports only common image formats: .png, .jpg, .jpeg, and .webp.
- ASCII rendering is best with clean, simple images.
- Braille encoding currently supports lowercase letters and basic punctuation only.

Thank you for using Asciime!

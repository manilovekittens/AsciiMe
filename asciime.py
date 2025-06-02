from PIL import Image
import random
import re
import requests
from io import BytesIO

# ASCII characters from dark to light
ASCII_CHARS = "@%#*+=-:. "

# Braille mappings for lowercase letters
BRAILLE_MAP = {
    chr(i): chr(0x2800 + i_offset) for i, i_offset in zip(
        range(ord('a'), ord('z') + 1),
        [0x01, 0x03, 0x09, 0x19, 0x11, 0x1B, 0x0B, 0x13, 0x0A, 0x1A,
         0x05, 0x07, 0x0D, 0x1D, 0x15, 0x17, 0x0F, 0x1F, 0x0E, 0x1E,
         0x25, 0x27, 0x2D, 0x3D, 0x35, 0x37]
    )
}
# Braille capital sign and punctuation mappings
CAPITAL_SIGN = chr(0x2820)
PUNCTUATION_MAP = {
    '.': '⠲', ',': '⠂', '!': '⠖', '?': '⠦', "'": '⠄',
    '"': '⠶', '-': '⠤', ':': '⠱', ';': '⠰', '(': '⠷', ')': '⠾'
}
# Fun facts about cats list
CAT_FACTS = [
    "Cats sleep for about 13 to 16 hours a day.",
    "A group of kittens is called a kindle!",
    "Cats can make over 100 different sounds.",
    "The oldest cat ever lived to be 38 years old!",
    "Cats' purring may help them heal faster.",
    "Each cat's nose print is unique—like a human fingerprint!",
    "Kittens can purr when they're just a few days old.",
    "Cats can rotate their ears 180 degrees.",
    "The richest cat in the world had a $7 million inheritance.",
    "House cats share 95.6% of their DNA with tigers."
]

# Input validator for local or web image paths
def get_valid_image_input():
    while True:
        image_path = input("Enter the path to the image (local or URL): ").strip()
        try:
            if image_path.startswith("http"):
                response = requests.get(image_path)
                response.raise_for_status()
                # Check if the content is actually an image
                if "image" in response.headers["Content-Type"]:
                    return BytesIO(response.content)
                else:
                    raise ValueError("URL does not point to an image.")
            else:
                with open(image_path, "rb") as f:
                    return image_path
        except Exception:
            print("\nUnable to load image. Please check your input.")
            print("Hint: Make sure your URL or file path ends in .png, .jpg, .jpeg, .webp, etc.\n")

# Convert alt text to Braille
def text_to_braille(description):
    braille_output = ""
    for char in description:
        if char.isalpha():
            if char.isupper():
                braille_output += CAPITAL_SIGN
                char = char.lower()
            braille_output += BRAILLE_MAP.get(char, "⍰")
        elif char == " ":
            braille_output += " "
        elif char in PUNCTUATION_MAP:
            braille_output += PUNCTUATION_MAP[char]
        else:
            braille_output += "⍰"
    return braille_output

# Analyze contrast level of grayscale image
def analyze_contrast(img):
    pixels = list(img.getdata())
    mean = sum(pixels) / len(pixels)
    variance = sum((p - mean) ** 2 for p in pixels) / len(pixels)
    stddev = variance ** 0.5

    if stddev < 20:
        return "Low Contrast — may be difficult for some users to distinguish."
    elif stddev < 50:
        return "Medium Contrast — acceptable, but could be improved."
    else:
        return "High Contrast — good accessibility."


# Convert image to ASCII image 
def image_to_ascii(image_input, new_width=100):
    try:
        img = Image.open(image_input).convert('L')
        width, height = img.size
        aspect_ratio = height / width
        new_height = int(new_width * aspect_ratio * 0.5)
        img = img.resize((new_width, new_height))

        contrast_note = analyze_contrast(img)

        pixels = img.getdata()
        ascii_str = ''.join(ASCII_CHARS[pixel // 32] for pixel in pixels)
        ascii_img = "\n".join(ascii_str[i:(i+new_width)] for i in range(0, len(ascii_str), new_width))

        return ascii_img, contrast_note

    except Exception as e:
        return f"Error: {e}", None


# Checks if cat related words are in the description
def contains_cat_words(text):
    cat_words = ["cat", "cats", "kitten", "kittens"]
    return any(word in text.lower() for word in cat_words)

# Generates random fun fact about cat
def generate_cat_fact():
    return random.choice(CAT_FACTS)

# Main program
if __name__ == "__main__":
    image_input = get_valid_image_input()

    ascii_art, contrast = image_to_ascii(image_input)
    print("\nASCII Image Representation:\n")
    print(ascii_art)

    if contrast:
        print("\nImage Contrast Analysis:\n" + contrast)


    # Image description with character limit
    while True:
        description = input("\nEnter a short image description (max 120 characters): ")
        if len(description) <= 120:
            break
        print("\nYour description is too long. Please enter no more than 120 characters.")

    braille = text_to_braille(description)
    print("\nBraille Representation of Description:\n")
    print(braille)

    # Cat fun fact generator
    if contains_cat_words(description):
        print("\nMEOW! Cat Detected! Here's a fun cat fact:\n")
        print(generate_cat_fact())
    
    # Asks user if they want to save their result as a text file
    save_output = input("\nWould you like to save the output to a text file? (y/n): ").strip().lower()
    if save_output == 'y':
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"asciime_output_{timestamp}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write("ASCII Image Representation:\n")
            file.write(ascii_art + "\n\n")
            file.write("Braille Representation of Description:\n")
            file.write(braille + "\n")
            file.write("\nImage Contrast Analysis:\n" + contrast + "\n")

            if contains_cat_words(description):
                file.write("\nFun Cat Fact:\n" + generate_cat_fact() + "\n")
        print(f"Output saved to {filename}.")


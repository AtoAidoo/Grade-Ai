import pytesseract
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Ensure the correct path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'


def extract_answers(image_path):
    # Open the image using PIL
    image = Image.open(image_path)

    # Convert the image to grayscale
    image = image.convert('L')

    # Use pytesseract to extract text
    text = pytesseract.image_to_string(image)

    # Dummy implementation of answer extraction from text
    # This is a placeholder. You'll need a more sophisticated method to parse the text.
    answers = []
    lines = text.split('\n')
    for line in lines:
        if 'A' in line:
            answers.append('A')
        elif 'B' in line:
            answers.append('B')
        elif 'C' in line:
            answers.append('C')
        elif 'D' in line:
            answers.append('D')

    return answers


# Example usage
image_path = 'path/to/multiple_choice_sheet.jpg'
answers = extract_answers(image_path)
print("Extracted Answers:", answers)

# Display the image
image = Image.open(image_path)
plt.imshow(image, cmap='gray')
plt.axis('off')
plt.show()

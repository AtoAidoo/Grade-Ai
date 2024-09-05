from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image
import cv2

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the correct path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    result = process_image_and_tally(filepath)

    return jsonify(result)


def retrieve_and_preprocess_image(filepath):
    # Load the image using OpenCV
    image = cv2.imread(filepath)

    # Check if the image was loaded successfully
    if image is None:
        raise ValueError("Image not loaded properly. Check the file path.")

    return image


def process_image(filepath):
    # Preprocess the image with OpenCV
    image = retrieve_and_preprocess_image(filepath)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding or other image enhancement techniques
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # OCR using pytesseract
    text = pytesseract.image_to_string(thresh)

    return text


def compare_text_with_answers(text):
    # Dummy correct answers
    correct_answers = ['A', 'B', 'C', 'D', 'A']

    # Extracted answers from OCR text
    extracted_answers = []
    lines = text.split('\n')
    for line in lines:
        if 'A' in line:
            extracted_answers.append('A')
        elif 'B' in line:
            extracted_answers.append('B')
        elif 'C' in line:
            extracted_answers.append('C')
        elif 'D' in line:
            extracted_answers.append('D')

    # Calculate the score
    score = sum(1 for a, b in zip(extracted_answers, correct_answers) if a == b)

    return {'score': score, 'answers': extracted_answers}


def process_image_and_tally(filepath):
    # Extract text from the image
    text = process_image(filepath)

    # Compare text with correct answers
    result = compare_text_with_answers(text)

    # Optionally save the result to a database or file
    # save_result(result)

    return result


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)

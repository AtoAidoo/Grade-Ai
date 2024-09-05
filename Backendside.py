from flask import Flask, request, jsonify
from  werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image

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

    result = process_image(filepath)

    return jsonify(result)


def process_image(filepath):
    # Open the image using PIL
    image = Image.open(filepath)
    image = image.convert('L')  # Convert to grayscale

    # Use pytesseract to extract text
    text = pytesseract.image_to_string(image)

    # Dummy implementation of answer extraction from text
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

    # Dummy correct answers
    correct_answers = ['A', 'B', 'C', 'D', 'A']
    score = sum(1 for a, b in zip(answers, correct_answers) if a == b)

    return {'score': score, 'answers': answers}


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)

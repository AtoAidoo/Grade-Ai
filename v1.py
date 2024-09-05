from flask import Flask, request, make_response, jsonify
import os
from uuid import uuid4

app = Flask(__name__)

# Configure temporary storage directory (ensure write permissions)
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

@app.route('/store-image', methods=['POST'])
def store_image():
    if request.method == 'POST':
        try:
            # Extract image data from request (adjust based on your React Native code)
            image_data = request.form.get('imageData')  # Assuming base64-encoded image
            if not image_data:
                return make_response(jsonify({'error': 'Missing image data'}), 400)

            # Generate a unique filename with extension (based on image type)
            filename = f"{uuid4()}.{get_image_extension(image_data)}"

            # Save image to temporary storage
            with open(os.path.join(TEMP_DIR, filename), 'wb') as f:
                f.write(image_data.encode())  # Decode base64 before writing

            # Return success message with the unique filename
            return jsonify({'success': True, 'filename': filename})
        except Exception as e:
            print(f"Error storing image: {e}")
            return make_response(jsonify({'error': 'Internal server error'}), 500)

def get_image_extension(image_data):
    """Extracts the image extension from base64-encoded data."""
    # Improved logic to handle various image formats (adjust if needed)
    header, data = image_data.split(',', 1)
    if header.startswith('data:image/'):
        return header.split('/')[1].split(';')[0]
    else:
        return None  # Handle unknown image format gracefully

if __name__ == '__main__':
    app.run(debug=True)
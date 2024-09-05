READ ME
pip install Flask
pip install opencv-python-headless
pip install pytesseract

Tesseract Setup:

Ensure that Tesseract is installed on your system and that the path to the Tesseract executable is correctly set (pytesseract.pytesseract.tesseract_cmd).

Running the Flask App:

To start the Flask application, run the script:

"python your_script_name.py"

The application will run on http://127.0.0.1:5000/ by default. You can upload images via the /upload endpoint using a POST request.
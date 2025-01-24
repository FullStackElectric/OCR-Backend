from flask import Flask, request, jsonify
from flask_cors import CORS
import easyocr
import os
app = application
application = Flask(__name__)
CORS(application)  # Enable CORS for the React Native app

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'])

@application.route('/ocr')
def ocr():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image = request.files['image']
    image_path = os.path.join('/tmp', image.filename)
    image.save(image_path)

    # Process the image with EasyOCR
    try:
        result = reader.readtext(image_path)
        extracted_text = ' '.join([text[1] for text in result])
        return jsonify({'text': extracted_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(image_path)

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)

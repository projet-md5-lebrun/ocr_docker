"""
OCR and Text-to-Speech Flask application using EasyOCR and gTTS.
"""

import io
import base64
from flask import Flask, render_template, request
import cv2
import numpy as np
import easyocr
from gtts import gTTS


app = Flask(__name__)

reader = easyocr.Reader(['fr'])


def easyocr_text(img):
    """
    Extract text from an image using EasyOCR.
    :param img: image
    :return: list of texts
    """
    results = reader.readtext(img)
    return results

def text_to_speech(text):
    """
    Convert text to speech using gTTS.
    :param text: text
    :return: BytesIO audio stream
    """
    try:
        tts = gTTS(text=text, lang='fr')
        audio_stream = io.BytesIO()
        tts.write_to_fp(audio_stream)
        audio_stream.seek(0)
        return audio_stream
    except SpecificException as e:
        print(f"Error: {e}")
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    texts = None
    audio_stream = None

    if request.method == 'POST':
        file = request.files['image']

        if file:
            image = cv2.imdecode(
                np.frombuffer(
                    file.read(),
                    np.uint8),
                cv2.IMREAD_COLOR)
            results = easyocr_text(image)

            # Extract the texts from results
            texts = [result[1] for result in results]
            # Concatenate all texts
            texts = ' '.join(texts)
            audio_stream = text_to_speech(texts)

            if audio_stream:
                audio_encoded = base64.b64encode(
                    audio_stream.read()).decode('utf-8')
                return render_template(
                    'index.html',
                    results=results,
                    texts=texts,
                    audio_stream=audio_encoded)

    return render_template(
        'index.html',
        results=results,
        texts=texts,
        audio_stream=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

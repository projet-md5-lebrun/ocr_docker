import os
import io
import base64
from flask import Flask, render_template, request
import cv2
import numpy as np
import pytesseract
from gtts import gTTS
from transformers import pipeline

summarizer = pipeline("summarization", model="Falconsai/text_summarization")

app = Flask(__name__)

# Set the TESSDATA_PREFIX environment variable


def ocr_text(image_data):
    try:
        results = pytesseract.image_to_string(image_data, lang='eng')
        return results
    except Exception as e:
        print(f"Error in OCR: {e}")
        return None


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
    summary = None

    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename != '':
            # Read image data from the file
            image_data = cv2.imdecode(
                np.frombuffer(
                    file.read(),
                    np.uint8),
                cv2.IMREAD_UNCHANGED)
            results = ocr_text(image_data)

            if results:
                texts = [result.strip() for result in results.split('\n')]
                texts = ' '.join(texts)
                summaries = summarizer(
                    results,
                    max_length=1300,
                    min_length=30,
                    do_sample=False)
                if summaries and 'summary_text' in summaries[0]:
                    summary = summaries[0]['summary_text']
                    audio_stream = text_to_speech(summary)

                if audio_stream:
                    audio_encoded = base64.b64encode(
                        audio_stream.read()).decode('utf-8')
                    return render_template(
                        'index.html',
                        results=results,
                        texts=texts,
                        summary=summary,
                        audio_stream=audio_encoded)

    return render_template(
        'index.html',
        texts=texts,
        summary=summary,
        audio_stream=None)


if __name__ == '__main__':
    app.run("0.0.0.0", port=80, debug=True)

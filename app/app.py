from flask import Flask, render_template, request, send_file
import cv2
import numpy as np
import easyocr
from gtts import gTTS
import os

app = Flask(__name__)

reader = easyocr.Reader(['fr'])


ocr_results = []

def easyocr_text(img):
    # Perform OCR on the image using EasyOCR
    results = reader.readtext(img)
    return results

def text_to_speech(text, filename='output.mp3'):
    
    tts = gTTS(text=text, lang='fr', slow=False)
    tts.save(filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    global ocr_results

    if request.method == 'POST':
        file = request.files['image']

        if file:
            # Read the uploaded image and decode it using OpenCV
            image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

            # Perform OCR on the image using EasyOCR
            ocr_results = easyocr_text(image)

            # Extract the texts from the results
            texts = [result[1] for result in ocr_results]

            return render_template('index.html', texts=texts, results=ocr_results)

    return render_template('index.html', texts=None, results=None)

@app.route('/text_to_speech', methods=['POST'])
def text_to_speech_route():
    global ocr_results

    if ocr_results:
        # Extract the first recognized text for text-to-speech
        all_text = '\n'.join(result[1] for result in ocr_results)
        
        # Convert concatenated text to speech
        text_to_speech(all_text)

        audio_path="output.mp3"

        #si on veut telecharger le fichier
        return send_file('output.mp3', as_attachment=True)

        #pour la lecture en playback pas besoin de telecharger le ficher
        #return render_template('index.html', texts=[all_text], results=ocr_results, audio_path=audio_path)

    return "No OCR results available."

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')

from flask import Flask, render_template, request
import cv2
import numpy as np
import easyocr
import os
app = Flask(__name__)

reader = easyocr.Reader(['en'])  

def easyocr_text(img):
    results = reader.readtext(img)
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    texts = None

    if request.method == 'POST':
        file = request.files['image']

        if file:
            image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
            results = easyocr_text(image)

            # Extract the texts from results
            texts = [result[1] for result in results]
            # concat all texts
            texts = ' '.join(texts)
            print(texts)

    return render_template('index.html', results=results, texts=texts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

from flask import Flask, render_template, request
import cv2
import numpy as np
import easyocr
import os

app = Flask(__name__)

reader = easyocr.Reader(['en'])  # Cette ligne doit être exécutée une seule fois pour charger le modèle en mémoire

def easyocr_text(img):
     results = reader.readtext(img)
     return results

@app.route('/', methods=['GET', 'POST'])
def index():
     if request.method == 'POST':
         file = request.files['image']

         if file:
             image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
             results = easyocr_text(image)

             # Extract the texts from results
             texts = [result[1] for result in results]

             return render_template('index.html', results=results, image_path="your_image.jpg", texts=texts)

     return render_template('index.html', results=None, image_path=None, texts=None)

if __name__ == '__main__':
     app.run(debug=True, port=5001 , host='0.0.0.0' )
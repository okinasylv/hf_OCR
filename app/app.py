from flask import Flask, request, send_from_directory
import pytesseract
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/health")
def health():
    return "OK"

@app.route("/")
def home():
    return '''
    <h2>OCR Web App</h2>
    <form method="POST" action="/upload" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <input type="submit" value="Feltöltés">
    </form>
    '''

@app.route("/upload", methods=["POST"])
def ocr():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        image = Image.open(filepath)

data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

draw = ImageDraw.Draw(image)

n_boxes = len(data['text'])

for i in range(n_boxes):
    try:
        conf = float(data['conf'][i])
    except:
        conf = 0

    if conf > 60:
        x = data['left'][i]
        y = data['top'][i]
        w = data['width'][i]
        h = data['height'][i]

        draw.rectangle([x, y, x+w, y+h], outline="green", width=2)

        boxed_path = os.path.join(UPLOAD_FOLDER, "boxed_" + file.filename)
        image.save(boxed_path)

        text = pytesseract.image_to_string(image)
    except Exception as e:
        return f"OCR error: {str(e)}"

    return f"""
    <h3>Szöveg:</h3>
    <pre>{text}</pre>

    <h3>Kép:</h3>
    <img src="/image/{os.path.basename(boxed_path)}" width="500">

    <br><a href="/">Vissza</a>
    """

@app.route('/image/<filename>')
def get_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
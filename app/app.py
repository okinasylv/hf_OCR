from flask import Flask, request, render_template_string
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
def upload():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        text = pytesseract.image_to_string(Image.open(filepath))
    except Exception as e:
        return f"OCR error: {str(e)}"

    return f"""
    <h3>Felismert szöveg:</h3>
    <pre>{text}</pre>
    <br>
    <a href="/">Vissza</a>
    """

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
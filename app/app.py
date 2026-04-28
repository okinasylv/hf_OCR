from flask import Flask, request, send_from_directory
import pytesseract
from PIL import Image, ImageDraw
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
    <h2>Pytesseract Keretező</h2>
    <form method="POST" action="/upload" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <input type="submit" value="Feltöltés">
    </form>
    '''

@app.route("/upload", methods=["POST"])
def ocr():
    if 'file' not in request.files: return "Nincs fájl"
    file = request.files['file']
    if file.filename == '': return "Nincs kiválasztott fájl"

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        image = Image.open(filepath).convert("RGB")
        draw = ImageDraw.Draw(image)

        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

        n_boxes = len(data['level'])
        for i in range(n_boxes):
            text = data['text'][i].strip()
            conf = int(data['conf'][i])

            if conf > 40 and len(text) > 0:
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                
       
                padding = 2
                draw.rectangle(
                    [x - padding, y - padding, x + w + padding, y + h + padding],
                    outline="red", 
                    width=3
                )

        boxed_filename = "boxed_" + file.filename
        boxed_path = os.path.join(UPLOAD_FOLDER, boxed_filename)
        image.save(boxed_path)

        full_text = pytesseract.image_to_string(image)

    except Exception as e:
        return f"OCR hiba: {str(e)}"

    return f"""
    <h3>Felismert szöveg:</h3>
    <pre style="background: #eee; padding: 10px;">{full_text}</pre>
    <h3>Keretezett eredmény:</h3>
    <img src="/image/{boxed_filename}" width="800">
    <br><a href="/">Vissza</a>
    """

@app.route('/image/<filename>')
def get_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
from flask import Flask, request, send_file
from pdf2image import convert_from_bytes
import zipfile
import io

app = Flask(__name__)

@app.route('/')
def home():
    return "PDF to JPG API is working!"

@app.route('/pdf-to-jpg', methods=['POST'])
def pdf_to_jpg():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    images = convert_from_bytes(file.read(), dpi=200)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for i, image in enumerate(images):
            img_io = io.BytesIO()
            image.save(img_io, format='JPEG')
            img_io.seek(0)
            zip_file.writestr(f'page_{i+1}.jpg', img_io.read())

    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='converted_images.zip'
    )

import os
import subprocess

from flask import Flask, flash, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.relpath('./assets')
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return 'Hello, world!'

@app.route('/send_pdf', methods=['GET', 'POST'])
def send_pdf():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            txt_location = os.path.join(app.config['UPLOAD_FOLDER'], "text.txt")
            location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(location)
            subprocess.run(["ocrmypdf", "--sidecar", txt_location, location, location])
            return redirect(url_for('uploaded_file'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploaded_file')
def uploaded_file():
    text = ''
    txt_file = os.path.join(app.config['UPLOAD_FOLDER'], "text.txt")
    with open(txt_file) as f:
        text = f.read()

    return jsonify({'raw_text': text})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
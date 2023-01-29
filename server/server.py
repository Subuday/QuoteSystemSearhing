import os
import pytesseract
from flask import Flask, jsonify, request, url_for, flash, redirect
from werkzeug.utils import secure_filename
from elasticsearch import Elasticsearch
from flask_cors import CORS, cross_origin

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

UPLOAD_FOLDER = '/home/idykyi/programming/quote-sercher/server/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

es = Elasticsearch(hosts=[{'host': "localhost", 'port': 9200, "scheme": "http"}])

app = Flask(__name__)
cors = CORS(app)
app.secret_key = 'super secret key'
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_TYPE'] = 'filesystem'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def find_quote_in_db(text):
    resp = es.search(index="bible-3", query={"match": {"text": text}}, highlight={"fields": {"text": {"type": "plain"}}})
    results = map(lambda hit: {"source": hit['_source'], "highlight": hit["highlight"]}, resp['hits']['hits'][:3])
    return list(results)


@app.route('/quote', methods=['GET', 'POST'])
@cross_origin()
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path = app.config['UPLOAD_FOLDER'] + "/" + filename
            text = " ".join(pytesseract.image_to_string(file_path).split())
            print(text)
            return jsonify({'chapters': find_quote_in_db(text)})


if __name__ == '__main__':
    app.run()

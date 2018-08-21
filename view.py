import os
import time
from flask import Flask, jsonify, request, render_template, send_from_directory
from utils import tf_predict

from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()

app = Flask(__name__)
app.config.update(DEBUG=False)

SRC_DIR = './data/sources'
TMP_DIR = './data/results'
DST_DIR = './data/labels'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'])


def check_format(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/")
def test():
    return render_template("index.html")


@app.route("/api/predict", methods=["POST", "GET"])
def predict():
    if request.method == "POST":
        image_name = request.form.get("image_name", "null")
        image_path = os.path.join(SRC_DIR, image_name)
        mask_path = image_path.replace('sources', 'results').replace('jpg', 'png')
        res = tf_predict(image_path, mask_path)
        return jsonify(res)
    else:
        return render_template("index.html")


@app.route('/api/getlist', methods=["POST", "GET"])
def getlist():
    """Note: this interface is irrelevant to TF serving, just an extra task for me.
    """
    if request.method == "POST":
        res = {'status': 0, 'files': []}
        lines = []
        for root, dirs, files in os.walk(SRC_DIR):
            level = root.replace(SRC_DIR, '').count(os.sep)
            indent = '-' * 2 * level
            lines.append('{}{}/'.format(indent, os.path.basename(root)) + '\n')
            # fileSave.write('{}{}/'.format(indent, os.path.abspath(root)) + '\n')
            sub_indent = '-' * 2 * (level + 1)
            for f in files:
                # fileSave.write('{}{}'.format(subIndent, f) + '\n')
                lines.append('{}{}'.format(sub_indent, f) + '\n')
        res['files'] = lines
        return jsonify(res)
    else:
        return render_template("index.html")


@app.route('/api/upload', methods=["POST"])
def upload():
    file = request.files.get('image_name')
    if not check_format(file.filename):
        return jsonify({'status': 101})

    path = os.path.join(DST_DIR, file.filename)
    if os.path.exists(path):
        return jsonify({'status': 102})

    try:
        file.save(path)
    except:
        return jsonify({'status': 103})
    else:
        return jsonify({'status': 0})


@app.route('/api/download/<path:filename>', methods=["POST", "GET"])
def download(filename):
    if request.method == "GET":
        path = ''
        split, name = filename.strip().split('_')
        if split == 'src':
            path = SRC_DIR
        elif split == 'res':
            path = TMP_DIR
        print(path)
        return send_from_directory(path, name, as_attachment=True)
    else:
        return render_template("index.html")


@app.route('/async', methods=["GET"])
def test_async_one():
    print("ASYN haa a request.")
    time.sleep(10)
    return 'hello asyn'


@app.route('/test/', methods=['GET'])
def tests():
    return 'hello test'


@app.before_first_request
def before_first_request():
    print("init done!")


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000, debug=True)
    http_server = WSGIServer(('', 8080), app)
    http_server.serve_forever()

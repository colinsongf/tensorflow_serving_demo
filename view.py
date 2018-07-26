from flask import Flask, jsonify, request, render_template
from utils import tf_predict, get_list, uploads, downloads

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def tfpredict():
    if request.method == "POST":
        image_name = request.form.get("image_name", "null")
        res = tf_predict(str(image_name))
        return jsonify(res)
    else:
        return render_template("index.html")


@app.route('/list', methods=["POST", "GET"])
def getlist():
    """Note: this interface is irrelevant to TF serving, just an extra task for me.
    """
    if request.method == "POST":
        res = get_list()
        return jsonify(res)
    else:
        return render_template("index.html")


@app.route('/upload', methods=["POST"])
def upload():
    f = request.files.get('image_name')
    return uploads(f)


@app.route('/download/<path:filename>', methods=["POST", "GET"])
def download(filename):
    if request.method == "GET":
        return downloads(filename)


@app.before_first_request
def before_first_request():
    print("init done!")


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=False
    ) 
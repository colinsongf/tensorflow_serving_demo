from flask import Flask, jsonify, request, render_template
import json
import TFRequest

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        image_name = request.form.get("image_name", "null")
        res = TFRequest.tf_predict(str(image_name))
        return jsonify(res)
    else:
        return render_template("index.html")


@app.route('/list', methods=["POST", "GET"])
def test():
    """Note: this interface is irrelevant to TF serving, just an extra task for me.
    """
    if request.method == "POST":
        res = TFRequest.get_list()
        return jsonify(res)
    else:
        return render_template("index.html")


@app.before_first_request
def before_first_request():
    print("init done!")


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=True
    ) 
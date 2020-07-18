from flask import *
from flask import render_template
from flask import Flask
from flask import send_file
from flask import request, redirect
from flask import Markup
from flask import send_from_directory
import os
from werkzeug.utils import secure_filename
import pandas as pd
from tpot_exporter import tpot_run
app = Flask(__name__)

data_files_path = os.getcwd()+"\\FYP\\static\\files\\datasets\\"

app.config["UPLOAD_PATH"] = data_files_path
app.config["ALLOWED_EXTENSIONS"] = "CSV"

#result = ''

df = pd.DataFrame()


def allowed_files(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False


@app.route("/")
def getstarted(methods=['POST', 'GET']):

    print("HOME PAGE")

    return render_template("Home.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    print("upload called")
    if request.method == "POST":

        if request.files:

            dataset = request.files["dataset"]
            target_col_name = request.form['target']

            if dataset.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_files(dataset.filename):
                filename = secure_filename(dataset.filename)

                dataset.save(os.path.join(app.config["UPLOAD_PATH"], filename))

                print("Dataset Saved")

                df = pd.read_csv(os.path.join(
                    app.config["UPLOAD_PATH"], filename))
                tpot_run(df, target_col_name)

                return redirect(request.url)
            else:
                print("That file extension is not allowed")
                return redirect(request.url)

    # return send_from_directory(data_files_path, 'pipeline.py')
    return send_from_directory(data_files_path, 'pipeline.py')


if __name__ == "__main__":
    app.run(port=5000, debug=True)

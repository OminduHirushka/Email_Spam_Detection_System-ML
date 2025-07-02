from flask import Flask, request, render_template
import pickle
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

pipe = pickle.load(open("model.pkl", "rb"))


@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        email_content = request.form["email"]
        prediction = pipe.predict([email_content])[0]
        return render_template("index.html", prediction=prediction)

    return render_template("index.html", prediction=None)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded", 400

        file = request.files["file"]
        if file.filename == "":
            return "No file selected", 400

        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            with open(filepath, "r", encoding="utf-8") as f:
                email_text = f.read()

            prediction = pipe.predict([email_text])[0]
            return render_template(
                "index.html", prediction=prediction, email=email_text
            )

    return render_template("index.html", prediction=None)


if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])

    app.run(debug=True)

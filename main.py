from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

pipe = pickle.load(open("model.pkl", "rb"))


@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        email_content = request.form["email"]
        prediction = pipe.predict([email_content])[0]
        return render_template("index.html", prediction=prediction)

    return render_template("index.html", prediction=None)

if __name__ == "__main__":
    app.run(debug=True)

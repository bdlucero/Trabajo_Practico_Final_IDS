
from flask import Flask, render_template, redirect, url_for
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:5001")

@app.route("/")
def home():
    return redirect(url_for("buscar"))

@app.route("/buscar")
def buscar():

    materias = []  # sin datos hardcodeados
    return render_template("busqueda.html",
                           materias=materias,
                           backend_url=BACKEND_URL)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

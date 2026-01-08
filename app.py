from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    hasil = ""
    pilihan_user = ""
    pilihan_bot = ""

    if request.method == "POST":
        pilihan_user = request.form["pilihan"]
        pilihan_bot = random.choice(["batu", "gunting", "kertas"])

        if pilihan_user == pilihan_bot:
            hasil = "Seri!"
        elif (
            (pilihan_user == "batu" and pilihan_bot == "gunting") or
            (pilihan_user == "gunting" and pilihan_bot == "kertas") or
            (pilihan_user == "kertas" and pilihan_bot == "batu")
        ):
            hasil = "Kamu Menang!"
        else:
            hasil = "Kamu Kalah!"

    return render_template(
        "index.html",
        hasil=hasil,
        pilihan_user=pilihan_user,
        pilihan_bot=pilihan_bot
    )

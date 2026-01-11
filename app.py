from flask import Flask, render_template, request, redirect, session, url_for
import random

app = Flask(__name__)
app.secret_key = "rahasia-super-aman"

# ----------------------------
# USER DUMMY
# ----------------------------
USERS = {
    "admin": {"password": "admin", "role": "admin"},
    "player": {"password": "123", "role": "player"},
    "guest": {"password": "guest", "role": "guest"},
}

# SIMPAN SKOR PLAYER (SEMENTARA DI MEMORY)
LEADERBOARD = {}

# ----------------------------
# HELPER
# ----------------------------
def reset_game():
    session["ronde"] = 0
    session["skor_player"] = 0
    session["skor_bot"] = 0

# ----------------------------
# LOGIN
# ----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username in USERS and USERS[username]["password"] == password:
            session["username"] = username
            session["role"] = USERS[username]["role"]
            reset_game()

            if session["role"] == "admin":
                return redirect("/admin")
            elif session["role"] == "player":
                return redirect("/game")
            elif session["role"] == "guest":
                return redirect("/guest")

        else:
            return render_template("index.html", error="Username atau password salah!")

    return render_template("index.html")

# ----------------------------
# GAME (PLAYER)
# ----------------------------
@app.route("/game", methods=["GET", "POST"])
def game():
    if "username" not in session or session.get("role") != "player":
        return redirect("/")

    username = session["username"]

    if "ronde" not in session:
        reset_game()

    result = None
    player_choice = None
    bot_choice = None

    if request.method == "POST":
        player_choice = request.form.get("choice")
        bot_choice = random.choice(["batu", "gunting", "kertas"])

        session["ronde"] += 1

        if player_choice == bot_choice:
            result = "Seri!"
        elif (
            (player_choice == "batu" and bot_choice == "gunting") or
            (player_choice == "gunting" and bot_choice == "kertas") or
            (player_choice == "kertas" and bot_choice == "batu")
        ):
            session["skor_player"] += 1
            result = "Kamu MENANG ronde ini!"
        else:
            session["skor_bot"] += 1
            result = "Kamu KALAH ronde ini!"

        # =========================
        # JIKA SUDAH 3 RONDE
        # =========================
        if session["ronde"] >= 3:

            # Pastikan user ada di leaderboard
            if username not in LEADERBOARD:
                LEADERBOARD[username] = {"win": 0, "lose": 0, "draw": 0}

            # Tentukan pemenang match
            if session["skor_player"] > session["skor_bot"]:
                LEADERBOARD[username]["win"] += 1
                result = "🏆 KAMU MENANG MATCH!"
            elif session["skor_player"] < session["skor_bot"]:
                LEADERBOARD[username]["lose"] += 1
                result = "💀 KAMU KALAH MATCH!"
            else:
                LEADERBOARD[username]["draw"] += 1
                result = "🤝 MATCH SERI!"

            # Reset game setelah match selesai
            reset_game()

    return render_template(
        "game.html",
        ronde=session["ronde"],
        skor_player=session["skor_player"],
        skor_bot=session["skor_bot"],
        result=result,
        player=player_choice,
        bot=bot_choice
    )


# ----------------------------
# ADMIN
# ----------------------------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "username" not in session or session.get("role") != "admin":
        return redirect("/")

    global LEADERBOARD

    if request.method == "POST":
        # Tombol reset ditekan
        LEADERBOARD = {}

    return render_template("admin.html", leaderboard=LEADERBOARD)


# ----------------------------
# GUEST
# ----------------------------
@app.route("/guest")
def guest():
    if "username" not in session or session.get("role") != "guest":
        return redirect("/")
    return render_template("guest.html", leaderboard=LEADERBOARD)

# ----------------------------
# LOGOUT
# ----------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ----------------------------
# RUN
# ----------------------------
if __name__ == "__main__":
    app.run()

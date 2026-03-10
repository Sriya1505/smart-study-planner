from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():

    if "user" not in session:
        return redirect("/login")

    db = get_db()
    tasks = db.execute("SELECT * FROM tasks WHERE user=?", (session["user"],)).fetchall()

    return render_template("index.html", tasks=tasks)


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        db.execute("INSERT INTO users VALUES (?,?)", (username, password))
        db.commit()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password),
        ).fetchone()

        if user:
            session["user"] = username
            return redirect("/")

    return render_template("login.html")


@app.route("/add", methods=["POST"])
def add():

    task = request.form["task"]
    date = request.form["date"]

    db = get_db()
    db.execute(
        "INSERT INTO tasks (user,task,date) VALUES (?,?,?)",
        (session["user"], task, date),
    )
    db.commit()

    return redirect("/")


@app.route("/delete/<id>")
def delete(id):

    db = get_db()
    db.execute("DELETE FROM tasks WHERE id=?", (id,))
    db.commit()

    return redirect("/")


@app.route("/logout")
def logout():

    session.pop("user")
    return redirect("/login")


app.run(debug=True)
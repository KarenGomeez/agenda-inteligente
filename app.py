from flask import Flask, render_template, redirect, request, session
from database import *

app = Flask(__name__)
app.secret_key = "secreto123"

create_tables()


# 🔐 LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = get_user(username, password)

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect("/")

    return render_template("login.html")


# 📝 REGISTER REAL
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        success = create_user(username, password)

        if success:
            return redirect("/login")

    return render_template("register.html")


# 🚪 LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# 🧠 HOME
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    tasks = get_tasks(user_id)

    categories = list(set([t["category"] for t in tasks if t["category"]]))

    total = len(tasks)
    completed = len([t for t in tasks if t["status"] == "completada"])
    pending = len([t for t in tasks if t["status"] == "pendiente"])

    progress = int((completed / total) * 100) if total > 0 else 0

    return render_template(
        "index.html",
        tasks=tasks,
        categories=categories,
        progress=progress
    )


# ➕ ADD
@app.route("/add", methods=["POST"])
def add():
    user_id = session["user_id"]

    title = request.form["title"]
    category = request.form["category"]
    priority = request.form["priority"]

    add_task(user_id, title, "", category, "task", priority)

    return redirect("/")


# ✔ COMPLETE
@app.route("/complete/<int:id>")
def complete(id):
    complete_task(id)
    return redirect("/")


# 🗑 DELETE
@app.route("/delete/<int:id>")
def delete(id):
    delete_task(id)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

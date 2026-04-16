from flask import Flask, render_template, redirect, request, session
from database import *

app = Flask(__name__)
app.secret_key = "secret123"

create_tables()


# 🔐 LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = get_user(request.form["username"], request.form["password"])

        if user:
            session["user_id"] = user[0]
            return redirect("/")
    
    return render_template("login.html")


# 📝 REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        create_user(request.form["username"], request.form["password"])
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

    categories = list(set([t[3] for t in tasks]))

    total = len(tasks)
    completed = len([t for t in tasks if t[5] == "completada"])
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
    if "user_id" not in session:
        return redirect("/login")

    add_task(
        session["user_id"],
        request.form["title"],
        request.form["category"],
        request.form["priority"]
    )

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

from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from database import (
    get_tasks,
    create_tables,
    create_user_table,
    add_task,
    complete_task,
    delete_task,
    auto_priority,
    get_connection
)

app = Flask(__name__)
app.secret_key = "secreto"

# 🔥 DB
create_tables()
create_user_table()

# 🔐 LOGIN CONFIG
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


# 🧠 HOME (SOLO USUARIO LOGUEADO)
@app.route("/")
@login_required
def home():
    tasks = get_tasks(current_user.id)

    categories = list(set([t[4] for t in tasks if t[4]]))

    total = len(tasks)
    completed = len([t for t in tasks if t[8] == "completada"])

    progress = int((completed / total) * 100) if total > 0 else 0

    return render_template(
        "index.html",
        tasks=tasks,
        categories=categories,
        progress=progress
    )


# ➕ AGREGAR
@app.route("/add", methods=["POST"])
@login_required
def add():
    title = request.form["title"]
    category = request.form["category"]
    priority = request.form["priority"]

    if not priority:
        priority = auto_priority(title, category)

    add_task(current_user.id, title, "", category, "task", priority)
    return redirect("/")


# ✔ COMPLETAR
@app.route("/complete/<int:id>")
@login_required
def complete(id):
    complete_task(id, current_user.id)
    return redirect("/")


# 🗑 ELIMINAR
@app.route("/delete/<int:id>")
@login_required
def delete(id):
    delete_task(id, current_user.id)
    return redirect("/")


# 🔐 LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            login_user(User(user[0]))
            return redirect("/")

    return render_template("login.html")


# 📝 REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# 🚪 LOGOUT
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)

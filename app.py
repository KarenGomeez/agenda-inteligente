from flask import Flask, render_template, redirect, request
from database import (
    get_tasks,
    create_tables,
    add_task,
    complete_task,
    delete_task,
    auto_priority
)

import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__, template_folder="templates")

create_tables()


# 🧠 HOME
@app.route("/")
def home():
    filter_type = request.args.get("filter")
    tasks = get_tasks()

    categories_db = [t[3] for t in tasks if t[3]]
    default_categories = ["Trabajo", "Estudio", "Personal", "Finanzas"]

    categories = default_categories.copy()
    for c in categories_db:
        if c not in categories:
            categories.append(c)

    total = len(tasks)
    completed = len([t for t in tasks if t[7] == "completada"])
    pending = len([t for t in tasks if t[7] == "pendiente"])
    urgent = len([t for t in tasks if t[5] == "urgente"])

    progress = int((completed / total) * 100) if total > 0 else 0

    return render_template(
        "index.html",
        tasks=tasks,
        total=total,
        completed=completed,
        pending=pending,
        urgent=urgent,
        progress=progress,
        categories=categories
    )


# ➕ AGREGAR (con prioridad manual o IA)
@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    category = request.form["category"].strip().capitalize()

    # 🔥 PRIORIDAD
    priority = request.form.get("priority")

    if not priority or priority == "auto":
        priority = auto_priority(title, category)

    add_task(title, "", category, "task", priority)
    return redirect("/")


# ✔ COMPLETAR
@app.route("/complete/<int:task_id>")
def complete(task_id):
    complete_task(task_id)
    return redirect("/")


# 🗑 ELIMINAR
@app.route("/delete/<int:task_id>")
def delete(task_id):
    delete_task(task_id)
    return redirect("/")


# ✏️ EDITAR
@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit(task_id):
    tasks = get_tasks()
    task = next((t for t in tasks if t[0] == task_id), None)

    if not task:
        return redirect("/")

    if request.method == "POST":
        title = request.form["title"]
        category = request.form["category"].strip().capitalize()
        priority = request.form["priority"]

        delete_task(task_id)
        add_task(title, "", category, "task", priority)

        return redirect("/")

    return render_template("edit.html", task=task)


# 📊 CHART
@app.route("/chart")
def chart():
    tasks = get_tasks()

    completed = len([t for t in tasks if t[7] == "completada"])
    pending = len([t for t in tasks if t[7] == "pendiente"])

    labels = ["Completadas", "Pendientes"]
    values = [completed, pending]

    plt.figure()
    plt.bar(labels, values)
    plt.title("Productividad")

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)

    graph_url = base64.b64encode(img.getvalue()).decode()

    return f"""
    <h2>📊 Dashboard</h2>
    <img src="data:image/png;base64,{graph_url}">
    <br><a href="/">Volver</a>
    """


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

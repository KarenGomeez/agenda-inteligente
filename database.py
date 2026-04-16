import sqlite3
from datetime import datetime

DB_NAME = "agenda.db"

def get_connection():
    return sqlite3.connect(DB_NAME)


# 👤 USERS
def create_user_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


# 📋 TASKS (con user_id)
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        description TEXT,
        category TEXT,
        task_type TEXT,
        priority TEXT,
        due_date TEXT,
        status TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_task(user_id, title, description="", category="general", task_type="task", priority="media"):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tasks (
        user_id, title, description, category, task_type,
        priority, due_date, status, created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        title,
        description,
        category,
        task_type,
        priority,
        None,
        "pendiente",
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_tasks(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM tasks
    WHERE user_id = ?
    ORDER BY id DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows


def complete_task(task_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE tasks
    SET status = 'completada'
    WHERE id = ? AND user_id = ?
    """, (task_id, user_id))

    conn.commit()
    conn.close()


def delete_task(task_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM tasks
    WHERE id = ? AND user_id = ?
    """, (task_id, user_id))

    conn.commit()
    conn.close()


def auto_priority(title, category):
    text = (title + " " + category).lower()

    if "urgente" in text or "hoy" in text:
        return "urgente"
    if "estudio" in text or "trabajo" in text:
        return "alta"

    return "media"

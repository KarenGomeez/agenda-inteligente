import sqlite3
from datetime import datetime

DB_NAME = "agenda.db"

def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # 👤 USERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # 📋 TASKS (con user_id)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        category TEXT,
        priority TEXT,
        status TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


# 🔐 USERS
def create_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()


def get_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user


# 📋 TASKS
def add_task(user_id, title, category, priority):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tasks (user_id, title, category, priority, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        title,
        category,
        priority,
        "pendiente",
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_tasks(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE user_id=?", (user_id,))
    rows = cursor.fetchall()

    conn.close()
    return rows


def complete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE tasks SET status='completada' WHERE id=?", (task_id,))
    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

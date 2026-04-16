import sqlite3
from datetime import datetime

DB_NAME = "agenda.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
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


def add_task(title, description="", category="general", task_type="task", priority="media", due_date=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tasks (
        title, description, category, task_type,
        priority, due_date, status, created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        description,
        category,
        task_type,
        priority,
        due_date,
        "pendiente",
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM tasks
    ORDER BY 
        CASE status
            WHEN 'pendiente' THEN 1
            WHEN 'completada' THEN 2
        END,
        CASE priority
            WHEN 'urgente' THEN 1
            WHEN 'alta' THEN 2
            WHEN 'media' THEN 3
            WHEN 'baja' THEN 4
        END,
        id DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows

def tasks_exist():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    conn.close()
    return count > 0

def complete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE tasks
    SET status = 'completada'
    WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM tasks
    WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()

def auto_priority(title, category):
    text = (title + " " + category).lower()

    if any(word in text for word in ["pagar", "factura", "deuda", "urgente", "hoy"]):
        return "urgente"

    if any(word in text for word in ["estudiar", "curso", "examen", "python", "trabajo"]):
        return "alta"

    if any(word in text for word in ["idea", "proyecto", "app", "desarrollo"]):
        return "media"

    return "baja"
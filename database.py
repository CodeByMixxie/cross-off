import sqlite3

DB_NAME = "tasks.db"

def connect():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = connect()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            completed INTEGER NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def add_task_db(text):
    conn = connect()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO tasks (text, completed) VALUES (?, ?)", (text, 0))
    
    conn.commit()
    conn.close()

def get_tasks():
    conn = connect()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, text, completed FROM tasks")
    tasks = cursor.fetchall()
    
    conn.close()
    return tasks

def update_task_status(task_id, completed):
    conn = connect()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))
    
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = connect()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    
    conn.commit()
    conn.close()

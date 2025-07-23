import sqlite3
import os
import datetime

DB_NAME = 'assistant_data.db'

def connect_db():
    """Establishes a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def create_tables():
    """Creates necessary tables if they don't exist."""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Table for To-Do List
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    completed INTEGER DEFAULT 0
                )
            ''')
            # Table for Notes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # Table for Reminders
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message TEXT NOT NULL,
                    reminder_time TEXT NOT NULL, -- Stored as ISO format string
                    is_set INTEGER DEFAULT 0
                )
            ''')
            conn.commit()
            print("Database tables created/checked successfully.")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
        finally:
            conn.close()

# --- To-Do List Functions ---
def add_todo(task):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO todos (task) VALUES (?)", (task,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding todo: {e}")
            return False
        finally:
            conn.close()

def get_all_todos():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, task, completed FROM todos ORDER BY id DESC")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching todos: {e}")
            return []
        finally:
            conn.close()

def mark_todo_complete(todo_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE todos SET completed = 1 WHERE id = ?", (todo_id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error marking todo complete: {e}")
            return False
        finally:
            conn.close()

# --- Notes Functions ---
def add_note(content):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding note: {e}")
            return False
        finally:
            conn.close()

def get_last_note():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT content FROM notes ORDER BY id DESC LIMIT 1")
            result = cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Error fetching last note: {e}")
            return None
        finally:
            conn.close()

# --- Reminders Functions ---
def add_reminder(message, reminder_time):
    """
    Adds a reminder to the database.
    reminder_time should be a string in ISO format (e.g., 'YYYY-MM-DD HH:MM:SS').
    """
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO reminders (message, reminder_time) VALUES (?, ?)", (message, reminder_time))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding reminder: {e}")
            return False
        finally:
            conn.close()

def get_pending_reminders():
    """Fetches reminders that are due and not yet marked as set."""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Select reminders that are due now or in the past, and are not yet set
            cursor.execute("SELECT id, message, reminder_time FROM reminders WHERE reminder_time <= ? AND is_set = 0", (datetime.datetime.now().isoformat(sep=' ', timespec='seconds'),))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching pending reminders: {e}")
            return []
        finally:
            conn.close()

def mark_reminder_set(reminder_id):
    """Marks a reminder as set/delivered."""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE reminders SET is_set = 1 WHERE id = ?", (reminder_id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error marking reminder set: {e}")
            return False
        finally:
            conn.close()


# Initialize database when this module is imported
create_tables()
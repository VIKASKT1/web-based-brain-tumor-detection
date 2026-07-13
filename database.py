# database.py
import os
import mysql.connector
from flask import session
import bcrypt

# --- Database Connection ---
def get_connection():
    ssl_disabled = os.environ.get('DB_SSL_DISABLED', 'False') == 'True'
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=int(os.environ.get('DB_PORT', 3306)),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', ''),
        database=os.environ.get('DB_NAME', 'braintumor'),
        ssl_disabled=ssl_disabled
    )

# --- Generic Query Handlers ---
def execute_select(query, params=None):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Select error: {e}")
        return []

def execute_insert(query, params):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Insert error: {e}")
        return str(e)

def execute_insert_return_id(query, params):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        insert_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return insert_id
    except Exception as e:
        print(f"Insert error: {e}")
        return None

def execute_update(query, params):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Update error: {e}")
        return False

def execute_delete(query, params):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        deleted = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return deleted
    except Exception as e:
        print(f"Delete error: {e}")
        return False


# --- Login Utilities ---
def check_login(query, email, password_input, role='user'):
    """
    role should be 'admin' or 'user' depending on which table/route is calling this.
    Sets session['role'] so login_required / admin_required can tell them apart.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
    except Exception as e:
        return False, f"Database error: {e}", "danger"

    if user:
        stored_pw = user['password']
        if isinstance(stored_pw, str):
            stored_pw = stored_pw.encode('utf-8')

        if bcrypt.checkpw(password_input.encode('utf-8'), stored_pw):
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['role'] = role
            return True, "Login Successful", "success"
        else:
            return False, "Invalid password", "danger"
    else:
        return False, "User not found", "danger"
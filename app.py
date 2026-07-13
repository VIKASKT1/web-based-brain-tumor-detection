import os
import uuid
from functools import wraps
from datetime import datetime

from flask import (
    Flask, jsonify, render_template, request, send_file,
    redirect, session, url_for, flash, make_response
)
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np

from database import (
    execute_select, execute_insert, execute_insert_return_id,
    execute_update, execute_delete, check_login
)
import bcrypt

server_timestamp = datetime.now().strftime("%Y%m%d")

app = Flask(__name__)

# --- Secret key from environment (falls back to a random key each restart if not set) ---
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))
app.config['SECRET_KEY'] = app.secret_key

# --- Upload limits ---
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB max upload

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --- Lazy model loading so app doesn't crash on startup if model file is missing ---
model = None

def get_model():
    global model
    if model is None:
        from keras.models import load_model
        model_path = os.path.join(BASE_DIR, 'model', 'brain_tumor_classifier_model.keras')
        model = load_model(model_path)
    return model


# --- Access control decorators ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or 'email' not in session:
            return redirect(url_for('login'))
        response = make_response(f(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            return redirect(url_for('login'))
        response = make_response(f(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    return decorated_function


# ===================== Public Routes =====================

@app.route('/')
def index():
    return render_template('Home.html')


@app.route('/about')
def about():
    return render_template('About.html')


@app.route('/contact')
def contact():
    return render_template('Contact.html')


@app.route('/login')
def login():
    return render_template('Login.html', active_tab="admin")


# ===================== Admin Auth =====================

@app.route('/admin-login', methods=['POST'])
def admin_login():
    email = request.form['admin_username']
    password = request.form['admin_password']

    query = "SELECT * FROM tbladmin WHERE email = %s"
    success, msg, msg_type = check_login(query, email, password, role='admin')

    if success:
        return redirect(url_for('admin_home'))
    else:
        return render_template('Login.html', msg=msg, msg_type=msg_type, active_tab="admin")


@app.route('/admin-home')
@admin_required
def admin_home():
    return render_template('Admin/AdminHome.html', msg="Welcome back, Admin!", msg_type="success")


# ===================== Admin: Users =====================

@app.route('/admin/users')
@admin_required
def admin_users():
    msg = request.args.get('msg')
    msg_type = request.args.get('msg_type', 'info')
    users = execute_select("SELECT * FROM tblusers")
    return render_template("Admin/AdminUsersList.html", users=users, msg=msg, msg_type=msg_type)


@app.route('/admin/edit-user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        mobile = request.form['mobile']
        query = "UPDATE tblusers SET username=%s, email=%s, mobile=%s WHERE id=%s"
        result = execute_update(query, (username, email, mobile, user_id))
        if result:
            return redirect(url_for('admin_users', msg="User updated successfully!", msg_type="success"))
        else:
            return redirect(url_for('admin_users', msg="Failed to update user.", msg_type="danger"))

    user = execute_select("SELECT * FROM tblusers WHERE id = %s", (user_id,))
    if user:
        return render_template("Admin/AdminUsersEdit.html", user=user[0])
    return redirect(url_for('admin_users', msg="User not found.", msg_type="warning"))


@app.route('/admin/delete-user/<int:user_id>')
@admin_required
def delete_user(user_id):
    success = execute_delete("DELETE FROM tblusers WHERE id = %s", (user_id,))
    if success:
        return redirect(url_for('admin_users', msg="User deleted successfully!", msg_type="success"))
    else:
        return redirect(url_for('admin_users', msg="Failed to delete user.", msg_type="danger"))


# ===================== Admin: FAQ =====================

@app.route('/admin/faq')
@admin_required
def admin_faq():
    msg = request.args.get('msg')
    msg_type = request.args.get('msg_type', 'info')
    faqs = execute_select("SELECT * FROM tblfaq")
    return render_template("Admin/AdminFAQList.html", faqs=faqs, msg=msg, msg_type=msg_type)


@app.route('/admin/add-faq', methods=['GET', 'POST'])
@admin_required
def add_faq():
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        result = execute_insert("INSERT INTO tblfaq (question, answer) VALUES (%s, %s)", (question, answer))
        if result is True:
            return redirect(url_for('admin_faq', msg="FAQ added successfully!", msg_type="success"))
        else:
            return redirect(url_for('admin_faq', msg="Failed to add FAQ.", msg_type="danger"))
    return render_template("Admin/AdminAddFAQ.html")


@app.route('/admin/edit-faq/<int:faq_id>', methods=['GET', 'POST'])
@admin_required
def edit_faq(faq_id):
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        result = execute_update("UPDATE tblfaq SET question=%s, answer=%s WHERE id=%s", (question, answer, faq_id))
        if result:
            return redirect(url_for('admin_faq', msg="FAQ updated successfully!", msg_type="success"))
        else:
            return redirect(url_for('admin_faq', msg="Failed to update FAQ.", msg_type="danger"))
    faq = execute_select("SELECT * FROM tblfaq WHERE id = %s", (faq_id,))
    if faq:
        return render_template("Admin/AdminEditFAQ.html", faq=faq[0])
    return redirect(url_for('admin_faq', msg="FAQ not found.", msg_type="warning"))


@app.route('/admin/delete-faq/<int:faq_id>')
@admin_required
def delete_faq(faq_id):
    success = execute_delete("DELETE FROM tblfaq WHERE id = %s", (faq_id,))
    if success:
        return redirect(url_for('admin_faq', msg="FAQ deleted successfully!", msg_type="success"))
    else:
        return redirect(url_for('admin_faq', msg="Failed to delete FAQ.", msg_type="danger"))


# ===================== Admin: Health Tips =====================

@app.route('/admin/health-tips')
@admin_required
def admin_health_tips():
    msg = request.args.get('msg')
    msg_type = request.args.get('msg_type', 'info')
    health_tips = execute_select("SELECT * FROM tblhealthtips ORDER BY id DESC")
    return render_template("Admin/AdminHealthTipsList.html", health_tips=health_tips, msg=msg, msg_type=msg_type)


@app.route('/admin/add-health-tip', methods=['GET', 'POST'])
@admin_required
def add_health_tip():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        query = "INSERT INTO tblhealthtips (title, description) VALUES (%s, %s)"
        result = execute_insert(query, (title, description))
        if result is True:
            return redirect(url_for('admin_health_tips', msg="Health tip added successfully!", msg_type="success"))
        else:
            return redirect(url_for('admin_health_tips', msg="Failed to add health tip.", msg_type="danger"))
    return render_template("Admin/AdminHealthTipForm.html", action="Add", health_tip=None)


@app.route('/admin/edit-health-tip/<int:tip_id>', methods=['GET', 'POST'])
@admin_required
def edit_health_tip(tip_id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        query = "UPDATE tblhealthtips SET title=%s, description=%s WHERE id=%s"
        result = execute_update(query, (title, description, tip_id))
        if result:
            return redirect(url_for('admin_health_tips', msg="Health tip updated successfully!", msg_type="success"))
        else:
            return redirect(url_for('admin_health_tips', msg="Failed to update health tip.", msg_type="danger"))

    tip = execute_select("SELECT * FROM tblhealthtips WHERE id = %s", (tip_id,))
    if tip:
        return render_template("Admin/AdminHealthTipForm.html", action="Edit", health_tip=tip[0])
    return redirect(url_for('admin_health_tips', msg="Health tip not found.", msg_type="warning"))


@app.route('/admin/delete-health-tip/<int:tip_id>')
@admin_required
def delete_health_tip(tip_id):
    success = execute_delete("DELETE FROM tblhealthtips WHERE id = %s", (tip_id,))
    if success:
        return redirect(url_for('admin_health_tips', msg="Health tip deleted successfully!", msg_type="success"))
    else:
        return redirect(url_for('admin_health_tips', msg="Failed to delete health tip.", msg_type="danger"))


@app.route('/adminlogout')
def adminlogout():
    session.clear()
    return redirect(url_for('login'))


# ===================== User Auth =====================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']

        user_check = execute_select("SELECT * FROM tblusers WHERE email = %s", (email,))
        if user_check and isinstance(user_check, list) and len(user_check) > 0:
            return render_template('Register.html', msg="Email already registered. Please login or use another email.", msg_type="danger")

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        insert_query = """
            INSERT INTO tblusers (username, email, mobile, password)
            VALUES (%s, %s, %s, %s)
        """
        result = execute_insert(insert_query, (username, email, mobile, hashed_pw))

        if result is True:
            return render_template('Login.html', msg="Registration successful! Please login.", msg_type="success", active_tab="user")
        else:
            return render_template('Register.html', msg="Error during registration. Please try again.", msg_type="danger")

    return render_template('Register.html')


@app.route('/user-login', methods=['POST'])
def user_login():
    email = request.form['user_username']
    password = request.form['user_password']

    query = "SELECT * FROM tblusers WHERE email = %s"
    success, msg, msg_type = check_login(query, email, password, role='user')

    if success:
        return redirect(url_for('user_dashboard'))
    else:
        return render_template('Login.html', msg=msg, msg_type=msg_type, active_tab="user")


@app.route('/user_dashboard')
@login_required
def user_dashboard():
    return render_template('User/UserHome.html', msg="Welcome back, User!", msg_type="success")


@app.route('/user/health-tips')
@login_required
def user_health_tips():
    health_tips = execute_select("SELECT * FROM tblhealthtips ORDER BY id DESC")
    return render_template('User/UserHealthTipsList.html', health_tips=health_tips)


@app.route('/user/faq')
@login_required
def user_faq():
    faqs = execute_select("SELECT * FROM tblfaq ORDER BY id DESC")
    return render_template('User/UserFAQList.html', faqs=faqs)


@app.route('/userlogout')
def userlogout():
    session.clear()
    return redirect(url_for('login'))


# ===================== Prediction =====================

@app.route('/user/prediction', methods=['GET', 'POST'])
@login_required
def user_prediction():
    if request.method == 'POST':
        try:
            file = request.files.get('image')
            if not file or file.filename == '':
                return render_template('User/UserPrediction.html', msg='No file selected.', msg_type='warning')

            if not allowed_file(file.filename):
                return render_template('User/UserPrediction.html', msg='Invalid file type. Use PNG or JPG.', msg_type='warning')

            try:
                clf = get_model()
            except Exception as e:
                print("Model load error:", e)
                return render_template('User/UserPrediction.html', msg='Model unavailable. Please try again later.', msg_type='danger')

            # Unique filename to prevent overwriting other users' uploads
            ext = secure_filename(file.filename).rsplit('.', 1)[-1].lower()
            filename = f"{uuid.uuid4()}.{ext}"
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(image_path)

            img = Image.open(image_path).convert('RGB').resize((128, 128))
            img_array = np.array(img) / 255.0
            img_array = img_array.reshape(1, 128, 128, 3)

            prediction = clf.predict(img_array)
            predicted_class = int(prediction[0][0] > 0.5)
            result = "No Tumor Detected" if predicted_class == 1 else "Tumor Detected"

            return render_template('User/UserPrediction.html',
                                    filename=filename,
                                    result=result,
                                    msg="Prediction complete.",
                                    msg_type="success")
        except Exception as e:
            print("Prediction error:", e)
            return render_template('User/UserPrediction.html', msg='Error during prediction.', msg_type='danger')

    return render_template('User/UserPrediction.html')


if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

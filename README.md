Good to flag — that changes some of the README's accuracy. Let me fix the DB references throughout to reflect TiDB instead of Aiven MySQL:

Good — TiDB Cloud (Serverless) is MySQL-compatible, so your `database.py`/`mysql-connector-python` setup already works with it as-is, since it's already SSL-enabled by default. No code changes needed, just the README text.

Here's the corrected README:

```markdown
# 🧠 Brain Tumor Detection System

A web-based application that uses deep learning to detect brain tumors from MRI scan images. Built with Flask, TensorFlow/Keras (CNN), and TiDB (MySQL-compatible), and deployed with a lightweight TFLite inference pipeline for production.

🔗 **Live Demo:** [web-based-brain-tumor-detection.onrender.com](https://web-based-brain-tumor-detection.onrender.com)

---

## 📌 Overview

This project allows users to upload an MRI brain scan and receive an instant AI-powered prediction indicating whether a tumor is present. It includes a full authentication system for both regular users and administrators, along with admin-managed FAQ and Health Tips sections.

---

## ✨ Features

### Public
- Home, About, Contact pages
- User registration and login

### User
- Secure login/logout
- Upload MRI scan for prediction
- View AI-generated diagnosis (Tumor Detected / No Tumor Detected)
- Browse Health Tips and FAQs

### Admin
- Secure admin login (role-based access control)
- Manage registered users (view, edit, delete)
- Manage FAQs (create, edit, delete)
- Manage Health Tips (create, edit, delete)

---

## 🛠️ Tech Stack

**Backend:** Python, Flask  
**Frontend:** HTML, CSS, Bootstrap, JavaScript  
**Database:** TiDB Serverless (MySQL-compatible, cloud-hosted)  
**AI/ML:** TensorFlow/Keras (CNN) for training, TensorFlow Lite for lightweight production inference  
**Auth & Security:** bcrypt password hashing, session-based role access control  
**Hosting:** Render (backend), TiDB Cloud (database), GitHub (source control)

---

## 🧠 Model Details

- **Architecture:** Convolutional Neural Network (CNN)
- **Input:** 128x128 RGB MRI images
- **Layers:** Conv2D, MaxPooling, Dropout, Flatten, Dense (Sigmoid output)
- **Loss Function:** Binary Crossentropy
- **Optimizer:** Adam
- **Classes:** Tumor / No Tumor

For production deployment, the trained `.keras` model was converted to **TensorFlow Lite (.tflite)** format. This reduces the model size by ~90% and significantly lowers memory usage during inference, making it suitable for free-tier cloud hosting. Verification testing confirmed the TFLite model produces predictions matching the original Keras model. Inference in production uses the lightweight `ai-edge-litert` runtime instead of full TensorFlow, further reducing memory overhead.

---

## 📂 Project Structure

```

brain-tumor-detection/
│
├── app.py                     # Main Flask application
├── database.py                 # TiDB/MySQL connection & query handlers
├── convert_to_tflite.py        # Script to convert/verify TFLite model
├── requirements.txt
├── Procfile
├── runtime.txt
├── .gitignore
├── .env.example
├── braintumor.sql              # Database schema + seed data
│
├── model/
│   └── brain_tumor_classifier_model.tflite
│
├── static/
│   ├── css/
│   ├── images/
│   └── uploads/                # Uploaded MRI images (runtime)
│
└── templates/
    ├── Admin/
    ├── User/
    └── ... (public pages)
```

---

## ⚙️ Setup & Installation (Local)

1. **Clone the repository**
   ```bash
   git clone https://github.com/VIKASKT1/web-based-brain-tumor-detection.git
   cd web-based-brain-tumor-detection
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Copy `.env.example` to `.env` and fill in your TiDB connection details:
   ```
   SECRET_KEY=your_secret_key
   DB_HOST=your_tidb_host
   DB_PORT=4000
   DB_USER=your_tidb_user
   DB_PASSWORD=your_tidb_password
   DB_NAME=braintumor
   DB_SSL_DISABLED=False
   ```
   > TiDB Serverless uses port `4000` by default and requires a secure (SSL/TLS) connection.

4. **Set up the database**
   Import the provided schema into your TiDB cluster:
   ```bash
   mysql -h your-tidb-host -P 4000 -u your-tidb-user -p braintumor < braintumor.sql
   ```

5. **Run the app**
   ```bash
   python app.py
   ```
   Visit `http://localhost:5000`

---

## ☁️ Deployment

- **Backend:** Deployed on [Render](https://render.com) (free tier)
- **Database:** Hosted on [TiDB Cloud Serverless](https://tidbcloud.com) (free tier, MySQL-compatible)
- **Inference:** Uses `ai-edge-litert` for lightweight TFLite model inference, optimized to run within free-tier memory limits

---

## 🔒 Security Notes

- Passwords are hashed using `bcrypt` before storage
- Role-based access control separates admin and user permissions
- Session cookies use no-cache headers to prevent stale authenticated views
- Environment variables keep all credentials out of source code
- Database connections use TLS/SSL (required by TiDB Serverless)

---

## 📈 Future Improvements

- CSRF protection (Flask-WTF)
- Persistent cloud storage for uploaded images (e.g., S3) instead of ephemeral local storage
- Automated cleanup of old uploaded files

---

## 👤 Author

**Vikas KT**  
Final Year Project — Web Based Brain Tumor Detection using Deep Learning

---

## ⚠️ Disclaimer

This system is an academic project intended for educational and demonstration purposes only. It is **not** a certified medical diagnostic tool and should not be used as a substitute for professional medical advice.

```

Quick note: I set `DB_PORT=4000` (TiDB Serverless's default), and dropped the "connection pooling" line from Future Improvements since TiDB's distributed architecture behaves differently there — not worth a generic MySQL-pooling claim on a different DB engine. Swap the repo URL and author name if either needs adjusting.

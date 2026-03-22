import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Register user API
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")  # For now plain text

    if not username or not email or not password:
        return jsonify({"status":"error", "message":"Fill all fields!"})

    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE username=? OR email=?", (username, email))
    if cursor.fetchone():
        conn.close()
        return jsonify({"status":"error", "message":"User already exists!"})

    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                   (username, email, password))
    conn.commit()
    conn.close()

    return jsonify({"status":"success", "message":"Registered successfully ✅"})

import os
import psycopg2
from flask import Flask, render_template, jsonify, request

CLEAR_PASSWORD = "__clear"
DATABASE_URL = os.environ.get("DATABASE_URL")

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(DATABASE_URL)

# cria tabela automaticamente (safe)
conn = get_connection()
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    messages TEXT NOT NULL
)
""")
conn.commit()
conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/messages", methods=["GET", "POST", "DELETE"])
def msgs():
    conn = get_connection()
    cur = conn.cursor()

    # ➕ POST (add message or clear)
    if request.method == "POST":
        data = request.get_json()
        content = data.get("content", "").strip()

        if not content:
            conn.close()
            return jsonify({"status": "ignored"})

        if content == CLEAR_PASSWORD:
            cur.execute("DELETE FROM messages")
            conn.commit()
            conn.close()
            return jsonify({"status": "success", "message": "Database cleared"})

        cur.execute(
            "INSERT INTO messages (messages) VALUES (%s)",
            (content,)
        )
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})

    # 📥 GET (list messages)
    cur.execute("SELECT messages FROM messages ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()

    return jsonify([row[0] for row in rows])

if __name__ == "__main__":
    app.run("0.0.0.0")

import sqlite3
from flask import Flask, render_template, jsonify, request


CLEAR_PASSWORD = '__clear'#'$(clearDatabasePass:_2012)$'
app = Flask(__name__)

def GetConnection():
  conn = sqlite3.connect("database.db")
  conn.row_factory = sqlite3.Row
  return conn

conn = GetConnection()
conn.execute("""CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, messages VARCHAR(160))""")
conn.commit()
conn.close()

@app.route("/")

def index():
  return render_template("index.html")

@app.route("/messages", methods=["GET", "POST", 'DELETE'])

def msgs():
  conn = GetConnection()

  if request.method == "POST":
      data = request.get_json()
      content = data.get("content", "").strip()

      if content == CLEAR_PASSWORD:
          # Secret entered → clear DB
          conn.execute("DELETE FROM messages")
          conn.commit()
          conn.close()
          return jsonify({"status": "success", "message": "Database cleared"})

      # Normal message → insert
      conn.execute("INSERT INTO messages (messages) VALUES (?)", (content,))
      conn.commit()
      conn.close()
      return jsonify({"status": "success"})

  mssgs = conn.execute("""SELECT * FROM messages""").fetchall()
  conn.close()

  jsonContent = jsonify([message['messages'] for message in mssgs])

  return jsonContent

def DeleteAll():
  conn = GetConnection()

  conn.execute("""DELETE FROM messages""")
  conn.commit()
  conn.close()
  return ''


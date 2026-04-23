import os
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    title TEXT
)
""")
conn.commit()

@app.route("/")
def home():
    return "Backend running 🚀"

@app.route("/api/data", methods=["GET"])
def get_data():
    cursor.execute("SELECT * FROM items")
    rows = cursor.fetchall()
    return jsonify([{"id": r[0], "title": r[1]} for r in rows])

@app.route("/api/data", methods=["POST"])
def add_data():
    data = request.json
    cursor.execute("INSERT INTO items (title) VALUES (%s) RETURNING id", (data["title"],))
    conn.commit()
    return jsonify({"status": "added"})

@app.route("/api/data/<int:id>", methods=["DELETE"])
def delete_data(id):
    cursor.execute("DELETE FROM items WHERE id=%s", (id,))
    conn.commit()
    return jsonify({"status": "deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

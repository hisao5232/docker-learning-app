from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# 環境変数からDB情報を取得
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "notes")
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "password")

# SQLAlchemy 設定
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Noteモデル
class Note(db.Model):
    __tablename__ = "note"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)

# ヘルスチェック
@app.get("/health")
def health():
    return {"status": "ok"}

# HTML表示
@app.route("/")
def index():
    notes = Note.query.order_by(Note.id.asc()).all()
    return render_template("index.html", notes=notes)

# Note一覧取得
@app.get("/notes")
def get_notes():
    notes = Note.query.order_by(Note.id.asc()).all()
    return jsonify([{"id": n.id, "text": n.text} for n in notes])

# Note追加
@app.post("/notes")
def add_note():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "text is required"}), 400

    note = Note(text=text)
    db.session.add(note)
    db.session.commit()
    return jsonify({"id": note.id, "text": note.text}), 201

@app.post("/add_note")
def add_note_form():
    text = (request.form.get("text") or "").strip()
    if text:
        note = Note(text=text)
        db.session.add(note)
        db.session.commit()
    return redirect("/")
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

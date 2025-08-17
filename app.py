from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# 環境変数から DB 接続文字列を組み立て（Compose で注入）
db_user = os.getenv("POSTGRES_USER", "user")
db_pass = os.getenv("POSTGRES_PASSWORD", "password")
db_name = os.getenv("POSTGRES_DB", "notes")
db_host = "db"  # docker-compose のサービス名（=コンテナ内ホスト名）

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# init.sql のテーブル名と合わせる
class Note(db.Model):
    __tablename__ = "note"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/notes")
def get_notes():
    notes = Note.query.order_by(Note.id.asc()).all()
    return jsonify([{"id": n.id, "text": n.text} for n in notes])

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

if __name__ == "__main__":
    # 学習用：シンプルに開発サーバを起動
    app.run(host="0.0.0.0", port=5000)

FROM python:3.11-slim

# Python の標準ログをそのまま出す設定（デバッグしやすい）
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 依存を先に入れてキャッシュを効かせる
COPY app/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# アプリ本体
COPY app/ .

EXPOSE 5000
CMD ["python", "app.py"]

FROM python:3.11-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
# Install system tools your app needs
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr poppler-utils && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "600", "app:app"]
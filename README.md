
# VisionTextAI

VisionTextAI is a **FastAPI application** that allows users to upload **images or PDFs** and extract text using **GPT-4o-mini OCR**.
It also provides a **summarized explanation** of the extracted content in **easy-to-understand language**.
Now includes **Docker support** and **CI/CD pipelines** for automated deployments.

---

## ✨ Features

* 📷 **Image OCR** – Extracts text from uploaded PNG/JPEG images.
* 📄 **PDF OCR** – Hybrid extraction (embedded text + OCR on image-only pages).
* 📝 **Summarization** – Simplifies extracted content for end-users.
* 🌐 **Swagger UI** – Upload and test files interactively.
* 🔒 **.env support** – API key securely managed via environment variables.
* 🐳 **Docker Support** – Run the app in a container.
* ⚙️ **CI/CD with GitHub Actions** – Automatically builds & pushes Docker images to Docker Hub.

---

## 🚀 Getting Started

### 1. Local Setup

```bash
git clone https://github.com/Dhiraj123-star/VisionTextAI.git
cd VisionTextAI
python -m venv venv
source venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
uvicorn main:app --reload
```

Access: 👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### 2. Docker Setup

```bash
docker build -t visiontextai .
docker run -d --name visiontextai -p 8000:8000 --env-file .env visiontextai
```

---

### 3. CI/CD (GitHub Actions)

* On **git push**, GitHub Actions will:

  1. Build the Docker image
  2. Push it to Docker Hub → `dhiraj918106/visiontextai`
  3. Keep your deployments up-to-date automatically

---

## 📌 Example JSON Response

```json
{
  "filename": "document.pdf",
  "extracted_text": "This is the raw OCR text from the document...",
  "summary": "This document explains the main idea in simple words..."
}
```

---

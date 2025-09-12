
# VisionTextAI

VisionTextAI is a simple **FastAPI application** that allows users to upload **images or PDFs** and extract text using **GPT-4o-mini OCR**.
It also provides a **summarized explanation** of the extracted content in **easy-to-understand language**.
Now includes **Docker support** for containerized deployments.

---

## ✨ Features

* 📷 **Image OCR** – Extracts text from uploaded PNG/JPEG images.
* 📄 **PDF OCR** – Extracts embedded text from PDFs and performs OCR on image-only pages.
* ⚡ **Hybrid Strategy** – Uses embedded text first, then OCR only if needed (faster + efficient).
* 📝 **Summarization** – Simplifies the extracted content so end-users can understand it easily.
* 🌐 **Swagger UI** – Upload and test files directly via interactive API docs.
* 🔒 **.env support** – API key is securely managed via environment variables.
* 🐳 **Docker Support** – Easily run the app in a container.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Dhiraj123-star/VisionTextAI.git
cd VisionTextAI
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Run the application locally

```bash
uvicorn main:app --reload
```

---

## 🐳 Running with Docker

### 1. Build the image

```bash
docker build -t visiontextai .
```

### 2. Run the container

```bash
docker run -d --name visiontextai -p 8000:8000 --env-file .env visiontextai
```

### 3. Access the API

👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📖 Usage

* Use the `/extract-text/` endpoint.
* Upload an **image (PNG/JPEG)** or **PDF**.
* Get JSON response with:

  * `filename` → original file name
  * `extracted_text` → raw OCR + extracted text
  * `summary` → simplified explanation of content

---

## 🛠 Tech Stack

* [FastAPI](https://fastapi.tiangolo.com/) – Web framework
* [OpenAI GPT-4o-mini](https://platform.openai.com/) – OCR & Summarization
* [PyPDF2](https://pypi.org/project/pypdf2/) – Extract embedded PDF text
* [pdf2image](https://pypi.org/project/pdf2image/) – Convert PDF pages to images for OCR
* [Pillow (PIL)](https://pillow.readthedocs.io/) – Image processing
* [Docker](https://www.docker.com/) – Containerization

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

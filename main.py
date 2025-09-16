import os
import io
import base64
import asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from openai import OpenAI
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
from PIL import Image

# Load env vars
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(
    title="VisionTextAI",
    description="Upload an image or PDF and extract + summarize text using GPT-4o-mini OCR.",
    version="4.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg"}
ALLOWED_DOC_TYPES = {"application/pdf"}


async def image_to_text(image_bytes: bytes, mime_type: str) -> str:
    """Send image to GPT-4o-mini for OCR and return extracted text."""
    base64_str = base64.b64encode(image_bytes).decode("utf-8")
    data_uri = f"data:{mime_type};base64,{base64_str}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an OCR assistant. Extract all readable text from the image."},
            {"role": "user", "content": [
                {"type": "text", "text": "Please extract the text from this image."},
                {"type": "image_url", "image_url": {"url": data_uri}}
            ]}
        ]
    )
    return response.choices[0].message.content


async def extract_pdf_text(file_bytes: bytes) -> str:
    """Extract text from PDF using hybrid strategy (embedded + OCR only if needed)."""
    reader = PdfReader(io.BytesIO(file_bytes))
    texts = []
    images_to_ocr = []

    # Step 1: Try embedded text extraction
    for i, page in enumerate(reader.pages):
        txt = page.extract_text()
        if txt and len(txt.strip()) > 20:  # use threshold to avoid junk
            texts.append(txt)
        else:
            # Mark for OCR
            images_to_ocr.append(i)

    # Step 2: OCR only for pages without good text
    if images_to_ocr:
        pdf_images = convert_from_bytes(file_bytes, dpi=150)  # lower DPI for speed
        tasks = []
        for idx in images_to_ocr:
            img = pdf_images[idx]
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format="PNG")
            tasks.append(image_to_text(img_byte_arr.getvalue(), "image/png"))

        # Run OCR in parallel
        ocr_results = await asyncio.gather(*tasks)
        texts.extend(ocr_results)

    return "\n".join(texts)


async def summarize_text(extracted_text: str) -> str:
    """Summarize and simplify extracted text for end-users."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes and explains text in simple, easy-to-understand language."},
            {"role": "user", "content": f"Summarize and explain this text simply:\n\n{extracted_text}"}
        ]
    )
    return response.choices[0].message.content


@app.post("/extract-text/")
async def extract_text(file: UploadFile = File(...)):
    """Upload an image or PDF and extract + summarize text."""
    try:
        if file.content_type in ALLOWED_IMAGE_TYPES:
            # Handle image
            image_bytes = await file.read()
            extracted_text = await image_to_text(image_bytes, file.content_type)

        elif file.content_type in ALLOWED_DOC_TYPES:
            # Handle PDF
            file_bytes = await file.read()
            extracted_text = await extract_pdf_text(file_bytes)

        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

        # Summarize for end-user
        summary = await summarize_text(extracted_text)

        return JSONResponse(content={
            "filename": file.filename,
            "extracted_text": extracted_text.strip(),
            "summary": summary.strip()
        })

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

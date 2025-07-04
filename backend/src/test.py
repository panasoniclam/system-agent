from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
import requests
import io
import json
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hoặc ['http://localhost:3000'] nếu muốn giới hạn
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"  # tùy hệ điều hành

OLLAMA_URL = "http://localhost:11434/api/generate"

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    # đọc nhiều file 
    contents = await file.read()
    temp_path = f"temp/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(contents)
        
    print()
    # OCR
    image = Image.open(io.BytesIO(await file.read()))
    text = pytesseract.image_to_string(image, lang="eng")
    # extracted_text = pytesseract.image_to_string(Image.open(image), lang="eng")
    # Prompt cho mô hình LLM
    prompt = f"""
    Từ đoạn văn sau, hãy trích xuất các trường sau và trả về JSON thuần:
    - ho_ten
    - ngay_sinh
    - so_cmnd
    - dia_chi

    Đoạn văn:
    {text}
    """

    # Gọi mô hình LLM qua Ollama
    payload = {
    "model": "llama3.2",   
    "prompt": f"""
    Từ đoạn văn sau, hãy trích xuất và trả kết quả dưới dạng JSON với các trường sau:
    - ho_ten
    - ngay_sinh
    - so_cmnd
    - dia_chi
    - so_tien (nếu có)
    - mã số bảo hiểm
    - mã thể
    - người hành nghề khám chữa bệnh
    - don_vi_lam_viec
    - so_seri
    - chuan_doan_va_phuong_phap_dieu_tri

    Hãy chỉ trả ra JSON thuần, không thêm lời giải thích.

    Đoạn văn:
    {text}
    """,
    "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    print("📦 Ollama raw response:", response.text)
    raw_output = response.json().get("response", "")
    print("📄 raw_output:", raw_output)
    try:
        data = json.loads(raw_output)
    except:
        return JSONResponse(content={"error": "LLM trả về kết quả không hợp lệ", "raw": raw_output}, status_code=500)

    return data

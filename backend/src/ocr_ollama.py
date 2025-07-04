import os
import fitz  
from PIL import Image
import pytesseract
import io
import requests
import zipfile

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    all_text = ""
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        text = pytesseract.image_to_string(img)
        all_text += text + "\n"
    return all_text

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    return pytesseract.image_to_string(img)

def analyze_text_with_ollama(text):
    prompt = f"""
Trích xuất các thông tin chính (Họ tên, ngày sinh, số giấy tờ, địa chỉ,...) từ đoạn văn sau và trả về kết quả dưới dạng JSON:
{text}
"""

    payload = {
    "model": "llama3.2",   
    "prompt": f"""
    Đoạn văn sau có thể chứa nhiều cá nhân, bạn hãy trích xuất thông tin thành danh sách các object JSON.
    Yêu cầu:
    - Trả về danh sách JSON (bắt đầu bằng `[`, kết thúc bằng `]`)
    - Mỗi object chứa:
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

    try:
        res = requests.post("http://localhost:11434/api/generate", json=payload)
        return res.json().get("response", "").strip()
    except Exception as e:
        return f"LLM ERROR: {e}"

def handle_input_file(file_path):
    results = []
    if file_path.endswith(".zip"):
        extract_dir = "unzipped_tmp"
        os.makedirs(extract_dir, exist_ok=True)
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        for fname in os.listdir(extract_dir):
            full_path = os.path.join(extract_dir, fname)
            if fname.lower().endswith(".pdf"):
                text = extract_text_from_pdf(full_path)
            elif fname.lower().endswith((".png", ".jpg", ".jpeg")):
                text = extract_text_from_image(full_path)
            else:
                continue

            llm_result = analyze_text_with_ollama(text)

            # results.append({
            #     "file": fname,
            #     "ocr_text": text,
            #     "llm_result": llm_result
            # })
            results.append(llm_result)
    else:
        # Nếu là file đơn lẻ: ảnh hoặc PDF
        if file_path.lower().endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif file_path.lower().endswith((".png", ".jpg", ".jpeg")):
            text = extract_text_from_image(file_path)
        else:
            return []

        llm_result = analyze_text_with_ollama(text)

        results.append({
            "file": os.path.basename(file_path),
            "ocr_text": text,
            "llm_result": llm_result
        })

    return results

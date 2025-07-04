from PIL import Image
import pytesseract
import requests
import pandas as pd
import json
# Gán đường dẫn nếu cần
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"  # Mac (hoặc tự động nếu đã export PATH)

# Step 1: OCR từ ảnh
image_path = "baohiem.png"  # thay bằng ảnh thật
extracted_text = pytesseract.image_to_string(Image.open(image_path), lang="eng")

print("📥 Text from image:\n", extracted_text)

# Step 2: Gửi prompt vào mô hình Ollama
ollama_url = "http://localhost:11434/api/generate"

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
    {extracted_text}
    """,
    "stream": False
}

response = requests.post(ollama_url, json=payload)
llm_output = response.json().get("response", "").strip()

 
try:
    extracted_info = json.loads(llm_output)
except json.JSONDecodeError:
    print("LLM không trả về JSON hợp lệ!")
    print(llm_output)
    exit()

 

# Tạo DataFrame
df = pd.DataFrame([extracted_info])

# Ghi ra Excel
df.to_excel("output.xlsx", index=False)

print("✅ Ghi xong file Excel: output.xlsx")
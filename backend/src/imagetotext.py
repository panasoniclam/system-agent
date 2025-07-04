from PIL import Image
import pytesseract

# Nếu cần, chỉ định path tesseract (macOS M1/M2 dùng Homebrew sẽ ở đây)
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

text = pytesseract.image_to_string(Image.open("testdata.png"), lang="eng")
print(text)

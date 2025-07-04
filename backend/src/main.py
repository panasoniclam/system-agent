from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from .ocr_ollama import handle_input_file
from fastapi.responses import JSONResponse
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    contents = await file.read()
    os.makedirs("temp_uploads", exist_ok=True)
    temp_path = f"temp_uploads/{file.filename}"
    print(temp_path,"temp_path")
    with open(temp_path, "wb") as f:
        f.write(contents)

    result = handle_input_file(temp_path)

    return JSONResponse(content=result[0] if result else {"error": "Không xử lý được"})

"use client"
import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<string>("");

  const handleUpload = async () => {
    console.log("run")
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setResult(data.llm_result || data.response || "Không có kết quả.");
    console.log(data,"data")
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Upload file zip / hình</h1>
      <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      <button onClick={handleUpload}>Gửi</button>

      <h2>Kết quả:</h2>
  
      <pre>{JSON.stringify(result)}</pre>
    </div>
  );
}

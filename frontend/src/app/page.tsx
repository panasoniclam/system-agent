'use client'
import { useState } from "react"

export default function Home() {
  const [file, setFile] = useState<File | null>(null)
  const [result, setResult] = useState<any>(null)

  const handleUpload = async () => {
    if (!file) return alert("Chọn ảnh trước!")

    const formData = new FormData()
    formData.append("file", file)

    const res = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      body: formData,
    })

    const data = await res.json()
    setResult(data)
  }

  return (
    <div style={{ padding: 32 }}>
      <h2>Trích xuất thông tin từ ảnh CMND</h2>
      <input type="file" onChange={e => setFile(e.target.files?.[0] || null)} />
      <button onClick={handleUpload}>Gửi và xử lý</button>
      <pre>{JSON.stringify(result, null, 2)}</pre>
    </div>
  )
}

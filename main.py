from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="DocuChat")

class ChatRequest(BaseModel):      # aturan format request (validasi otomatis)
    session_id: str
    message: str

@app.get("/health")               # GET = ambil data / cek status
def health():
    return {"status": "ok"}

@app.post("/api/v1/chat")         # POST = kirim data
def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Pesan tidak boleh kosong")
    return {"answer": f"(sementara) kamu bertanya: {req.message}", "sources": []}
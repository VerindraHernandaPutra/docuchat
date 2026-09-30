from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag import answer

app = FastAPI(title="DocuChat")

class ChatRequest(BaseModel):      # aturan format request (validasi otomatis)
    session_id: str
    message: str

@app.get("/health")               # GET = ambil data / cek status
def health():
    return {"status": "ok"}

@app.post("/api/v1/chat")
def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Pesan tidak boleh kosong")
    try:
        result = answer(req.message)
    except Exception:
        raise HTTPException(status_code=503, detail="Layanan LLM sedang tidak tersedia, coba lagi nanti")
    return result
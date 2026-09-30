from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag import answer
# (a) di bagian atas
from contextlib import asynccontextmanager
from db import init_db, save_message, get_history

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()          # buat tabel saat aplikasi start
    yield

app = FastAPI(title="DocuChat", lifespan=lifespan)   # ganti baris app lama

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
    save_message(req.session_id, "user", req.message)
    save_message(req.session_id, "assistant", result["answer"])
    return result

@app.get("/api/v1/history/{session_id}")
def history(session_id: str):
    return {"session_id": session_id, "messages": get_history(session_id)}
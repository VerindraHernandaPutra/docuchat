from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    assert client.get("/health").status_code == 200

def test_pesan_kosong_ditolak():
    r = client.post("/api/v1/chat", json={"session_id": "t", "message": "   "})
    assert r.status_code == 400

def test_field_hilang_422():
    r = client.post("/api/v1/chat", json={"session_id": "t"})
    assert r.status_code == 422
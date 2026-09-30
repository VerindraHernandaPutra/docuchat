import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# 1. LOAD: baca semua PDF (1 halaman = 1 dokumen)
docs = PyPDFDirectoryLoader("data/").load()
print(f"Load: {len(docs)} halaman")

# 2. SPLIT: potong jadi chunk
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
chunks = splitter.split_documents(docs)
print(f"Split: {len(chunks)} chunk")
print("Contoh chunk:\n", chunks[0].page_content[:300])

# 3 + 4. EMBED + STORE: ubah jadi vektor, simpan ke Chroma
embeddings = OllamaEmbeddings(model="bge-m3", base_url=OLLAMA_URL)
Chroma.from_documents(chunks, embeddings, persist_directory="chroma_db")
print("Selesai: tersimpan di folder chroma_db/")
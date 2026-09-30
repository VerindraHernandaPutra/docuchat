from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

db = Chroma(persist_directory="chroma_db", embedding_function=OllamaEmbeddings(model="bge-m3"))
for d in db.similarity_search("metode penelitian yang digunakan", k=3):
    print(d.metadata, "\n", d.page_content[:200], "\n---")
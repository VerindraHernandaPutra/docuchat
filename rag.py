import os
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

embeddings = OllamaEmbeddings(model="bge-m3", base_url=OLLAMA_URL)
vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})      # top-k = 4
llm = ChatOllama(model="qwen2.5:3b", temperature=0.9, base_url=OLLAMA_URL)

prompt = ChatPromptTemplate.from_template(
    """Kamu asisten yang menjawab HANYA berdasarkan konteks berikut.
Jika jawabannya tidak ada di konteks, katakan: "Maaf, informasi itu tidak ada di dokumen."

Konteks:
{context}

Pertanyaan: {question}"""
)

chain = prompt | llm      # LCEL: output prompt dialirkan ke LLM

def answer(question: str) -> dict:
    docs = retriever.invoke(question)                            # RETRIEVE
    context = "\n\n".join(d.page_content for d in docs)          # AUGMENT
    result = chain.invoke({"context": context, "question": question})  # GENERATE
    sources = [{"file": d.metadata.get("source"), "page": d.metadata.get("page")} for d in docs]
    return {"answer": result.content, "sources": sources}
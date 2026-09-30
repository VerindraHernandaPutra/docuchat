import numpy as np
from langchain_ollama import OllamaEmbeddings

e = OllamaEmbeddings(model="bge-m3")
a, b, c = e.embed_documents(["cara reset password", "lupa kata sandi", "resep nasi goreng"])
cos = lambda x, y: np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))
print("password vs kata sandi:", cos(a, b))   # harusnya tinggi
print("password vs nasi goreng:", cos(a, c))  # harusnya rendah
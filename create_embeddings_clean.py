# scripts/create_embeddings_clean.py

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

DATA_DIR = "data"
VECTOR_DIR = "vector_db"

def load_pdfs(data_dir):
    documents = []
    for root, _, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".pdf"):
                path = os.path.join(root, file)
                loader = PyPDFLoader(path)
                docs = loader.load()
                for d in docs:
                    d.metadata["source"] = file
                documents.extend(docs)
    return documents

def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=80,
        separators=["\n\n", "\n", "।", ".", " ", ""]
    )
    return splitter.split_documents(docs)

def build_vector_db(chunks):
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=VECTOR_DIR
    )

if __name__ == "__main__":
    print("📘 Loading PDFs...")
    docs = load_pdfs(DATA_DIR)

    print("✂️ Splitting documents...")
    chunks = split_documents(docs)

    print("🧬 Creating vector database...")
    build_vector_db(chunks)

    print("✅ Embeddings created successfully.")

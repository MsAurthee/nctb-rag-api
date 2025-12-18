import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TXT_DIR = os.path.join(BASE_DIR, "data", "txt")
VECTOR_DIR = os.path.join(BASE_DIR, "vector_db")

print("Loading TXT files...")
docs = []

for file in os.listdir(TXT_DIR):
    if file.endswith(".txt"):
        loader = TextLoader(os.path.join(TXT_DIR, file), encoding="utf-8")
        docs.extend(loader.load())

print("Splitting text...")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)
splits = splitter.split_documents(docs)

print("Embedding...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

db = Chroma.from_documents(
    splits,
    embedding=embeddings,
    persist_directory=VECTOR_DIR
)

print("✅ Vector DB ready")

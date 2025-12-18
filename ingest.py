import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "vector_db")

files = [
    ("data/nctb.txt", "bangla"),
    ("data/english_grammar.txt", "english")
]

all_docs = []

for path, source in files:
    full_path = os.path.join(BASE_DIR, path)
    loader = TextLoader(full_path, encoding="utf-8")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    docs = splitter.split_documents(documents)

    # 🔑 ADD METADATA (SAFE)
    for d in docs:
        d.metadata["source"] = source

    all_docs.extend(docs)

# ✅ SAFE multilingual embedding (Bangla + English)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

db = Chroma.from_documents(
    all_docs,
    embedding=embeddings,
    persist_directory=DB_DIR
)

print("✅ Bangla + English books ingested successfully")

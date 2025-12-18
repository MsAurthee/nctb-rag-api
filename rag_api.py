from fastapi import FastAPI
from pydantic import BaseModel
import os

# LangChain core
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Vector DB
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# LLM (Ollama – FIXED)
from langchain_ollama import OllamaLLM


# =========================
# FastAPI App
# =========================
app = FastAPI(
    title="NCTB RAG API",
    description="RAG system for NCTB Class 9 & 10 books",
    version="1.0"
)

# =========================
# Paths
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "vector_db")

# =========================
# Embeddings (ONLY embeddings use HF – OK)
# =========================
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# =========================
# Vector DB
# =========================
db = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embeddings
)

# =========================
# LLM (PURE OLLAMA – NO HF LLM)
# =========================
llm = OllamaLLM(
    model="qwen2.5:1.5b",
    temperature=0.2,
    num_ctx=2048
)



# =========================
# Prompt
# =========================
prompt = ChatPromptTemplate.from_template(
    """
তুমি একজন NCTB বইভিত্তিক সহকারী।

নিচের context ব্যবহার করে প্রশ্নের উত্তর দাও।
যদি উত্তর context এ না থাকে, তাহলে বলবে:
"এই তথ্যটি NCTB বইয়ে পাওয়া যায়নি।"

Context:
{context}

Question:
{question}

Answer:
"""
)

# =========================
# Context Retriever
# =========================
def get_context(question: str) -> str:
    retriever = db.as_retriever(search_kwargs={"k": 4})
    docs = retriever.invoke(question)

    if not docs:
        return "No relevant context found."

    return "\n\n".join(doc.page_content for doc in docs)

# =========================
# RAG Chain (SAFE & STABLE)
# =========================
rag_chain = (
    {
        "context": get_context,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

# =========================
# Request Schema
# =========================
class Question(BaseModel):
    question: str

# =========================
# Health Check
# =========================
@app.get("/")
def root():
    return {"status": "API is running"}

# =========================
# Ask Endpoint
# =========================
@app.post("/ask")
def ask(q: Question):
    try:
        answer = rag_chain.invoke(q.question)
        return {"answer": answer}
    except Exception as e:
        return {
            "error": "LLM processing failed",
            "details": str(e)
        }

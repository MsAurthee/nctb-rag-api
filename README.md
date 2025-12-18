📘 NCTB RAG API

Retrieval-Augmented Generation (RAG) API for NCTB Textbooks

🧠 Project Overview

NCTB RAG API is a backend service that allows users to ask questions from NCTB textbooks and receive accurate, context-based answers.

The system uses Retrieval-Augmented Generation (RAG), which means:

Answers are generated only from textbook content

If the answer is not found in the books, the system clearly says so

No hallucinated or made-up answers

🏗️ Architecture (High Level)
User Question
      ↓
Vector Search (ChromaDB)
      ↓
Relevant NCTB Text Chunks
      ↓
Prompt + Context
      ↓
LLM (Phi / Ollama / HF)
      ↓
Final Answer

🚀 Tech Stack
Layer	Technology
API Framework	FastAPI
LLM	Ollama (Phi) / HuggingFace
Embeddings	sentence-transformers
Vector Database	ChromaDB
Language	Python 3
Deployment	Render
API Docs	Swagger (OpenAPI)
📂 Project Structure
nctb-rag-api/
│
├── scripts/
│   ├── rag_api.py        # Main FastAPI application
│
├── vector_db/            # Chroma persistent vector database
│
├── requirements.txt      # Python dependencies
│
├── README.md             # Project documentation
│
└── .gitignore

⚙️ How RAG Works in This Project

NCTB books are converted into text

Text is split into small chunks

Each chunk is converted into embeddings

Embeddings are stored in ChromaDB

User asks a question

Most relevant chunks are retrieved

LLM answers only using retrieved context

If context is missing:

"এই তথ্যটি NCTB বইয়ে পাওয়া যায়নি।"

🔌 API Endpoint
POST /ask

Ask a question from NCTB textbooks.

Request Body
{
  "question": "What is a noun?"
}

Response
{
  "answer": "A noun is a word that names a person, place, thing, or idea."
}

📑 API Documentation (Swagger)

After running the server, open in browser:

http://localhost:10000/docs


or (Render URL):

https://<your-service-name>.onrender.com/docs

🖥️ Local Setup (Development)
1️⃣ Clone the Repository
git clone https://github.com/MsAurthee/nctb-rag-api.git
cd nctb-rag-api

2️⃣ Create Virtual Environment
python -m venv venv_rag
source venv_rag/bin/activate   # Linux/Mac
venv_rag\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the API
uvicorn scripts.rag_api:app --host 0.0.0.0 --port 10000

☁️ Deployment (Render)
Render Configuration
Field	Value
Language	Python 3
Build Command	pip install -r requirements.txt
Start Command	uvicorn scripts.rag_api:app --host 0.0.0.0 --port 10000
Instance Type	Standard (2GB RAM)

⚠️ Free tier (512MB) is not sufficient for LLM-based workloads.

🧪 Error Handling

Missing context → Safe fallback response

LLM failure → API returns meaningful error

No hallucinated answers

Debug logging enabled for development

🔐 Security & Design Choices

Stateless API

No user data stored

Vector DB is read-only during query

Safe prompt constraints enforced

🔮 Future Improvements

Frontend UI (React / Next.js)

Authentication & rate limiting

Multi-book selection

Bangla OCR optimization

Streaming responses

Cloud-based LLM fallback

👩‍💻 Author

Marjan Sultana Aurthee
CSE | AI & RAG Systems
GitHub: https://github.com/MsAurthee

⭐ Final Note

This project is designed to be:

Explainable

Reliable

Education-focused

Production-ready

If you are a frontend developer, simply consume the /ask API.
All intelligence is handled in the backend.

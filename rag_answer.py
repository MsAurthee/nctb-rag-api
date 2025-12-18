# scripts/rag_answer.py

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

VECTOR_DIR = "vector_db"

def load_chain():
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    vector_db = Chroma(
        persist_directory=VECTOR_DIR,
        embedding_function=embedding
    )

    llm = OllamaLLM(
        model="phi",
        temperature=0.2
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a strict academic teacher.
Answer ONLY using the provided NCTB textbook context.
Use the SAME language as the question.

If the answer is NOT found in the context, say:
"এই তথ্যটি NCTB বইয়ে পাওয়া যায়নি।"

Context:
{context}

Question:
{question}

Answer:
"""
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_db.as_retriever(search_kwargs={"k": 4}),
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=False
    )

    return chain

if __name__ == "__main__":
    chain = load_chain()
    while True:
        q = input("❓ Question: ")
        if q.lower() in ["exit", "quit"]:
            break
        print("🧠 Answer:", chain.invoke(q)["result"])

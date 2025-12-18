from langchain_huggingface import HuggingFaceEndpoint

llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-base",
    max_new_tokens=50
)

print(llm.invoke("What is a noun?"))

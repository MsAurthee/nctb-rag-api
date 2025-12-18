from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

loader = DirectoryLoader(
    "data/ict",
    glob="**/*.pdf",
    loader_cls=PyPDFLoader
)

docs = loader.load()

print("Total pages loaded:", len(docs))
print("Sample text:")
print(docs[0].page_content[:500])

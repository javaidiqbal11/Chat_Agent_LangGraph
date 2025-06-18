import os
from dotenv import load_dotenv
from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings

# Load API Key
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# Load Word files from docs/
def load_word_docs(folder_path: str):
    texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".docx"):
            doc_path = os.path.join(folder_path, filename)
            doc = Document(doc_path)
            full_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            texts.append(full_text)
    return texts

# Chunking text
def chunk_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
        separators=["\n", ".", " "]
    )
    return splitter.create_documents(docs)

# Main routine
def store_to_chroma():
    raw_texts = load_word_docs("docs")
    documents = chunk_docs(raw_texts)
    embeddings = OpenAIEmbeddings(openai_api_key=openai_key)

    # Create ChromaDB vectorstore
    vectorstore = Chroma.from_documents(documents, embedding=embeddings, persist_directory="chroma_store")
    print("Documents embedded and stored in ChromaDB.")

if __name__ == "__main__":
    store_to_chroma()

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

# === MODIFICATION HERE ===
# 'langchain.text_splitter' is deprecated.
# We now import from the new 'langchain_text_splitters' package.
from langchain_text_splitters import RecursiveCharacterTextSplitter
# =========================


# --- Configuration ---
DOCS_DIR = "docs"
CHROMA_DB_DIR = "chroma_db"
EMBEDDING_MODEL = 'all-MiniLM-L6-v2' 

def main():
    """
    Main function to ingest PDF documents into a Chroma vector store.
    This script will:
    1. Load PDFs from the DOCS_DIR.
    2. Split them into manageable chunks.
    3. Create embeddings for each chunk.
    4. Save them to a persistent vector store in CHROMA_DB_DIR.
    """
    print("Starting document ingestion process...")

    # 1. Load documents
    documents = []
    if not os.path.exists(DOCS_DIR):
        print(f"Error: The directory '{DOCS_DIR}' was not found.")
        print("Please create a 'docs' folder and add your ESG PDFs.")
        return

    pdf_files = [f for f in os.listdir(DOCS_DIR) if f.endswith(".pdf")]
    if not pdf_files:
        print(f"No PDF files found in the '{DOCS_DIR}' directory. Exiting.")
        return
        
    print(f"Found {len(pdf_files)} PDF file(s) to process...")

    for filename in pdf_files:
        filepath = os.path.join(DOCS_DIR, filename)
        try:
            loader = PyPDFLoader(filepath)
            loaded_docs = loader.load()
            documents.extend(loaded_docs)
            print(f"Successfully loaded {filename}")
        except Exception as e:
            print(f"Failed to load or process {filename}. Error: {e}")

    if not documents:
        print("No documents were successfully loaded. Exiting.")
        return

    print(f"\nTotal documents loaded: {len(documents)}")

    # 2. Split documents into smaller chunks
    # This class is now imported from 'langchain_text_splitters'
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)
    print(f"Documents split into {len(splits)} chunks.")

    # 3. Create embeddings
    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    embedding_function = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)

    # 4. Create and persist the Chroma vector store
    print(f"Creating and persisting vector store at '{CHROMA_DB_DIR}'...")
    # This will overwrite the existing database each time.
    # For a production app, you might want to check for existing IDs.
    db = Chroma.from_documents(
        documents=splits, 
        embedding=embedding_function,
        persist_directory=CHROMA_DB_DIR
    )
    
    print("\n--- Ingestion Complete ---")
    print(f"Vector store created at '{CHROMA_DB_DIR}' with {len(splits)} chunks.")

if __name__ == "__main__":
    main()
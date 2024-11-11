from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
import os

DATA_PATH = 'Data/'
DB_FAISS_PATH = 'db'

# Create vector database
def create_vector_db():
    # Load PDF documents
    print("Loading documents from directory:", DATA_PATH)
    loader = DirectoryLoader(DATA_PATH, glob='*.pdf', loader_cls=PyPDFLoader)
    documents = loader.load()
    print(f"Number of documents loaded: {len(documents)}")

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    print(f"Number of text chunks created: {len(texts)}")

    # Verify the content of a few chunks
    print("Sample chunks:")
    for i, chunk in enumerate(texts[:3]):
        print(f"Chunk {i+1}: {chunk.page_content[:100]}...")  # Print first 100 characters of each chunk's content


    # Initialize embeddings model
    print("Initializing embeddings model...")
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2', model_kwargs={'device': 'cpu'})

    # Create FAISS vector store
    print("Creating FAISS vector store...")
    db = FAISS.from_documents(texts, embeddings)
    
    # Check the number of embeddings
    if db is not None:
        print(f"Number of embeddings in FAISS vector store: {len(db.index_to_docstore_id)}")
    else:
        print("Failed to create FAISS vector store.")

    # Save FAISS database locally
    print(f"Saving FAISS vector store to {DB_FAISS_PATH}...")
    db.save_local(DB_FAISS_PATH)

    # Verify the saved FAISS database file
    if os.path.exists(DB_FAISS_PATH):
        print(f"FAISS database successfully saved at {DB_FAISS_PATH}")
    else:
        print("Error: FAISS database was not saved correctly.")

if __name__ == "__main__":
    create_vector_db()

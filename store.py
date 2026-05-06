import os
import chromadb
from typing import List, Dict, Any
from chromadb.config import Settings
from processing.embeddings import get_embedding_model
from langchain_community.vectorstores import Chroma

# Persistent directory for ChromaDB
CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

def get_vector_store():
    """
    Initialize or load the ChromaDB vector store.
    """
    embeddings = get_embedding_model()
    
    # Initialize LangChain's Chroma vector store wrapper
    vector_store = Chroma(
        collection_name="doc_intelligence",
        embedding_function=embeddings,
        persist_directory=CHROMA_PERSIST_DIR
    )
    
    return vector_store

def add_documents_to_store(chunks: List[Dict[str, Any]]):
    """
    Add document chunks to the vector store.
    """
    vector_store = get_vector_store()
    
    texts = [chunk["page_content"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]
    
    # Add texts will automatically persist in recent versions if directory is set
    vector_store.add_texts(texts=texts, metadatas=metadatas)
    vector_store.persist()
    
    return True

def search_documents(query: str, k: int = 4):
    """
    Search for top-k similar documents for a query.
    """
    vector_store = get_vector_store()
    results = vector_store.similarity_search_with_score(query, k=k)
    return results

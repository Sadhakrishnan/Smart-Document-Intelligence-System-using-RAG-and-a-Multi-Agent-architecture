from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(documents: List[Dict[str, Any]], chunk_size: int = 500, chunk_overlap: int = 50) -> List[Dict[str, Any]]:
    """
    Splits a list of document dictionaries (with 'page_content' and 'metadata')
    into smaller chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    
    chunks = []
    for doc in documents:
        text = doc["page_content"]
        metadata = doc["metadata"]
        
        split_texts = text_splitter.split_text(text)
        
        for split in split_texts:
            chunks.append({
                "page_content": split,
                "metadata": metadata
            })
            
    return chunks

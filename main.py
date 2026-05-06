from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import shutil
import os
from typing import List

from ingestion.pdf_loader import extract_text_from_pdf
from ingestion.ocr import extract_text_from_image
from processing.chunking import chunk_text
from store import add_documents_to_store
from agents.router import classify_intent
from agents.retrieval_agent import run_retrieval
from agents.summarizer_agent import run_summarization
from agents.extraction_agent import run_extraction
from agents.comparison_agent import run_comparison

app = FastAPI(title="Smart Document Intelligence System")

class QueryRequest(BaseModel):
    query: str

@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Upload documents, process them, and store in Vector DB.
    """
    all_chunks = []
    
    for file in files:
        contents = await file.read()
        filename = file.filename.lower()
        
        extracted_data = []
        if filename.endswith(".pdf"):
            extracted_data = extract_text_from_pdf(contents, use_pdfplumber=True)
        elif filename.endswith((".png", ".jpg", ".jpeg")):
            extracted_data = extract_text_from_image(contents, source_name=file.filename)
        else:
            # Try plain text fallback
            try:
                text = contents.decode("utf-8")
                extracted_data = [{"page_content": text, "metadata": {"source": file.filename}}]
            except Exception:
                continue
                
        if extracted_data:
            chunks = chunk_text(extracted_data)
            all_chunks.extend(chunks)
            
    if not all_chunks:
        raise HTTPException(status_code=400, detail="No readable content found in uploaded files.")
        
    success = add_documents_to_store(all_chunks)
    
    return {"message": f"Successfully processed and stored {len(all_chunks)} chunks.", "chunks": len(all_chunks)}

@app.post("/query")
async def handle_query(request: QueryRequest):
    """
    Handle a generic query and route it to the appropriate agent.
    """
    query = request.query
    intent = classify_intent(query)
    
    if intent == "summarization":
        result = run_summarization(query)
        result["intent"] = intent
        return result
    elif intent == "extraction":
        result = run_extraction(query)
        result["intent"] = intent
        return result
    elif intent == "comparison":
        result = run_comparison(query)
        result["intent"] = intent
        return result
    else:
        # Default to retrieval
        result = run_retrieval(query)
        result["intent"] = "retrieval"
        return result

@app.post("/extract")
async def handle_extract(request: QueryRequest):
    """
    Explicit endpoint for structured JSON extraction.
    """
    return run_extraction(request.query)

@app.post("/compare")
async def handle_compare(request: QueryRequest):
    """
    Explicit endpoint for multi-document comparison.
    """
    return run_comparison(request.query)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

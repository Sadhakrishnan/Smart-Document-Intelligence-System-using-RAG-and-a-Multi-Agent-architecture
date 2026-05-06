from store import search_documents
from agents.router import get_llm
from langchain.prompts import PromptTemplate
import json

def run_extraction(query: str):
    """
    Extracts structured JSON data from documents based on a query.
    """
    # We retrieve relevant docs that might contain the data
    docs = search_documents(query, k=3)
    
    if not docs:
        return {"extracted_data": {}, "error": "No relevant documents found for extraction."}
        
    context = "\n\n".join([f"Source: {doc[0].metadata.get('source', 'Unknown')}\nContent: {doc[0].page_content}" for doc in docs])
    
    llm = get_llm()
    prompt = PromptTemplate(
        input_variables=["context", "query"],
        template="""
You are a strict data extraction agent. Extract the requested information from the provided context and return it as valid JSON ONLY.
Do not include any explanation, markdown formatting (like ```json), or conversational text. Just the JSON object.

Context:
{context}

Extraction Request:
{query}

JSON Output:
"""
    )
    
    chain = prompt | llm
    
    try:
        response = chain.invoke({"context": context, "query": query})
        # Clean up output in case LLM added markdown
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
            
        json_data = json.loads(content.strip())
        return {
            "extracted_data": json_data,
            "sources": [doc[0].metadata for doc in docs]
        }
    except json.JSONDecodeError:
        return {
            "extracted_data": {},
            "error": "Failed to parse LLM output as JSON.",
            "raw_output": response.content
        }
    except Exception as e:
        return {
            "extracted_data": {},
            "error": f"Error during extraction: {str(e)}"
        }

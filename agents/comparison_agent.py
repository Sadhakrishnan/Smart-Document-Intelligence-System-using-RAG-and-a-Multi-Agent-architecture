from store import search_documents
from agents.router import get_llm
from langchain.prompts import PromptTemplate

def run_comparison(query: str):
    """
    Compares multiple documents or entities based on a query.
    """
    # Retrieve documents to compare
    docs = search_documents(query, k=6)
    
    if not docs:
        return {"comparison": "No documents found to compare.", "sources": []}
        
    context = "\n\n".join([f"Source: {doc[0].metadata.get('source', 'Unknown')}\nContent: {doc[0].page_content}" for doc in docs])
    sources = [doc[0].metadata for doc in docs]
    
    llm = get_llm()
    prompt = PromptTemplate(
        input_variables=["context", "query"],
        template="""
You are an expert comparison agent. Compare the requested information across the provided documents.
Highlight the key differences and similarities clearly. Use bullet points or a structured format if helpful.

Documents:
{context}

Comparison Request:
{query}

Comparison Analysis:
"""
    )
    
    chain = prompt | llm
    
    try:
        response = chain.invoke({"context": context, "query": query})
        return {
            "comparison": response.content,
            "sources": sources
        }
    except Exception as e:
        return {
            "comparison": f"Error generating comparison: {str(e)}",
            "sources": sources
        }

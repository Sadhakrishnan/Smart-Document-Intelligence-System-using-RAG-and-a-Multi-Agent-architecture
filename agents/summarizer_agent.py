from store import search_documents
from agents.router import get_llm
from langchain.prompts import PromptTemplate

def run_summarization(query: str):
    """
    Summarizes documents based on a query.
    """
    # Retrieve top documents that might be relevant to summarize
    docs = search_documents(query, k=5)
    
    if not docs:
        return {"summary": "No documents found to summarize.", "sources": []}
        
    context = "\n\n".join([f"Source: {doc[0].metadata.get('source', 'Unknown')}\nContent: {doc[0].page_content}" for doc in docs])
    sources = [doc[0].metadata for doc in docs]
    
    llm = get_llm()
    prompt = PromptTemplate(
        input_variables=["context", "query"],
        template="""
You are an expert summarizer. Provide a structured summary of the following documents based on the user's request.
Include section-wise headings if applicable.

Documents:
{context}

Request:
{query}

Structured Summary:
"""
    )
    
    chain = prompt | llm
    
    try:
        response = chain.invoke({"context": context, "query": query})
        return {
            "summary": response.content,
            "sources": sources
        }
    except Exception as e:
        return {
            "summary": f"Error generating summary: {str(e)}",
            "sources": sources
        }

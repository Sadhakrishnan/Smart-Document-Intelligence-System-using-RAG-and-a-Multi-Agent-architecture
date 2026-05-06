from store import search_documents
from agents.router import get_llm
from langchain.prompts import PromptTemplate

def run_retrieval(query: str):
    """
    Retrieves context and answers the question.
    """
    docs = search_documents(query, k=4)
    
    if not docs:
        return {"answer": "No relevant documents found.", "sources": []}
    
    context = "\n\n".join([f"Source: {doc[0].metadata.get('source', 'Unknown')}\nContent: {doc[0].page_content}" for doc in docs])
    sources = [doc[0].metadata for doc in docs]
    
    llm = get_llm()
    prompt = PromptTemplate(
        input_variables=["context", "query"],
        template="""
Answer the question based ONLY on the following context. If you cannot answer based on the context, say "I don't know based on the provided documents."

Context:
{context}

Question:
{query}

Answer:
"""
    )
    
    chain = prompt | llm
    
    try:
        response = chain.invoke({"context": context, "query": query})
        return {
            "answer": response.content,
            "sources": sources
        }
    except Exception as e:
        return {
            "answer": f"Error generating answer: {str(e)}",
            "sources": sources
        }

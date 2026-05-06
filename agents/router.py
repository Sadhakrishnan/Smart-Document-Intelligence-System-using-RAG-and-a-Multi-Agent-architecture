from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    # Fallback to a dummy key if not set, for local testing without calls
    api_key = os.getenv("OPENAI_API_KEY", "dummy-key")
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=api_key)

def classify_intent(query: str) -> str:
    """
    Classify the intent of the user query into one of:
    - retrieval (Q&A)
    - summarization
    - extraction
    - comparison
    """
    llm = get_llm()
    prompt = PromptTemplate(
        input_variables=["query"],
        template="""
You are an intent classifier for a Document Intelligence System.
Classify the following user query into exactly one of the following categories:
- retrieval: General question answering based on documents.
- summarization: Requesting a summary of documents.
- extraction: Requesting structured data extraction (e.g., JSON, invoices).
- comparison: Requesting comparison between multiple documents.

Return ONLY the category name.

Query: {query}
Category:
"""
    )
    
    chain = prompt | llm
    try:
        response = chain.invoke({"query": query})
        intent = response.content.strip().lower()
        if intent not in ["retrieval", "summarization", "extraction", "comparison"]:
            return "retrieval" # default fallback
        return intent
    except Exception as e:
        print(f"Error classifying intent: {e}")
        return "retrieval" # default fallback

from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embedding_model(model_name: str = "all-MiniLM-L6-v2"):
    """
    Returns a SentenceTransformer embeddings model wrapped in LangChain interface.
    """
    # model_kwargs={'device': 'cpu'} can be added if GPU is not available
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    return embeddings

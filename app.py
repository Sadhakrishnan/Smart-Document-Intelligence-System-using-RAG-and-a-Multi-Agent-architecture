import streamlit as st
import requests
import json

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Smart Document Intelligence", layout="wide")

st.title("📄 Smart Document Intelligence System")

st.sidebar.header("1. Upload Documents")
uploaded_files = st.sidebar.file_uploader(
    "Upload PDFs, Images, or Text", 
    accept_multiple_files=True,
    type=["pdf", "png", "jpg", "jpeg", "txt"]
)

if st.sidebar.button("Process Documents"):
    if uploaded_files:
        with st.spinner("Processing documents..."):
            files_to_upload = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
            try:
                response = requests.post(f"{API_URL}/upload", files=files_to_upload)
                if response.status_code == 200:
                    st.sidebar.success(f"Success! Processed {response.json().get('chunks', 0)} text chunks.")
                else:
                    st.sidebar.error(f"Error: {response.text}")
            except Exception as e:
                st.sidebar.error(f"Failed to connect to API: {str(e)}")
    else:
        st.sidebar.warning("Please upload files first.")

st.header("2. Ask Questions or Instruct Agents")

query_modes = ["Auto-Route (Smart)", "Q&A (Retrieval)", "Summarization", "Extraction (JSON)", "Comparison"]
mode = st.radio("Select Mode:", query_modes, horizontal=True)

query = st.text_area("Enter your query or request:")

if st.button("Submit"):
    if not query:
        st.warning("Please enter a query.")
    else:
        with st.spinner("Thinking..."):
            try:
                payload = {"query": query}
                if mode == "Auto-Route (Smart)":
                    endpoint = f"{API_URL}/query"
                elif mode == "Q&A (Retrieval)":
                    # Force retrieval by sending to /query but routing logic handles it, or create a specific endpoint
                    # Since we don't have a specific retrieval endpoint, we rely on the prompt to force it
                    endpoint = f"{API_URL}/query" 
                elif mode == "Extraction (JSON)":
                    endpoint = f"{API_URL}/extract"
                elif mode == "Comparison":
                    endpoint = f"{API_URL}/compare"
                else:
                    # Summarization
                    endpoint = f"{API_URL}/query" # Will be routed if we specify 'summarize' in the text
                    payload["query"] = f"Summarize: {query}"
                    
                response = requests.post(endpoint, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.subheader("Results")
                    
                    if "intent" in data:
                        st.info(f"Routed to: **{data['intent'].title()} Agent**")
                    
                    if "answer" in data:
                        st.markdown(data["answer"])
                    elif "summary" in data:
                        st.markdown(data["summary"])
                    elif "extracted_data" in data:
                        st.json(data["extracted_data"])
                    elif "comparison" in data:
                        st.markdown(data["comparison"])
                        
                    with st.expander("Show Sources"):
                        if "sources" in data and data["sources"]:
                            for i, source in enumerate(data["sources"]):
                                st.write(f"**Source {i+1}:**", source)
                        else:
                            st.write("No specific sources referenced.")
                else:
                    st.error(f"API Error: {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to API: {str(e)}")

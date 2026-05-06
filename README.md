# Smart Document Intelligence System using RAG + Multi-Agent Architecture

An end-to-end **Smart Document Intelligence System** built with **Retrieval-Augmented Generation (RAG)** and **Multi-Agent AI architecture**.

This system processes multi-format documents, extracts knowledge, stores embeddings in a vector database, routes user queries intelligently, and returns explainable outputs with source references.

---

## 🚀 Features

### 📄 Multi-format Document Support
Supports:

- PDF (text-based + scanned)
- Images (`.jpg`, `.png`)
- Text files (`.txt`)

---

### 🔍 OCR for Scanned Documents
Automatically extracts text from scanned documents using:

- Tesseract OCR
- EasyOCR

Capabilities:

- Image-to-text extraction
- Scanned PDF processing
- Optional multilingual OCR support

---

### 🧹 Text Processing Pipeline
Preprocessing includes:

- Text cleaning
- Noise/symbol removal
- Whitespace normalization

Chunking strategy:

- **300–500 tokens per chunk**
- **50 token overlap**

Metadata preserved for traceability:

```json
{
  "chunk": "sample text...",
  "source": "invoice.pdf",
  "page": 2
}
```

---

## 🧠 System Architecture

```text
User Upload
   ↓
Document Ingestion Pipeline
   ↓
OCR Layer (if needed)
   ↓
Text Cleaning + Chunking
   ↓
Embedding Generation
   ↓
Vector Database Storage
   ↓
Agent Router (Intent Classification)
   ↓
Specialized Agents
   ├── Retrieval Agent (Q&A)
   ├── Summarization Agent
   ├── Extraction Agent
   └── Comparison Agent
   ↓
LLM Reasoning Layer
   ↓
Final Output (Answer / JSON / Insights)
   ↓
Frontend UI
```

---

## 🤖 Multi-Agent System

### 1. Retrieval Agent (RAG Q&A)
Handles question answering.

Workflow:

- Embed user query
- Retrieve top-k relevant chunks
- Pass retrieved context to LLM
- Generate grounded answer

Output:

- Accurate answer
- Source references

Example:

```bash
Q: What is the invoice total?
A: ₹12,000 (Source: page 2, invoice.pdf)
```

---

### 2. Summarization Agent
Generates:

- Short summary
- Detailed summary
- Section-wise summary

Example:

```bash
Summarize this legal document
```

Output:

- Key clauses
- Risks
- Summary headings

---

### 3. Extraction Agent
Converts unstructured text into structured JSON.

Example query:

```bash
Extract invoice_number, date, total
```

Output:

```json
{
  "invoice_number": "INV-123",
  "date": "2024-01-01",
  "total": 12000
}
```

Supports:

- Invoices
- Resumes
- Contracts
- Custom schemas

---

### 4. Comparison Agent
Compares multiple uploaded documents.

Capabilities:

- Field comparison
- Difference analysis
- Percentage change

Example:

```bash
Compare Invoice A and Invoice B
```

Output:

```text
Invoice A: ₹10,000
Invoice B: ₹12,000
Difference: +20%
```

---

## 🔥 RAG Pipeline

### Embeddings
Uses:

- Sentence Transformers
- `all-MiniLM-L6-v2`

---

### Vector Database
Supported vector stores:

- FAISS
- ChromaDB

Stores:

- Embeddings
- Metadata
- Source references

Enables:

- Semantic similarity search
- Top-k retrieval

---

## ⚙️ Backend APIs (FastAPI)

### Upload Documents

```http
POST /upload
```

Uploads files and processes ingestion pipeline.

---

### Query Documents

```http
POST /query
```

Supports:

- Question answering
- Summarization

---

### Extract Structured Data

```http
POST /extract
```

Returns JSON outputs.

---

### Compare Documents

```http
POST /compare
```

Returns document comparison insights.

---

## 🎨 Frontend

Built with:

- Streamlit *(recommended for quick demo)*
- React *(production UI)*

Features:

- Upload multiple documents
- Chat interface
- JSON viewer
- Comparison dashboard
- Source highlighting

Optional:

- Show source chunks toggle
- Confidence score display

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit / React |
| OCR | Tesseract / EasyOCR |
| RAG | LangChain |
| Multi-Agent | CrewAI / LangGraph |
| Embeddings | Sentence Transformers |
| Vector DB | FAISS / Chroma |
| LLM | OpenAI GPT / Mistral / LLaMA |

---

## 📂 Project Structure

```bash
doc-intelligence/
│
├── ingestion/
│   ├── pdf_loader.py
│   ├── ocr.py
│
├── processing/
│   ├── chunking.py
│   ├── embeddings.py
│
├── agents/
│   ├── router.py
│   ├── retrieval_agent.py
│   ├── extraction_agent.py
│   ├── summarizer_agent.py
│   ├── comparison_agent.py
│
├── vector_db/
│   └── store.py
│
├── api/
│   └── main.py
│
├── frontend/
│   └── app.py
│
└── README.md
```

---

## 🔥 Advanced Features

### High-impact improvements

- Table extraction from PDFs
- Document classification
    - Invoice
    - Resume
    - Legal
- Multi-language OCR + translation
- Confidence score from similarity search
- Highlight exact source chunks used for answers
- Explainable RAG outputs

---

## 📌 Expected Outputs

### Question Answering

```bash
Q: What is the total amount?
A: ₹12,000 (page 2)
```

---

### JSON Extraction

```json
{
  "invoice_number": "INV-123",
  "total": 12000
}
```

---

### Comparison

```bash
Invoice B is 20% higher than Invoice A
```

---

## 🧪 Installation

Clone repository:

```bash
git clone https://github.com/your-username/doc-intelligence.git
cd doc-intelligence
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run backend:

```bash
uvicorn api.main:app --reload
```

Run frontend:

```bash
streamlit run frontend/app.py
```

---

## 🔐 Design Principles

- Modular architecture
- Production-ready code
- Explainable AI outputs
- Grounded RAG responses
- Minimal hallucination
- Structured outputs

---

## 📈 Future Scope

- Hybrid search (keyword + semantic)
- Knowledge graph integration
- Agent memory
- Workflow automation
- Cloud deployment (AWS/GCP/Azure)

---

## 👨‍💻 Author

Built as an advanced AI engineering project for:

- RAG systems
- Multi-agent orchestration
- Document AI
- Production LLM pipelines

---

## ⭐ If you found this useful

Give this repo a star ⭐

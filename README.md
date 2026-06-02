# Enterprise RAG Document Analyzer 🚀

A secure, high-performance AI knowledge base that uses Retrieval-Augmented Generation (RAG) to instantly extract answers from massive PDF documents while strictly preventing AI hallucinations.

## 📌 Business Value
Traditional LLMs hallucinate when asked about proprietary data. This application solves that by anchoring the AI's responses exclusively to the provided internal documents. It allows users to query dense PDFs (reports, manuals, contracts) in natural language, reducing information retrieval time from hours to seconds.

## ⚙️ Architecture & Data Flow
1. **Document Ingestion:** Parses complex PDF documents and extracts raw text.
2. **Text Chunking:** Splits the text into overlapping semantic chunks to preserve context.
3. **Embedding Generation:** Converts text chunks into vector embeddings.
4. **Vector Storage:** Stores embeddings in a vector database for rapid semantic search.
5. **Retrieval & Generation:** When a user asks a question, the system retrieves the most relevant chunks from the database, feeds them into the LLM as context, and generates a grounded, accurate response.

## 🛠️ Tech Stack
* **Backend:** Python, FastAPI, Uvicorn
* **Frontend:** Streamlit
* **AI Framework:** LangChain
* **Vector Database:** ChromaDB
* **Embeddings:** HuggingFace (`sentence-transformers`)
* **LLM:** Google Gemini (`google-genai`)
* **Document Processing:** PyPDF

## 🚀 Local Installation & Setup

### 1. Clone the repository
```bash
git clone [https://github.com/vivekro073/enterprise-rag-analyzer.git](https://github.com/vivekro073/enterprise-rag-analyzer.git)
cd enterprise-rag-analyzer
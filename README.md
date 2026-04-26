# 🛠️ Bespoke RAG Architecture (From Scratch)

This repository houses a **fully custom-built** Retrieval-Augmented Generation (RAG) backend. Deliberately avoiding heavy, black-box frameworks (like LangChain or LlamaIndex), this system is engineered entirely from the ground up, component by component. By writing the ingestion, embedding, vector search, and LLM orchestration layers natively, this project achieves granular, absolute control over every step of the RAG pipeline—resulting in highly optimized, transparent, and tailor-made behavior.

## 🚀 Hand-Crafted Features

- **Custom PDF Ingestion & Purpose-Built Chunking:** Utilizes direct extraction via PyMuPDF (`fitz`) paired with a custom chunking algorithm tailored exactly to our retrieval needs—completely avoiding generic off-the-shelf text splitters.
- **Direct Embedding Orchestration:** Bare-metal integration with Hugging Face models, ensuring complete control over tokenization strategies and vector generation without intermediate abstractions.
- **Native Dual-Database Architecture:** A meticulously synced setup bridging raw vector similarity search in **Pinecone** with an **asynchronous PostgreSQL** (`asyncpg`) database acting as the absolute source of truth for complex document state and metadata.
- **Framework-less LLM Agent:** A hand-rolled, highly-specific LLM agent leveraging the Groq API. Context-injection, prompt engineering, and response synthesis are entirely custom-written for minimal latency and maximum precision.
- **Raw, High-Performance API:** Built directly on top of **FastAPI** for pure, zero-bloat asynchronous endpoints.

## 🛠️ Tech Stack

- **Framework:** FastAPI, Python 3.11+
- **Database:** PostgreSQL (asyncpg), Pinecone (Vector Search)
- **AI/ML:** Groq API (LLM Generation), HuggingFace (Embeddings)
- **Document Processing:** PyMuPDF (`fitz`)

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── agent/               # LLM integration and prompting (Groq)
│   ├── core/                # App configuration and exceptions
│   ├── db/                  # PostgreSQL database connections and models
│   ├── embedding/           # Logic for creating embeddings (HuggingFace)
│   ├── ingestion/           # Pipeline to chunk PDFs and orchestrate ingestion
│   └── pinecone_client/     # Pinecone vector DB connection and querying
```

## ⚙️ Setup & Installation

1. Create a virtual environment and activate it:
   ```bash
   python -m venv myenv
   myenv\Scripts\activate
   ```
2. Install dependencies (make sure your `requirements.txt` is updated):
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Set up your environment variables (e.g., in `backend/.env`):
   ```env
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_ENV=your_pinecone_environment
   GROQ_API_KEY=your_groq_api_key
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
   ```
4. Run the FastAPI development server:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

## 📖 How it Works

1. **Upload & Ingestion:** PDFs are submitted to the API, where `chunk_pdf.py` processes and breaks them up.
2. **Embedding:** `embedder.py` translates the text chunks into vector representations.
3. **Storage:** The raw text and metadata are saved in Postgres, while the vector embeddings are upserted into Pinecone.
4. **Querying:** When a user asks a question, the agent embeds the query, searches Pinecone for the most relevant context, and uses the LLM to formulate an informed response.

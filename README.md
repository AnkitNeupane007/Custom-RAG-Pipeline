# Custom RAG Project

This is a custom Retrieval-Augmented Generation (RAG) backend designed to process PDF documents, generate embeddings, and provide an intelligent LLM interface for querying the ingested data.

## 🚀 Features

- **PDF Ingestion & Chunking:** Extracts text from PDFs (using PyMuPDF/`fitz`) and splits it into manageable chunks for accurate retrieval.
- **Embeddings:** Uses Hugging Face models to generate highly relevant semantic embeddings for text chunks.
- **Vector Database:** Integrates with **Pinecone** to store and search through chunk embeddings efficiently.
- **Relational Database:** Uses asynchronous PostgreSQL (`asyncpg`) to manage document metadata and application state.
- **LLM Agent:** Leverages targeted LLM inference (via Groq) to generate accurate, context-aware answers based on the retrieved documents.
- **RESTful API:** Built with **FastAPI** to provide fast and fully-typed async endpoints.

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

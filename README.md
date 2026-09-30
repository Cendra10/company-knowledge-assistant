# Company Knowledge Assistant

## Description
Company Knowledge Assistant is a Retrieval-Augmented Generation (RAG) API that lets you ask questions across multiple company knowledge bases (KBs),such as HR and Engineering, and get answers grounded only in your own documents, complete with source citations. This project is focused on multi-KB retrieval, metadata filtering, and answer citation.

## Features
- Multi-Knowledge Base ingestion - each subfolder in `data/` is treated as a separate KB
- Automatic document processing: extract text from `.docx` files, chunk with overlap
- Vector storage and semantic search via ChromaDB
- Metadata filtering - restrict search to a specific KB (`source_kb`)
- LLM-generated answers grounded strictly in retrieved context (Groq API)
- Citation - every answer includes the source KB and filename it was drawn from
- Evaluation script to test retrieval and answer accuracy against expected keywords

## Tech Stack
- Python
- FastAPI
- ChromaDB (persistent vector database)
- python-docx (document text extraction)
- Groq API (OpenAI-compatible), model `openai/gpt-oss-20b`
- Pydantic (request/response schemas)

## Installation
```bash
git clone https://github.com/Cendra10/company-knowledge-assistant.git
cd company-knowledge-assistant
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_api_key_here
```

## Usage
1. Add your documents to `data/<kb_name>/` (e.g. `data/hr/`, `data/engineering/`) — `.docx` files only.
2. Start the server:
```bash
   uvicorn main:app --reload
```
3. Open `http://127.0.0.1:8000/docs` for the interactive Swagger UI.
4. Run `POST /ingest` to process all documents and store them in ChromaDB.
5. Run `POST /ask` with a question to get an answer with citations.

## Project Structure

```
company-knowledge-assistant/
    data/
        engineering/
    hr/
    chroma_db/      # generated automatically, not tracked in git
    main.py         # FastAPI endpoints (/ingest, /ask)
    ingestion.py    # document extraction, chunking, ingestion pipeline
    embeddings.py   # ChromaDB connection and storage
    rag.py          # retrieval with metadata filtering
    llm.py          # context building and LLM answer generation
    schemas.py      # Pydantic request/response models
    evaluation.py   # accuracy testing script
    requirements.txt
    .env            # not tracked in git
```

## Example
**Request** — `POST /ask`
```json
{
  "question": "How long before should employees submit a leave request?",
  "source_kb": "engineering"
}
```

**Response**
```json
{
  "answer": "Employees should submit a leave request at least four months in advance.",
  "citation": [
    {"source": "engineering", "filename": "leave-policy.docx"}
  ]
}
```

## Future Improvement
- Currently supports `.docx` files only — add support for PDF and TXT
- No automatic sync when a file is deleted from `data/` (old chunks remain in ChromaDB until manually cleared)
- Endpoints are synchronous; could be converted to async for better concurrency under load
- Evaluation results can vary slightly between runs due to LLM non-determinism
- Changing the chunk ID/metadata schema requires clearing `chroma_db/` and re-ingesting, since old records are not automatically migrated

## License
MIT
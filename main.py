from fastapi import FastAPI
from schemas import AskRequest, AskResponse
from ingestion import ingest
from embeddings import get_chroma_collection
from rag import retrieve_chunks

app = FastAPI()

@app.post("/ingest")
def ingest_endpoint():
    all_chunks, collection = ingest()
    return{"message": "Ingestion complete",
           "total_chunks": len(all_chunks)}

@app.post("/ask")
def ask_endpoint(request: AskRequest):
    collection = get_chroma_collection()
    answer = retrieve_chunks(collection, request.question, source_kb=request.source_kb)
    full_text = ",".join(answer)
    return AskResponse(answer=full_text)
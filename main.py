from fastapi import FastAPI
from schemas import AskRequest, AskResponse
from ingestion import ingest
from embeddings import get_chroma_collection
from rag import retrieve_chunks
from llm import ask_question

app = FastAPI()

@app.post("/ingest")
def ingest_endpoint():
    all_chunks = ingest()
    return{"message": "Ingestion complete",
           "total_chunks": len(all_chunks)}

@app.post("/ask")
def ask_endpoint(request: AskRequest):
    collection = get_chroma_collection()
    documents, metadatas = retrieve_chunks(collection, request.question, source_kb=request.source_kb)
    answer = ask_question(documents, request.question)
    return AskResponse(answer=answer, citation=metadatas)
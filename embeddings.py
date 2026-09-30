import chromadb

def get_chroma_collection():
    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_or_create_collection(name="my_collection")
    return collection

def save_to_chroma(collection, chunks, source_name, file_name):
    collection.delete(
        where={
            "$and":[
                {"source": source_name},
                {"filename": file_name}
                ]})

    ids = [f"{source_name}_{file_name}_{i}"
           for i in range(len(chunks))]
    collection.add(
        documents=[chunk["text"] for chunk in chunks],
        ids=ids,
        metadatas=[{"source": source_name, "filename": file_name} for _ in chunks]
    )
import chromadb

def get_chroma_collection():
    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_or_create_collection(name="my_collection")
    return collection

def save_to_chroma(collection, chunks, source_name):
    collection.delete(where={"source": source_name})

    ids = [f"{source_name}_{i}"
           for i in range(len(chunks))]
    collection.add(
        documents=[chunk["text"] for chunk in chunks],
        ids=ids,
        metadatas=[{"source": source_name} for _ in chunks]
    )

if __name__ == "__main__":
    collection = get_chroma_collection()
    save_to_chroma(collection, all_chunks, "engineering")
    print("Saved:", collection.count())
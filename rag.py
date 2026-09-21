def retrieve_chunks(collection, query, n_results=3):
    query_result=collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return query_result['documents'][0]

if __name__ == "__main__":
    from embeddings import get_chroma_collection
    collection = get_chroma_collection()
    result = retrieve_chunks(collection, "berapa lama sebelum mengajukan cuti ?")
    print(result)
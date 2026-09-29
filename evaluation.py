from rag import retrieve_chunks
from embeddings import get_chroma_collection
from llm import ask_question

test_cases = [
    {"question": "How long before should employees submit a leave request?", "expected_keyword": "months", "source_kb": "engineering"},
    {"question": "What does the HR dummy document contain?", "expected_keyword": "dummy", "source_kb": "hr"},
    {"question": "When do employees receive their salary?", "expected_keyword": "25", "source_kb": "hr"}
]

collection = get_chroma_collection()

for case in test_cases:
    documents, metadatas = retrieve_chunks(collection, case["question"],source_kb=case["source_kb"])
    answer = ask_question(documents, case["question"])

    print(repr(answer))

    if case["expected_keyword"] in answer:
        print("pas:", case["question"])
    else:
        print("fail:", case["question"], "-> answer:", answer)
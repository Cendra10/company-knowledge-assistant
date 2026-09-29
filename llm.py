from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client= OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def build_context(chunks):
    result_chunks=""
    max_char=8000

    for item in chunks:
        result_chunks += item + "\n\n"

        if len(result_chunks) > max_char:
            break
    return result_chunks

def ask_question(metadata, question):
    context=build_context(metadata)
    print(f"CONTEXT: {context}")

    prompt = [
        {"role": "system", "content": "Jawab HANYA berdasarkan context dan menjawab singkat menggunakan Bahasa Indonesia."}
    ]

    prompt.append({
        "role": "user", "content": f"Context:\n{context}\n\nPertanyaan:{question}"
    })

    result_question= client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=prompt
    )
    return result_question.choices[0].message.content
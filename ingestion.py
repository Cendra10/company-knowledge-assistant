from pathlib import Path
import io
from docx import Document
from zipfile import BadZipFile
from fastapi import HTTPException
from docx.opc.exceptions import PackageNotFoundError

#Extract text dari file
def extract_text_from_docx(contents):
    docx_list = []
    try:
          doc = Document(io.BytesIO(contents))
          for para in doc.paragraphs:
               docx_list.append(para.text)
    except (PackageNotFoundError, BadZipFile):
          raise HTTPException(
              status_code=400,
              detail="Invalid or corrupted DOCX file."
        )
    full_text = ",".join(docx_list)
    return full_text

def chunk_text(text, source_kb, filename, chunk_size=500, overlap=100):
    result = []
    start = 0
    while start < len(text):
          end = start + chunk_size
          chunk = text[start:end]
          result.append({"text": chunk, "source": source_kb, "filename": filename})
          start = end-overlap
    return result

all_chunks = []
#Scan Folder & dapatkan nama KB
for source_kb in Path("data").iterdir():
        if source_kb.is_dir():
            for file in source_kb.iterdir():
                print (source_kb.name, file.name)
                text = extract_text_from_docx(file.read_bytes())
                chunks = chunk_text(text, source_kb.name, file.name)
                all_chunks.extend(chunks)
                print(all_chunks)
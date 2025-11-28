import os
from PyPDF2 import PdfReader
from docx import Document

def load_text_file(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def load_pdf_file(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def load_docx_file(path):
    doc = Document(path)
    text = "\n".join([p.text for p in doc.paragraphs])
    return text

def load_file(path):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".txt":
        return load_text_file(path)

    elif ext == ".pdf":
        return load_pdf_file(path)

    elif ext == ".docx":
        return load_docx_file(path)

    else:
        raise ValueError("Unsupported file type: " + ext)

import os
import pandas as pd
from PyPDF2 import PdfReader


def parse_document(file_path: str):
    """
    Detects file type and extracts raw content.
    No interpretation here.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError("File does not exist")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return _parse_pdf(file_path)

    if ext == ".csv":
        return _parse_csv(file_path)

    raise ValueError("Unsupported file type")


def _parse_pdf(file_path: str):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return {
        "type": "pdf",
        "content": text,
        "pages": len(reader.pages)
    }


def _parse_csv(file_path: str):
    df = pd.read_csv(file_path)

    return {
        "type": "csv",
        "rows": len(df),
        "columns": list(df.columns),
        "preview": df.head(5).to_dict(orient="records")
    }


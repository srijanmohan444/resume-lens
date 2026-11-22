import io
import re


def extract_text(filename: str, data: bytes) -> str:
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    if ext == "pdf":
        import pdfplumber
        try:
            with pdfplumber.open(io.BytesIO(data)) as pdf:
                text = "\n".join((p.extract_text() or "") for p in pdf.pages[:6])
        except Exception:
            raise ValueError("This PDF could not be opened. Re-export it from Word or Google Docs and try again.")
    elif ext == "docx":
        import docx
        try:
            d = docx.Document(io.BytesIO(data))
        except Exception:
            raise ValueError("This DOCX could not be opened. Save it again as .docx and retry.")
        parts = [p.text for p in d.paragraphs]
        for t in d.tables:
            for row in t.rows:
                parts.append(" | ".join(c.text for c in row.cells))
        text = "\n".join(parts)
    elif ext == "txt":
        text = data.decode("utf-8", errors="ignore")
    else:
        raise ValueError("Upload a PDF, DOCX or TXT file.")

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if len(text) < 200:
        raise ValueError("Very little text was found. If this is a scanned or image-only PDF, upload a text-based version.")
    return text[:15000]

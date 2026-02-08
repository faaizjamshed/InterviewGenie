import PyPDF2
import docx2txt
import os


def extract_text(filepath):
    """
    Extract text safely from PDF, DOCX, TXT.
    Never crashes server — always returns text.
    """

    if not os.path.exists(filepath):
        return "File not found."

    try:
        ext = filepath.rsplit('.', 1)[-1].lower()

        # ===== PDF =====
        if ext == "pdf":
            text = ""
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ""
            return text.strip() or "PDF read but no text found."

        # ===== DOCX =====
        elif ext == "docx":
            text = docx2txt.process(filepath)
            return text.strip() or "DOCX read but empty."

        # ===== TXT =====
        elif ext == "txt":
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                return f.read().strip()

        else:
            return "Unsupported file format."

    except Exception as e:
        print("TEXT EXTRACT ERROR:", e)
        return "Resume uploaded but extraction failed."

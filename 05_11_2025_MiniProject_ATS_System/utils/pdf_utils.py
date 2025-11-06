import PyPDF2
from io import BytesIO

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text from PDF bytes using PyPDF2.
    Mirrors the behavior from your original monolithic file.
    """
    try:
        pdf_file = BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            # PyPDF2's extract_text() may return None on some pages — handle that
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        # Keep same behavior as original: print error and return empty string
        print(f"Error extracting PDF: {e}")
        return ""

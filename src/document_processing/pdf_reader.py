
from pathlib import Path
from pypdf import PdfReader


def extract_pages_from_pdf(file_path: str) -> list[dict]:
    """Extract text from a PDF while preserving page numbers."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {file_path}")

    reader = PdfReader(str(path))
    extracted_pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if page_text and page_text.strip():
            extracted_pages.append({
                "page": page_number,
                "text": page_text.strip(),
                "source": path.name,
            })

    return extracted_pages


def extract_text_from_pdf(file_path: str) -> str:
    """Extract PDF text as a single string for compatibility."""

    pages = extract_pages_from_pdf(file_path)

    return "\n\n".join(
        f"[Page {page['page']}]\n{page['text']}"
        for page in pages
    )

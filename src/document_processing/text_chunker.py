
import re


def chunk_pages(
    pages: list[dict],
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[dict]:
    """Split PDF pages into chunks while preserving source metadata."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size")

    all_chunks = []

    for page in pages:
        text = re.sub(r"\s+", " ", page["text"]).strip()

        if not text:
            continue

        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))

            all_chunks.append({
                "text": text[start:end],
                "page": page["page"],
                "source": page["source"],
            })

            if end == len(text):
                break

            start = end - overlap

    return all_chunks

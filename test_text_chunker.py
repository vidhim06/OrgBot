
from src.document_processing.pdf_reader import extract_pages_from_pdf
from src.document_processing.text_chunker import chunk_pages

pages = extract_pages_from_pdf("data/sample.pdf")
chunks = chunk_pages(pages)

print(f"Total chunks created: {len(chunks)}")

for index, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {index} ---")
    print(f"Source: {chunk['source']}")
    print(f"Page: {chunk['page']}")
    print(f"Text ({len(chunk['text'])} characters):")
    print(chunk["text"])

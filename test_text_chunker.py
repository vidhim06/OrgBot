
from src.document_processing.pdf_reader import extract_text_from_pdf
from src.document_processing.text_chunker import chunk_text

# Step 1: Extract text from the sample PDF
text = extract_text_from_pdf("data/sample.pdf")

# Step 2: Split the text into chunks
chunks = chunk_text(text, chunk_size=500, overlap=50)

# Step 3: Display the results
print(f"Total chunks created: {len(chunks)}")

for i, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {i} ({len(chunk)} characters) ---")
    print(chunk)

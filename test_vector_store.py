
from src.document_processing.pdf_reader import extract_pages_from_pdf
from src.document_processing.text_chunker import chunk_pages
from src.document_processing.embedding_model import generate_embeddings
from src.document_processing.vector_store import VectorStore


# Read the sample PDF and create chunks.
pages = extract_pages_from_pdf("data/sample.pdf")
chunks = chunk_pages(pages)

# Create an embedding for every chunk.
texts = [chunk["text"] for chunk in chunks]
embeddings = generate_embeddings(texts)

# Store the chunks and embeddings.
store = VectorStore()
store.add_chunks(chunks, embeddings)

# Search using a question about the scholarship deadline.
question = "Scholarship ke liye apply karne ki last date kya hai?"
query_embedding = generate_embeddings([question])[0]

results = store.search(query_embedding, n_results=3)

print("Search question:", question)
print("\nRetrieved results:")

for result in results:
    print(f"\nSource: {result['source']}, Page: {result['page']}")
    print(f"Distance: {result['distance']:.4f}")
    print(result["text"][:300])

assert results, "No results were retrieved."
assert any("scholarship" in item["text"].lower() for item in results)

print("\nVector store test passed!")

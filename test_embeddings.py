
from src.document_processing.embedding_model import generate_embeddings


texts = [
    "Scholarship applications are open from 1 November to 20 November 2026.",
    "The end-semester examinations begin on 7 December 2026.",
]

embeddings = generate_embeddings(texts)

print("Number of texts:", len(embeddings))
print("Dimensions of first embedding:", len(embeddings[0]))
print("First embedding sample:", embeddings[0][:5])

assert len(embeddings) == 2
assert len(embeddings[0]) > 0
assert len(embeddings[0]) == len(embeddings[1])

print("Embedding test passed!")

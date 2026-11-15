
from src.document_processing.embedding_model import generate_embeddings
from src.document_processing.vector_store import VectorStore
from src.generation.answer_generator import generate_answer


def answer_question(question: str, organisation_id: int) -> dict:
    """Retrieve relevant chunks from the logged-in organisation."""

    if not question.strip():
        return {
            "answer": "Please enter a question.",
            "sources": [],
        }

    # Convert question into an embedding
    query_embedding = generate_embeddings([question])[0]

    # Search only this organisation's documents
    store = VectorStore()
    retrieved_chunks = store.search(
        query_embedding,
        organisation_id=organisation_id,
        n_results=3
    )

    # Generate answer with sources
    return generate_answer(question, retrieved_chunks)

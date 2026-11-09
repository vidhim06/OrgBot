
from src.document_processing.embedding_model import generate_embeddings
from src.document_processing.vector_store import VectorStore
from src.generation.answer_generator import generate_answer


def answer_question(question: str) -> dict:
    """Retrieve relevant document chunks and return an answer with sources."""

    if not question.strip():
        return {
            "answer": "Please enter a question.",
            "sources": [],
        }

    # Convert the user's question into an embedding.
    query_embedding = generate_embeddings([question])[0]

    # Search the existing ChromaDB collection.
    store = VectorStore()
    retrieved_chunks = store.search(query_embedding, n_results=3)

    # Return the answer and its source information.
    return generate_answer(question, retrieved_chunks)

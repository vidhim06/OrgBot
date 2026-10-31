
import time

from src.document_processing.embedding_model import generate_embeddings
from src.document_processing.vector_store import VectorStore
from src.generation.answer_generator import generate_answer


def answer_question(question: str) -> dict:

    if not question.strip():
        return {
            "answer": "Please enter a question.",
            "sources": []
        }

    start = time.time()

    # Step 1: Generate embedding
    step_start = time.time()
    query_embedding = generate_embeddings([question])[0]
    print("Embedding time:", round(time.time() - step_start, 2), "seconds")

    # Step 2: Retrieve relevant chunks
    step_start = time.time()
    store = VectorStore()
    retrieved_chunks = store.search(query_embedding, n_results=3)
    print("Retrieval time:", round(time.time() - step_start, 2), "seconds")

    # Step 3: Generate AI answer
    step_start = time.time()
    result = generate_answer(question, retrieved_chunks)
    print("Gemini time:", round(time.time() - step_start, 2), "seconds")

    print("Total time:", round(time.time() - start, 2), "seconds")

    return result

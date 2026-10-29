
from src.document_processing.embedding_model import generate_embeddings
from src.document_processing.vector_store import VectorStore


store = VectorStore()

test_cases = [
    {
        "question": "What is the last date to apply for the scholarship?",
        "expected_phrase": "20 november 2026",
    },
    {
        "question": "Scholarship ke liye last date kya hai?",
        "expected_phrase": "20 november 2026",
    },
    {
        "question": "When do end-semester examinations begin?",
        "expected_phrase": "7 december 2026",
    },
    {
        "question": "What are the library opening hours?",
        "expected_phrase": "9:00 am to 5:00 pm",
    },
    {
        "question": "Where is the student support desk?",
        "expected_phrase": "room a-104",
    },
]

passed = 0

for case in test_cases:
    question = case["question"]
    expected = case["expected_phrase"].lower()

    query_embedding = generate_embeddings([question])[0]
    results = store.search(query_embedding, n_results=1)

    top_text = results[0]["text"].lower() if results else ""
    success = expected in top_text

    if success:
        passed += 1

    print(f"\nQuestion: {question}")
    print(f"Expected phrase: {expected}")
    print(f"Top-1 result: {'PASS' if success else 'FAIL'}")

    if results:
        print(f"Retrieved text: {top_text[:200]}")

print(f"\nTop-1 evaluation: {passed}/{len(test_cases)} passed")

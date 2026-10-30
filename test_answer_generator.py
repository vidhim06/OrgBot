
from src.generation.answer_generator import generate_answer


def test_answer_with_source():
    chunks = [
        {
            "text": "Scholarship applications close on 20 November 2026.",
            "source": "sample.pdf",
            "page": 1,
        }
    ]

    result = generate_answer("What is the scholarship deadline?", chunks)

    assert "20 November 2026" in result["answer"]
    assert result["sources"][0]["file"] == "sample.pdf"
    assert result["sources"][0]["page"] == 1


def test_answer_when_no_chunks():
    result = generate_answer("Unknown question", [])

    assert result["sources"] == []
    assert "could not find" in result["answer"].lower()


if __name__ == "__main__":
    test_answer_with_source()
    test_answer_when_no_chunks()
    print("All answer-generator tests passed!")

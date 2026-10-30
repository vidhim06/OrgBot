
from src.generation.qa_pipeline import answer_question


def test_scholarship_question():
    result = answer_question(
        "Scholarship ke liye last date kya hai?"
    )

    assert "20 november 2026" in result["answer"].lower()
    assert result["sources"]
    assert result["sources"][0]["file"] == "sample.pdf"


if __name__ == "__main__":
    test_scholarship_question()
    print("QA pipeline test passed!")

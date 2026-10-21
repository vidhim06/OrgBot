
from sentence_transformers import SentenceTransformer


# A small multilingual model that supports English and many other languages.
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

_model = None


def get_embedding_model():
    """Load the embedding model once and reuse it."""

    global _model

    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Convert a list of text strings into numerical vectors."""

    if not texts:
        return []

    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return embeddings.tolist()

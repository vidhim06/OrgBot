
import chromadb
from uuid import uuid4


class VectorStore:
    """Store and search document chunks separately by organisation."""

    def __init__(self, collection_name: str = "orgbot_saas_documents"):
        self.client = chromadb.PersistentClient(
            path="data/chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(
        self,
        chunks: list[dict],
        embeddings: list[list[float]],
        organisation_id: int,
    ) -> None:
        """Save document chunks with organisation-specific metadata."""

        if len(chunks) != len(embeddings):
            raise ValueError(
                "The number of chunks must match the number of embeddings."
            )

        if not chunks:
            return

        upload_id = uuid4().hex

        ids = [
            f"{organisation_id}-{upload_id}-chunk{i}"
            for i in range(len(chunks))
        ]

        self.collection.upsert(
            ids=ids,
            documents=[chunk["text"] for chunk in chunks],
            embeddings=embeddings,
            metadatas=[
                {
                    "source": chunk["source"],
                    "page": chunk["page"],
                    "organisation_id": organisation_id,
                }
                for chunk in chunks
            ],
        )

    def search(
        self,
        query_embedding: list[float],
        organisation_id: int,
        n_results: int = 3,
    ) -> list[dict]:
        """Search only documents belonging to the given organisation."""

        total = self.collection.count()

        if total == 0:
            return []

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, total),
            where={"organisation_id": organisation_id},
        )

        matches = []

        for i, text in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][i]

            matches.append({
                "text": text,
                "source": metadata["source"],
                "page": metadata["page"],
                "distance": results["distances"][0][i],
            })

        return matches

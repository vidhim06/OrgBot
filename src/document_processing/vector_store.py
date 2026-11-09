
import chromadb

from uuid import uuid4
class VectorStore:
    """Store and search document chunks using ChromaDB."""

    def __init__(self, collection_name: str = "orgbot_documents"):
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
    ) -> None:
        """Save chunks, embeddings, and their source metadata."""

        if len(chunks) != len(embeddings):
            raise ValueError(
                "The number of chunks must match the number of embeddings."
            )

        if not chunks:
            return

        upload_id = uuid4().hex

        ids = [
            f"{upload_id}-chunk{i}"
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
                }
                for chunk in chunks
            ],
        )

    def search(
        self,
        query_embedding: list[float],
        n_results: int = 3,
    ) -> list[dict]:
        """Find the most relevant chunks for a query."""

        total = self.collection.count()

        if total == 0:
            return []

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, total),
        )

        matches = []

        for i, text in enumerate(results["documents"][0]):
            matches.append({
                "text": text,
                "source": results["metadatas"][0][i]["source"],
                "page": results["metadatas"][0][i]["page"],
                "distance": results["distances"][0][i],
            })

        return matches

    def reset(self) -> None:
        """Delete and recreate the collection for a fresh indexing run."""

        collection_name = self.collection.name
        self.client.delete_collection(collection_name)

        self.collection = self.client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )


import chromadb


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

        ids = [
            f"{chunk['source']}-page{chunk['page']}-chunk{i}"
            for i, chunk in enumerate(chunks)
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

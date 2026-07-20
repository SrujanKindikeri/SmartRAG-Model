from database import VectorDatabase
from embeddings import EmbeddingGenerator
from config import TOP_K


class SemanticSearch:
    """
    Performs semantic search on the Chroma vector database.
    """

    def __init__(self):
        self.db = VectorDatabase()
        self.embedder = EmbeddingGenerator()

    def search(self, question, top_k=TOP_K):

        # Create embedding for user question
        query_embedding = self.embedder.embed_text(question)

        # Query ChromaDB
        results = self.db.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        retrieved = []

        for document, metadata, distance in zip(
                documents,
                metadatas,
                distances):

            retrieved.append({
                "text": document,
                "filename": metadata["filename"],
                "chunk_id": metadata["chunk_id"],
                "score": round(1 - distance, 4)
            })

        return retrieved
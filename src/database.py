import chromadb
from config import VECTOR_DB_DIR, COLLECTION_NAME


class VectorDatabase:
    """
    Handles all interactions with the ChromaDB vector database.
    """

    def __init__(self):
        print("Initializing ChromaDB...")

        self.client = chromadb.PersistentClient(
            path=str(VECTOR_DB_DIR)
        )

        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={
                "description": "SmartRAG Knowledge Base"
            }
        )

        print(f"Collection Loaded: {COLLECTION_NAME}")

    # --------------------------------------------------------
    # Add Chunks
    # --------------------------------------------------------

    def add_chunks(self, chunks, embeddings):
        """
        Add document chunks and embeddings to ChromaDB.
        """

        if not chunks:
            print("No chunks to store.")
            return

        ids = []
        documents = []
        metadatas = []

        for chunk in chunks:

            chunk_id = chunk["chunk_id"]

            ids.append(str(chunk_id))

            documents.append(chunk["text"])

            metadatas.append({
                "filename": chunk["filename"],
                "path": chunk["path"],
                "chunk_id": chunk["chunk_id"]
            })

        try:
            self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )

            print(f"Stored {len(chunks)} chunks.")

        except Exception as e:
            print("Database Error:", e)

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    def search(self, query_embedding, top_k):

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results

    # --------------------------------------------------------
    # Count Vectors
    # --------------------------------------------------------

    def count(self):

        return self.collection.count()

    # --------------------------------------------------------
    # Reset Database
    # --------------------------------------------------------

    def clear(self):

        self.client.delete_collection(COLLECTION_NAME)

        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME
        )

        print("Knowledge Base Cleared.")

    # --------------------------------------------------------
    # Database Information
    # --------------------------------------------------------

    def info(self):

        print("=" * 50)
        print("SmartRAG Database")
        print("=" * 50)
        print(f"Collection : {COLLECTION_NAME}")
        print(f"Vectors    : {self.count()}")
        print("=" * 50)
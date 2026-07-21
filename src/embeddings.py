"""
=========================================================
SmartRAG Embedding Generator
=========================================================

Features
--------
✓ Singleton Model Loading
✓ Batch Embedding Generation
✓ Query Embeddings
✓ Normalized Embeddings
✓ Production Ready
=========================================================
"""

from typing import List

from sentence_transformers import SentenceTransformer

from config import (
    EMBEDDING_MODEL,
    EMBEDDING_BATCH_SIZE
)


class EmbeddingGenerator:

    _model = None

    def __init__(self):

        if EmbeddingGenerator._model is None:

            print("=" * 60)
            print(f"Loading Embedding Model : {EMBEDDING_MODEL}")
            print("=" * 60)

            EmbeddingGenerator._model = SentenceTransformer(
                EMBEDDING_MODEL
            )

        self.model = EmbeddingGenerator._model

    # =====================================================
    # Embed Multiple Chunks
    # =====================================================

    def embed_chunks(
        self,
        chunks: List[dict]
    ) -> List[List[float]]:

        texts = [

            chunk["text"]

            for chunk in chunks

        ]

        embeddings = self.model.encode(

            texts,

            batch_size=EMBEDDING_BATCH_SIZE,

            convert_to_numpy=True,

            normalize_embeddings=True,

            show_progress_bar=True

        )

        return embeddings.tolist()

    # =====================================================
    # Embed Multiple Text Strings
    # =====================================================

    def embed_texts(
        self,
        texts: List[str]
    ) -> List[List[float]]:

        embeddings = self.model.encode(

            texts,

            batch_size=EMBEDDING_BATCH_SIZE,

            convert_to_numpy=True,

            normalize_embeddings=True,

            show_progress_bar=False

        )

        return embeddings.tolist()

    # =====================================================
    # Embed Single Query
    # =====================================================

    def embed_query(
        self,
        query: str
    ) -> List[float]:

        embedding = self.model.encode(

            query,

            convert_to_numpy=True,

            normalize_embeddings=True

        )

        return embedding.tolist()

    # =====================================================
    # Embed Single Text
    # =====================================================

    def embed_text(
        self,
        text: str
    ) -> List[float]:

        embedding = self.model.encode(

            text,

            convert_to_numpy=True,

            normalize_embeddings=True

        )

        return embedding.tolist()

    # =====================================================
    # Embedding Dimension
    # =====================================================

    def embedding_dimension(self):

        return self.model.get_sentence_embedding_dimension()

    # =====================================================
    # Model Information
    # =====================================================

    def info(self):

        return {

            "model": EMBEDDING_MODEL,

            "dimension": self.embedding_dimension(),

            "batch_size": EMBEDDING_BATCH_SIZE

        }

    # =====================================================
    # Print Information
    # =====================================================

    def print_info(self):

        info = self.info()

        print("\n" + "=" * 60)
        print("Embedding Model")
        print("=" * 60)

        print(f"Model      : {info['model']}")
        print(f"Dimension  : {info['dimension']}")
        print(f"Batch Size : {info['batch_size']}")

        print("=" * 60)

    # =====================================================
    # Health Check
    # =====================================================

    def health(self):

        try:

            dimension = self.embedding_dimension()

            return {

                "status": "healthy",

                "model": EMBEDDING_MODEL,

                "dimension": dimension

            }

        except Exception as e:

            return {

                "status": "error",

                "message": str(e)

            }


# =========================================================
# Testing
# =========================================================

if __name__ == "__main__":

    embedder = EmbeddingGenerator()

    embedder.print_info()

    sample = "What is the minimum attendance required?"

    vector = embedder.embed_query(sample)

    print()

    print("Embedding Length :", len(vector))

    print("First 10 Values :")

    print(vector[:10])

    print()

    print(embedder.health())
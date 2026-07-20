from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL


class EmbeddingGenerator:
    """
    Generates embeddings using SentenceTransformer.
    """

    _model = None

    def __init__(self):

        if EmbeddingGenerator._model is None:
            print("=" * 60)
            print(f"Loading Embedding Model: {EMBEDDING_MODEL}")
            print("=" * 60)

            EmbeddingGenerator._model = SentenceTransformer(
                EMBEDDING_MODEL
            )

        self.model = EmbeddingGenerator._model

    # --------------------------------------------------------
    # Single Text Embedding
    # --------------------------------------------------------

    def embed_text(self, text):

        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding.tolist()

    # --------------------------------------------------------
    # Batch Embeddings
    # --------------------------------------------------------

    def embed_chunks(self, chunks):

        if not chunks:
            return []

        print(f"Generating embeddings for {len(chunks)} chunks...")

        texts = [chunk["text"] for chunk in chunks]

        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            normalize_embeddings=True
        )

        return embeddings.tolist()

    # --------------------------------------------------------
    # Embedding Dimension
    # --------------------------------------------------------

    def embedding_dimension(self):

        return self.model.get_sentence_embedding_dimension()

    # --------------------------------------------------------
    # Model Information
    # --------------------------------------------------------

    def info(self):

        print("=" * 60)
        print("Embedding Model Information")
        print("=" * 60)
        print(f"Model      : {EMBEDDING_MODEL}")
        print(f"Dimension  : {self.embedding_dimension()}")
        print("=" * 60)
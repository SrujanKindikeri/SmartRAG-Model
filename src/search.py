"""
=========================================================
SmartRAG Search Engine
=========================================================

Pipeline

User Query
     │
     ▼
Embedding
     │
     ▼
ChromaDB Search
     │
     ▼
Filter Results
     │
     ▼
Remove Duplicates
     │
     ▼
Build Context

=========================================================
"""

from embeddings import EmbeddingGenerator
from database import VectorDatabase

from config import TOP_K


class SearchEngine:

    def __init__(self):

        self.embedder = EmbeddingGenerator()

        self.database = VectorDatabase()

    # =====================================================
    # Generate Query Embedding
    # =====================================================

    def embed_query(
        self,
        query: str
    ):

        return self.embedder.embed_query(query)

    # =====================================================
    # Semantic Search
    # =====================================================

    def search(
        self,
        query: str,
        top_k: int = TOP_K
    ):

        embedding = self.embed_query(query)

        return self.database.search(

            query_embedding=embedding,

            top_k=top_k

        )

    # =====================================================
    # Score Filtering
    # =====================================================

    def search_with_threshold(

        self,

        query,

        top_k=TOP_K,

        max_distance=1.5

    ):

        results = self.search(

            query,

            top_k

        )

        filtered = []

        for item in results:

            # Smaller distance = better match
            if item["score"] <= max_distance:

                filtered.append(item)

        return filtered
    # =====================================================
    # Remove Duplicate Results
    # =====================================================

    def remove_duplicates(
        self,
        results
    ):

        unique_results = []
        seen = set()

        for item in results:

            text = item.get("text", "").strip()

            if not text:
                continue

            if text in seen:
                continue

            seen.add(text)
            unique_results.append(item)

        return unique_results

    # =====================================================
    # Extract Source Files
    # =====================================================

    def get_sources(
        self,
        results
    ):

        sources = []
        seen = set()

        for item in results:

            filename = item.get("filename", "Unknown")

            if filename not in seen:

                seen.add(filename)
                sources.append(filename)

        return sources

    # =====================================================
    # Build Context
    # =====================================================

    def build_context(
        self,
        results
    ):

        if not results:

            return ""

        context = []

        for index, item in enumerate(results, start=1):

            context.append(f"[Document {index}]")

            context.append(
                f"Source: {item.get('filename', 'Unknown')}"
            )

            context.append("")

            context.append(
                item.get("text", "")
            )

            context.append("\n")

        return "\n".join(context)

    # =====================================================
    # Print Search Results
    # =====================================================

    def print_results(
        self,
        results
    ):

        print("\n" + "=" * 70)
        print("Search Results")
        print("=" * 70)

        if not results:

            print("No matching documents found.")
            print("=" * 70)

            return

        for index, item in enumerate(results, start=1):

            print(f"\nResult #{index}")
            print("-" * 70)

            print(
                f"File  : {item.get('filename', 'Unknown')}"
            )

            print(
                f"Chunk : {item.get('chunk_number', 0)}"
            )

            print(
                f"Distance : {item.get('score', 0):.4f}"
            )

            preview = item.get("text", "")[:250]

            if len(item.get("text", "")) > 250:

                preview += "..."

            print("\nPreview\n")

            print(preview)

        print("=" * 70)
    # =====================================================
    # Complete Retrieval Pipeline
    # =====================================================

    def retrieve(
        self,
        query: str,
        top_k: int = TOP_K,
        max_distance: float = 1.5
    ):

        results = self.search_with_threshold(
            query=query,
            top_k=top_k,
            max_distance=max_distance
        )

        results = self.remove_duplicates(results)

        context = self.build_context(results)

        sources = self.get_sources(results)

        return {
            "query": query,
            "results": results,
            "context": context,
            "sources": sources,
            "count": len(results)
        }

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self):

        return {

            "embedding_model": self.embedder.info()["model"],

            "embedding_dimension": self.embedder.embedding_dimension(),

            "database_vectors": self.database.count(),

            "top_k": TOP_K

        }

    # =====================================================
    # Print Statistics
    # =====================================================

    def print_statistics(self):

        stats = self.statistics()

        print("\n" + "=" * 60)
        print("Search Engine Statistics")
        print("=" * 60)

        print(
            f"Embedding Model     : {stats['embedding_model']}"
        )

        print(
            f"Embedding Dimension : {stats['embedding_dimension']}"
        )

        print(
            f"Stored Vectors      : {stats['database_vectors']}"
        )

        print(
            f"Default TOP-K       : {stats['top_k']}"
        )

        print("=" * 60)

    # =====================================================
    # Health Check
    # =====================================================

    def health(self):

        try:

            return {

                "status": "healthy",

                "database": self.database.test_connection(),

                "vectors": self.database.count(),

                "embedding_dimension": self.embedder.embedding_dimension()

            }

        except Exception as e:

            return {

                "status": "error",

                "message": str(e)

            }

    # =====================================================
    # Print Health
    # =====================================================

    def print_health(self):

        health = self.health()

        print("\n" + "=" * 60)
        print("Search Engine Health")
        print("=" * 60)

        for key, value in health.items():

            print(f"{key.capitalize():22}: {value}")

        print("=" * 60)

    # =====================================================
    # Search & Print
    # =====================================================

    def search_and_print(
        self,
        query: str,
        top_k: int = TOP_K
    ):

        output = self.retrieve(
            query=query,
            top_k=top_k
        )

        self.print_results(output["results"])

        print("\nSources")

        if output["sources"]:

            for source in output["sources"]:

                print(f" - {source}")

        else:

            print("No sources found.")

        print()

        print("Context Length :", len(output["context"]))

        return output
# =====================================================
# Testing
# =====================================================

if __name__ == "__main__":

    search = SearchEngine()

    search.print_statistics()

    search.print_health()

    while True:

        print()

        query = input("Search > ").strip()

        if query.lower() in ["exit", "quit"]:

            break

        search.search_and_print(query)

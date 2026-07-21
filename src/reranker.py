"""
=========================================================
SmartRAG Reranker
=========================================================

Pipeline

Search Results
      │
      ▼
Create (Query, Chunk) Pairs
      │
      ▼
CrossEncoder
      │
      ▼
Assign Scores
      │
      ▼
Sort by Relevance

=========================================================
"""

from sentence_transformers import CrossEncoder

from config import (
    RERANK_MODEL,
    RERANK_TOP_K
)


class Reranker:

    _model = None

    def __init__(self):

        if Reranker._model is None:

            print("\nLoading CrossEncoder...")

            Reranker._model = CrossEncoder(
                RERANK_MODEL
            )

            print("CrossEncoder Loaded.")

        self.model = Reranker._model

    # =====================================================
    # Predict Relevance Scores
    # =====================================================

    def score(
        self,
        query,
        results
    ):

        if not results:

            return []

        pairs = [

            (
                query,
                item.get("text", "")
            )

            for item in results

        ]

        scores = self.model.predict(
            pairs
        )

        reranked = []

        for item, score in zip(results, scores):

            data = dict(item)

            data["rerank_score"] = float(score)

            reranked.append(data)

        return reranked

    # =====================================================
    # Sort Results
    # =====================================================

    def rerank(
        self,
        query,
        results,
        top_k=RERANK_TOP_K
    ):

        reranked = self.score(
            query,
            results
        )

        reranked.sort(

            key=lambda x: x["rerank_score"],

            reverse=True

        )

        return reranked[:top_k]
    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self):

        return {

            "model": RERANK_MODEL,

            "top_k": RERANK_TOP_K

        }

    # =====================================================
    # Print Statistics
    # =====================================================

    def print_statistics(self):

        stats = self.statistics()

        print("\n" + "=" * 60)
        print("Reranker Statistics")
        print("=" * 60)

        print(f"CrossEncoder Model : {stats['model']}")
        print(f"Default TOP-K      : {stats['top_k']}")

        print("=" * 60)

    # =====================================================
    # Health Check
    # =====================================================

    def health(self):

        try:

            return {

                "status": "healthy",

                "model": RERANK_MODEL,

                "loaded": self.model is not None

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
        print("Reranker Health")
        print("=" * 60)

        for key, value in health.items():

            print(f"{key.capitalize():15}: {value}")

        print("=" * 60)

    # =====================================================
    # Pretty Print Results
    # =====================================================

    def print_results(
        self,
        results
    ):

        print("\n" + "=" * 70)
        print("Reranked Results")
        print("=" * 70)

        if not results:

            print("No results available.")
            print("=" * 70)
            return

        for i, item in enumerate(results, start=1):

            print(f"\nRank #{i}")
            print("-" * 70)

            print(
                f"File          : {item.get('filename', 'Unknown')}"
            )

            print(
                f"Chunk         : {item.get('chunk_number', 0)}"
            )

            print(
                f"Cross Score   : {item.get('rerank_score', 0):.4f}"
            )

            if "score" in item:

                print(
                    f"Vector Score  : {item.get('score', 0):.4f}"
                )

            preview = item.get("text", "")[:250]

            if len(item.get("text", "")) > 250:

                preview += "..."

            print("\nPreview\n")
            print(preview)

        print("=" * 70)

    # =====================================================
    # Complete Pipeline
    # =====================================================

    def rerank_and_print(
        self,
        query,
        results,
        top_k=RERANK_TOP_K
    ):

        reranked = self.rerank(
            query=query,
            results=results,
            top_k=top_k
        )

        self.print_results(reranked)

        return reranked
# =====================================================
# Testing
# =====================================================

if __name__ == "__main__":

    from search import SearchEngine

    search = SearchEngine()

    reranker = Reranker()

    reranker.print_statistics()

    reranker.print_health()

    while True:

        print()

        query = input("Query > ").strip()

        if query.lower() in ["exit", "quit"]:

            break

        retrieved = search.retrieve(query)

        reranked = reranker.rerank(
            query=query,
            results=retrieved["results"]
        )

        reranker.print_results(reranked)
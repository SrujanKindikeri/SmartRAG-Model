from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self):
        print("Loading Cross Encoder...")

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(self, question, search_results, top_n=5):

        if not search_results:
            return []

        pairs = [
            (question, result["text"])
            for result in search_results
        ]

        scores = self.model.predict(pairs)

        ranked = list(zip(search_results, scores))
        ranked.sort(key=lambda x: x[1], reverse=True)

        return [item[0] for item in ranked[:top_n]]
"""
=========================================================
SmartRAG Engine
=========================================================

Coordinates

Search
↓

Reranker
↓

Prompt Builder
↓

LLM
↓

Memory

=========================================================
"""

from search import SearchEngine
from reranker import Reranker
from prompt_builder import PromptBuilder
from llm import LLM
from memory import ConversationMemory

from config import (
    ENABLE_RERANK,
    RERANK_TOP_K,
    NO_CONTEXT_RESPONSE
)


class SmartRAG:

    def __init__(self):

        print("\nInitializing SmartRAG...")

        self.search = SearchEngine()

        self.reranker = Reranker()

        self.prompt_builder = PromptBuilder()

        self.llm = LLM()

        self.memory = ConversationMemory()

        print("SmartRAG Ready.\n")

    # =====================================================
    # Retrieve Documents
    # =====================================================

    def retrieve(
        self,
        question
    ):

        retrieval = self.search.retrieve(question)

        results = retrieval["results"]

        if ENABLE_RERANK and results:

            results = self.reranker.rerank(

                query=question,

                results=results,

                top_k=RERANK_TOP_K

            )

        context = self.search.build_context(results)

        sources = self.search.get_sources(results)

        return {

            "results": results,

            "context": context,

            "sources": sources

        }

    # =====================================================
    # Build Prompt
    # =====================================================

    def create_prompt(
        self,
        question,
        context
    ):

        history = self.memory.recent()

        if context.strip():

            return self.prompt_builder.build_prompt(

                question=question,

                context=context,

                history=history

            )

        return self.prompt_builder.build_no_context_prompt(

            question=question,

            history=history

        )
    # =====================================================
    # Ask SmartRAG
    # =====================================================

    def ask(
        self,
        question: str
    ):

        try:

            question = question.strip()

            if not question:

                return {

                    "question": "",

                    "answer": "Please enter a valid question.",

                    "sources": [],

                    "context": ""

                }

            # ---------------------------------------------
            # Retrieve Relevant Documents
            # ---------------------------------------------

            retrieval = self.retrieve(question)

            context = retrieval["context"]

            sources = retrieval["sources"]

            results = retrieval["results"]

            # ---------------------------------------------
            # No Context Found
            # ---------------------------------------------

            if not context.strip():

                answer = NO_CONTEXT_RESPONSE

                self.memory.add(

                    question,

                    answer

                )

                return {

                    "question": question,

                    "answer": answer,

                    "sources": [],

                    "context": "",

                    "results": []

                }

            # ---------------------------------------------
            # Build Prompt
            # ---------------------------------------------

            prompt = self.create_prompt(

                question,

                context

            )

            # ---------------------------------------------
            # Generate Answer
            # ---------------------------------------------

            answer = self.llm.generate(

                prompt

            )

            # ---------------------------------------------
            # Save Conversation
            # ---------------------------------------------

            self.memory.add(

                question,

                answer

            )

            # ---------------------------------------------
            # Return Response
            # ---------------------------------------------

            return {

                "question": question,

                "answer": answer,

                "sources": sources,

                "context": context,

                "results": results

            }

        except Exception as e:

            return {

                "question": question,

                "answer": f"SmartRAG Error : {str(e)}",

                "sources": [],

                "context": "",

                "results": []

            }

    # =====================================================
    # Chat Alias
    # =====================================================

    def chat(
        self,
        question
    ):

        return self.ask(question)
    # =====================================================
    # Clear Conversation Memory
    # =====================================================

    def clear_memory(self):

        self.memory.clear()

        print("Conversation memory cleared.")

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self):

        return {

            "documents": self.search.database.count(),

            "conversations": self.memory.count(),

            "reranking": ENABLE_RERANK,

            "llm_model": self.llm.model,

            "embedding_model": self.search.embedder.info()["model"]

        }

    # =====================================================
    # Print Statistics
    # =====================================================

    def print_statistics(self):

        stats = self.statistics()

        print("\n" + "=" * 60)
        print("SmartRAG Statistics")
        print("=" * 60)

        print(f"Indexed Chunks     : {stats['documents']}")
        print(f"Conversations      : {stats['conversations']}")
        print(f"Reranking Enabled  : {stats['reranking']}")
        print(f"Embedding Model    : {stats['embedding_model']}")
        print(f"LLM Model          : {stats['llm_model']}")

        print("=" * 60)

    # =====================================================
    # Health Check
    # =====================================================

    def health(self):

        return {

            "status": "healthy",

            "database": self.search.database.test_connection(),

            "vectors": self.search.database.count(),

            "llm": self.llm.test_connection(),

            "memory": self.memory.count(),

            "reranker": self.reranker.health()["status"]

        }

    # =====================================================
    # Print Health
    # =====================================================

    def print_health(self):

        health = self.health()

        print("\n" + "=" * 60)
        print("SmartRAG Health")
        print("=" * 60)

        for key, value in health.items():

            print(f"{key.capitalize():15}: {value}")

        print("=" * 60)

    # =====================================================
    # Show Sources
    # =====================================================

    def print_sources(
        self,
        sources
    ):

        print("\nSources")

        if not sources:

            print("No source documents.")

            return

        for source in sources:

            print(f" - {source}")
# =====================================================
# Testing
# =====================================================

if __name__ == "__main__":

    rag = SmartRAG()

    rag.print_statistics()

    rag.print_health()

    while True:

        print()

        question = input("You > ").strip()

        if question.lower() in [

            "exit",

            "quit"

        ]:

            break

        response = rag.ask(question)

        print("\nAssistant\n")

        print(response["answer"])

        rag.print_sources(

            response["sources"]

        )

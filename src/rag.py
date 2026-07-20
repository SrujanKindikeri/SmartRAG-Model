"""
=========================================================
SmartRAG
---------------------------------------------------------
Complete Retrieval-Augmented Generation Pipeline

Flow

User Question
      │
      ▼
Semantic Search
      │
      ▼
Cross Encoder Reranker
      │
      ▼
Conversation Memory
      │
      ▼
Prompt Builder
      │
      ▼
Qwen3 (Ollama)
      │
      ▼
Final Answer
=========================================================
"""

from search import SemanticSearch
from reranker import Reranker
from prompt_builder import PromptBuilder
from llm import LLM
from memory import ConversationMemory

from config import (
    TOP_K,
    RERANK_TOP_K
)


class SmartRAG:

    def __init__(self):

        print("=" * 70)
        print("Initializing SmartRAG...")
        print("=" * 70)

        self.search = SemanticSearch()

        self.reranker = Reranker()

        self.memory = ConversationMemory()

        self.prompt_builder = PromptBuilder()

        self.llm = LLM()

        print("✓ Semantic Search Loaded")

        print("✓ Cross Encoder Loaded")

        print("✓ Conversation Memory Loaded")

        print("✓ Prompt Builder Loaded")

        print("✓ Ollama Loaded")

        print("=" * 70)
        print("SmartRAG Ready")
        print("=" * 70)

    # ====================================================
    # Ask Question
    # ====================================================

    def ask(self, question):

        question = question.strip()

        if question == "":
            return (
                "Please enter a valid question.",
                []
            )

        try:

            # ---------------------------------------------
            # Retrieve Documents
            # ---------------------------------------------

            retrieved_chunks = self.search.search(
                question,
                top_k=TOP_K
            )

            if len(retrieved_chunks) == 0:

                return (
                    "I couldn't find any relevant information in the knowledge base.",
                    []
                )

            # ---------------------------------------------
            # Rerank Results
            # ---------------------------------------------

            ranked_chunks = self.reranker.rerank(

                question,

                retrieved_chunks,

                top_n=RERANK_TOP_K

            )

            # ---------------------------------------------
            # Build Prompt
            # ---------------------------------------------

            prompt, sources = self.prompt_builder.build_prompt(

                question,

                ranked_chunks,

                self.memory

            )

            # ---------------------------------------------
            # Generate Answer
            # ---------------------------------------------

            answer = self.llm.generate(prompt)

            # ---------------------------------------------
            # Save Conversation
            # ---------------------------------------------

            self.memory.add(

                question,

                answer

            )

            return answer, sources

        except Exception as e:

            return (
                f"SmartRAG Error : {str(e)}",
                []
            )

    # ====================================================
    # Clear Conversation Memory
    # ====================================================

    def clear_memory(self):

        self.memory.clear()

        print("Conversation history cleared.")

    # ====================================================
    # Show Memory
    # ====================================================

    def show_memory(self):

        history = self.memory.load()

        if len(history) == 0:

            print("No conversation history.")

            return

        print("=" * 70)

        print("Conversation History")

        print("=" * 70)

        for index, chat in enumerate(history, start=1):

            print(f"\nConversation {index}")

            print("-" * 50)

            print(f"User      : {chat['user']}")

            print(f"Assistant : {chat['assistant']}")

        print("=" * 70)
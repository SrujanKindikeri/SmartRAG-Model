"""
=========================================================
SmartRAG Conversation Memory
=========================================================

Stores conversation history in history.json

Features
--------
- Persistent memory
- Auto save
- Auto load
- Maximum history limit
- Conversation retrieval

=========================================================
"""

import json
from pathlib import Path

from config import (
    MEMORY_FILE,
    MAX_HISTORY
)


class ConversationMemory:

    def __init__(self):

        self.file = Path(MEMORY_FILE)

        self.history = []

        self.load()

    # =====================================================
    # Load Memory
    # =====================================================

    def load(self):

        if not self.file.exists():

            self.history = []

            return

        try:

            with open(

                self.file,

                "r",

                encoding="utf-8"

            ) as f:

                self.history = json.load(f)

        except Exception:

            self.history = []

    # =====================================================
    # Save Memory
    # =====================================================

    def save(self):

        with open(

            self.file,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                self.history,

                f,

                indent=4,

                ensure_ascii=False

            )

    # =====================================================
    # Add Conversation
    # =====================================================

    def add(

        self,

        question,

        answer

    ):

        self.history.append(

            {

                "question": question,

                "answer": answer

            }

        )

        if len(self.history) > MAX_HISTORY:

            self.history = self.history[-MAX_HISTORY:]

        self.save()

    # =====================================================
    # Get History
    # =====================================================

    def get_history(self):

        return self.history

    # =====================================================
    # Recent Conversations
    # =====================================================

    def recent(

        self,

        limit=5

    ):

        return self.history[-limit:]
    # =====================================================
    # Clear Memory
    # =====================================================

    def clear(self):

        self.history = []

        self.save()

    # =====================================================
    # Search History
    # =====================================================

    def search(
        self,
        keyword
    ):

        keyword = keyword.lower()

        results = []

        for item in self.history:

            question = item.get("question", "").lower()

            answer = item.get("answer", "").lower()

            if keyword in question or keyword in answer:

                results.append(item)

        return results

    # =====================================================
    # Remove Conversation
    # =====================================================

    def remove(
        self,
        index
    ):

        if 0 <= index < len(self.history):

            self.history.pop(index)

            self.save()

            return True

        return False

    # =====================================================
    # Count Conversations
    # =====================================================

    def count(self):

        return len(self.history)

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self):

        return {

            "total_conversations": self.count(),

            "memory_file": str(self.file),

            "max_history": MAX_HISTORY

        }

    # =====================================================
    # Print Statistics
    # =====================================================

    def print_statistics(self):

        stats = self.statistics()

        print("\n" + "=" * 60)
        print("Conversation Memory Statistics")
        print("=" * 60)

        print(
            f"Total Conversations : {stats['total_conversations']}"
        )

        print(
            f"Memory File         : {stats['memory_file']}"
        )

        print(
            f"Maximum History     : {stats['max_history']}"
        )

        print("=" * 60)

    # =====================================================
    # Health Check
    # =====================================================

    def health(self):

        return {

            "status": "healthy",

            "loaded": isinstance(self.history, list),

            "memory_file_exists": self.file.exists(),

            "conversation_count": self.count()

        }

    # =====================================================
    # Print Health
    # =====================================================

    def print_health(self):

        health = self.health()

        print("\n" + "=" * 60)
        print("Conversation Memory Health")
        print("=" * 60)

        for key, value in health.items():

            print(f"{key.capitalize():22}: {value}")

        print("=" * 60)

    # =====================================================
    # Print Conversations
    # =====================================================

    def print_history(self):

        print("\n" + "=" * 60)
        print("Conversation History")
        print("=" * 60)

        if not self.history:

            print("No conversations available.")
            print("=" * 60)
            return

        for i, item in enumerate(self.history, start=1):

            print(f"\nConversation #{i}")
            print("-" * 60)

            print("Question:")
            print(item.get("question", ""))

            print("\nAnswer:")
            print(item.get("answer", ""))

        print("=" * 60)
# =====================================================
# Testing
# =====================================================

if __name__ == "__main__":

    memory = ConversationMemory()

    memory.add(

        "What is SmartRAG?",

        "SmartRAG is a Retrieval-Augmented Generation system."

    )

    memory.add(

        "Minimum attendance?",

        "Students must maintain at least 75% attendance."

    )

    memory.print_statistics()

    memory.print_health()

    memory.print_history()

    print()

    print("Search Results\n")

    results = memory.search("attendance")

    for item in results:

        print(item)

    print()

    print("Recent Conversations\n")

    for item in memory.recent():

        print(item)

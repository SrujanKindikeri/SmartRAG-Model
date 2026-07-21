print("MAIN STARTED")
"""
=========================================================
SmartRAG Terminal Application
=========================================================

Commands

/help
/stats
/health
/history
/clear
/rebuild
/exit

=========================================================
"""

from rag import SmartRAG
from indexer import Indexer


class SmartRAGCLI:

    def __init__(self):

        print("=" * 70)
        print("SmartRAG v2.0")
        print("=" * 70)

        # -------------------------------------
        # Initialize Indexer
        # -------------------------------------

        self.indexer = Indexer()

        self.indexer.startup()

        # -------------------------------------
        # Initialize RAG
        # -------------------------------------

        self.rag = SmartRAG()

        self.last_response = None

    # =====================================================
    # Banner
    # =====================================================

    def banner(self):

        print()

        print("=" * 70)
        print("SmartRAG Ready")
        print("=" * 70)

        print("Type /help to see available commands.\n")

    # =====================================================
    # Help
    # =====================================================

    def help(self):

        print()

        print("=" * 70)
        print("Commands")
        print("=" * 70)

        print("/help      Show commands")
        print("/stats     System statistics")
        print("/health    Health status")
        print("/history   Conversation history")
        print("/sources   Sources from last answer")
        print("/clear     Clear conversation memory")
        print("/rebuild   Rebuild knowledge base")
        print("/exit      Exit SmartRAG")

        print("=" * 70)

    # =====================================================
    # Statistics
    # =====================================================

    def stats(self):

        self.rag.print_statistics()

    # =====================================================
    # Health
    # =====================================================

    def health(self):

        self.rag.print_health()

    # =====================================================
    # History
    # =====================================================

    def history(self):

        self.rag.memory.print_history()

    # =====================================================
    # Clear Memory
    # =====================================================

    def clear(self):

        self.rag.clear_memory()

    # =====================================================
    # Rebuild Database
    # =====================================================

    def rebuild(self):

        print()

        print("Rebuilding Knowledge Base...\n")

        self.indexer.rebuild()

        print("\nKnowledge Base Updated.\n")
    # =====================================================
    # Show Last Sources
    # =====================================================

    def sources(self):

        if not self.last_response:

            print("\nNo previous response available.\n")
            return

        self.rag.print_sources(

            self.last_response.get(

                "sources",

                []

            )

        )

    # =====================================================
    # Process Commands
    # =====================================================

    def process_command(

        self,

        command

    ):

        command = command.lower()

        if command == "/help":

            self.help()

        elif command == "/stats":

            self.stats()

        elif command == "/health":

            self.health()

        elif command == "/history":

            self.history()

        elif command == "/sources":

            self.sources()

        elif command == "/clear":

            self.clear()

        elif command == "/rebuild":

            self.rebuild()

        elif command in [

            "/exit",

            "/quit"

        ]:

            print("\nGoodbye!\n")

            return False

        else:

            print("\nUnknown command.")

            print("Type /help\n")

        return True

    # =====================================================
    # Chat Loop
    # =====================================================

    def run(self):

        self.banner()

        while True:

            try:

                question = input("You > ").strip()

                if not question:

                    continue

                if question.startswith("/"):

                    if not self.process_command(

                        question

                    ):

                        break

                    continue

                print()

                print("Assistant\n")

                response = self.rag.ask(

                    question

                )

                self.last_response = response

                print(

                    response["answer"]

                )

                if response["sources"]:

                    print("\nSources")

                    for source in response["sources"]:

                        print(

                            f" - {source}"

                        )

                print()

            except KeyboardInterrupt:

                print("\n\nInterrupted.")

                break

            except Exception as e:

                print()

                print(

                    f"Unexpected Error : {e}"

                )
# =====================================================
# Main
# =====================================================

if __name__ == "__main__":

    app = SmartRAGCLI()

    app.run()
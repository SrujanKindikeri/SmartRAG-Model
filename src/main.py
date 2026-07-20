from loader import DocumentLoader
from chunking import TextChunker
from embeddings import EmbeddingGenerator
from database import VectorDatabase
from rag import SmartRAG


def initialize_database():

    db = VectorDatabase()

    # If database already contains vectors
    if db.count() > 0:
        print("=" * 60)
        print("Knowledge Base Already Exists")
        print(f"Stored Chunks : {db.count()}")
        print("=" * 60)
        return

    print("=" * 60)
    print("Building Knowledge Base...")
    print("=" * 60)

    # Load documents
    loader = DocumentLoader()
    documents = loader.load_documents()

    # Chunk documents
    chunker = TextChunker()
    chunks = chunker.chunk_documents(documents)

    print(f"Total Chunks : {len(chunks)}")

    # Generate embeddings
    embedder = EmbeddingGenerator()
    embeddings = embedder.embed_chunks(chunks)

    # Store in ChromaDB
    db.add_chunks(chunks, embeddings)

    print("=" * 60)
    print("Knowledge Base Created Successfully")
    print("=" * 60)


def start_chat():

    rag = SmartRAG()

    print("\n")
    print("=" * 70)
    print("🤖 SmartRAG Terminal")
    print("=" * 70)
    print("Type 'exit' to quit.")
    print("=" * 70)

    while True:

        question = input("\nYou : ").strip()

        if question.lower() in ["exit", "quit"]:
            print("\nGoodbye 👋")
            break

        if question == "":
            continue

        answer, sources = rag.ask(question)

        print("\nAssistant\n")
        print(answer)

        if len(sources):

            print("\nSources")

            for source in sources:
                print(f"• {source}")

        print("\n" + "-" * 70)


if __name__ == "__main__":

    initialize_database()

    start_chat()
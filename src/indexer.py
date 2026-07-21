"""
=========================================================
SmartRAG Indexer
=========================================================

Pipeline
--------
Load Documents
      │
      ▼
Chunk Documents
      │
      ▼
Generate Embeddings
      │
      ▼
Store in ChromaDB

Features
--------
✓ Incremental Indexing
✓ SHA256 Change Detection
✓ Metadata Persistence
✓ Duplicate Prevention
✓ Automatic Updates
=========================================================
"""

import json
from pathlib import Path

from loader import DocumentLoader
from chunking import DocumentChunker
from embeddings import EmbeddingGenerator
from database import VectorDatabase

from config import (
    INDEX_FILE,
    ENABLE_INCREMENTAL_INDEXING
)


class Indexer:

    def __init__(self):

        self.loader = DocumentLoader()

        self.chunker = DocumentChunker()

        self.embedder = EmbeddingGenerator()

        self.database = VectorDatabase()

        self.metadata = self.load_metadata()

    # =====================================================
    # Load Metadata
    # =====================================================

    def load_metadata(self):

        if not INDEX_FILE.exists():

            return {}

        try:

            with open(

                INDEX_FILE,

                "r",

                encoding="utf-8"

            ) as file:

                return json.load(file)

        except Exception:

            return {}

    # =====================================================
    # Save Metadata
    # =====================================================

    def save_metadata(self):

        with open(

            INDEX_FILE,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                self.metadata,

                file,

                indent=4

            )

    # =====================================================
    # Check Document Status
    # =====================================================

    def needs_update(

        self,

        document

    ):

        if not ENABLE_INCREMENTAL_INDEXING:

            return True

        filename = document["filename"]

        current_hash = document["hash"]

        if filename not in self.metadata:

            return True

        old_hash = self.metadata[filename]["hash"]

        return old_hash != current_hash
    # =====================================================
    # Index Single Document
    # =====================================================

    def index_document(
        self,
        document
    ):

        filename = document["filename"]

        print(f"\nIndexing : {filename}")

        # ---------------------------------------------
        # Update Existing Document
        # ---------------------------------------------

        if filename in self.metadata:

            old_hash = self.metadata[filename]["hash"]

            if self.database.file_exists(old_hash):

                self.database.delete_file(old_hash)

        # ---------------------------------------------
        # Chunk Document
        # ---------------------------------------------

        chunks = self.chunker.chunk_document(document)

        if not chunks:

            print("No chunks generated.")

            return

        # ---------------------------------------------
        # Generate Embeddings
        # ---------------------------------------------

        embeddings = self.embedder.embed_chunks(

            chunks

        )

        # ---------------------------------------------
        # Store in Database
        # ---------------------------------------------

        self.database.add_chunks(

            chunks,

            embeddings

        )

        # ---------------------------------------------
        # Save Metadata
        # ---------------------------------------------

        self.metadata[filename] = {

            "hash": document["hash"],

            "filepath": document["filepath"],

            "extension": document["extension"],

            "size": document["size"]

        }

        self.save_metadata()

        print(f"Completed : {filename}")

    # =====================================================
    # Index All Documents
    # =====================================================

    def index_documents(self):

        documents = self.loader.load_documents()

        if not documents:

            print("No documents found.")

            return

        indexed = 0
        skipped = 0

        for document in documents:

            if self.needs_update(document):

                self.index_document(

                    document

                )

                indexed += 1

            else:

                print(

                    f"Skipped : {document['filename']}"

                )

                skipped += 1

        print("\n" + "=" * 60)
        print("Indexing Completed")
        print("=" * 60)
        print(f"Indexed : {indexed}")
        print(f"Skipped : {skipped}")
        print(f"Vectors : {self.database.count()}")
        print("=" * 60)
    # =====================================================
    # Rebuild Entire Knowledge Base
    # =====================================================

    def rebuild(self):

        print("\n" + "=" * 60)
        print("Rebuilding Knowledge Base...")
        print("=" * 60)

        # Clear existing vectors
        self.database.clear_database()

        # Reset metadata
        self.metadata = {}

        self.save_metadata()

        # Re-index all documents
        self.index_documents()

        print("\nKnowledge Base Rebuilt Successfully.")

    # =====================================================
    # Synchronize Database
    # =====================================================

    def sync(self):

        """
        Remove vectors belonging to files
        that no longer exist inside data/.
        """

        documents = self.loader.load_documents()

        current_files = {

            document["filename"]

            for document in documents

        }

        removed = []

        for filename in list(self.metadata.keys()):

            if filename not in current_files:

                old_hash = self.metadata[filename]["hash"]

                print(f"Removing : {filename}")

                self.database.delete_file(old_hash)

                removed.append(filename)

                del self.metadata[filename]

        if removed:

            self.save_metadata()

        print("\nSynchronization Complete.")

        print(f"Removed Files : {len(removed)}")

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self):

        return {

            "indexed_documents": len(self.metadata),

            "stored_vectors": self.database.count(),

            "metadata_file": str(INDEX_FILE)

        }

    # =====================================================
    # Print Statistics
    # =====================================================

    def print_statistics(self):

        stats = self.statistics()

        print("\n" + "=" * 60)
        print("Indexer Statistics")
        print("=" * 60)

        print(

            f"Indexed Documents : "

            f"{stats['indexed_documents']}"

        )

        print(

            f"Stored Vectors    : "

            f"{stats['stored_vectors']}"

        )

        print(

            f"Metadata File     : "

            f"{stats['metadata_file']}"

        )

        print("=" * 60)
    # =====================================================
    # Metadata Information
    # =====================================================

    def metadata_info(self):

        print("\n" + "=" * 60)
        print("Indexed Files")
        print("=" * 60)

        if not self.metadata:

            print("No indexed files found.")
            print("=" * 60)
            return

        for filename, info in self.metadata.items():

            print(f"\nFile      : {filename}")
            print(f"Hash      : {info.get('hash', '')[:20]}...")
            print(f"Extension : {info.get('extension', '')}")
            print(f"Size      : {info.get('size', 0)} bytes")
            print(f"Path      : {info.get('filepath', '')}")

        print("=" * 60)

    # =====================================================
    # Health Check
    # =====================================================

    def health(self):

        try:

            return {

                "status": "healthy",

                "documents": len(self.metadata),

                "vectors": self.database.count(),

                "database": self.database.test_connection()

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
        print("Indexer Health")
        print("=" * 60)

        for key, value in health.items():

            print(f"{key.capitalize():15}: {value}")

        print("=" * 60)

    # =====================================================
    # Startup
    # =====================================================

    def startup(self):

        """
        Smart startup.

        Existing KB
            ↓
        Sync Deleted Files
            ↓
        Index New / Updated Files

        New KB
            ↓
        Build Everything
        """

        if self.database.count() == 0:

            print("=" * 60)
            print("No Knowledge Base Found")
            print("=" * 60)

            self.index_documents()

            return

        print("=" * 60)
        print("Knowledge Base Already Exists")
        print(f"Stored Chunks : {self.database.count()}")
        print("=" * 60)

        self.sync()

        self.index_documents()

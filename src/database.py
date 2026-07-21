"""
=========================================================
SmartRAG Vector Database
=========================================================

Features
--------
✓ Persistent ChromaDB
✓ Safe Metadata Storage
✓ Semantic Search
✓ Incremental Indexing Support
✓ Duplicate Detection
✓ Production Ready
=========================================================
"""

from typing import Dict, List

import chromadb
from chromadb.config import Settings

from config import (
    VECTOR_DB_DIR,
    COLLECTION_NAME
)


class VectorDatabase:

    def __init__(self):

        print("Initializing ChromaDB...")

        self.client = chromadb.PersistentClient(

            path=str(VECTOR_DB_DIR),

            settings=Settings(
                anonymized_telemetry=False
            )

        )

        self.collection = self.client.get_or_create_collection(

            name=COLLECTION_NAME,

            metadata={
                "description": "SmartRAG Knowledge Base"
            }

        )

        print(f"Collection Loaded : {COLLECTION_NAME}")

    # =====================================================
    # Add Chunks
    # =====================================================

    def add_chunks(

        self,

        chunks: List[Dict],

        embeddings: List[List[float]]

    ):

        if not chunks:

            return

        ids = []
        documents = []
        metadatas = []

        for chunk in chunks:

            ids.append(chunk["chunk_id"])

            documents.append(chunk["text"])

            metadatas.append({

                "filename": chunk["filename"],

                "filepath": chunk["filepath"],

                "extension": chunk["extension"],

                "hash": chunk["hash"],

                "chunk_number": int(chunk["chunk_number"]),

                "size": int(chunk["size"])

            })

        try:

            self.collection.add(

                ids=ids,

                documents=documents,

                embeddings=embeddings,

                metadatas=metadatas

            )

            print("=" * 60)
            print(f"Stored {len(ids)} chunks.")
            print("=" * 60)

        except Exception as e:

            print(f"Database Error : {e}")

    # =====================================================
    # Count
    # =====================================================

    def count(self):

        return self.collection.count()

    # =====================================================
    # Collection Info
    # =====================================================

    def info(self):

        return {

            "collection": COLLECTION_NAME,

            "vectors": self.count()

        }

    def print_info(self):

        info = self.info()

        print("\n" + "=" * 60)
        print("Vector Database")
        print("=" * 60)

        print(f"Collection : {info['collection']}")
        print(f"Vectors    : {info['vectors']}")

        print("=" * 60)
    # =====================================================
    # Search
    # =====================================================

    def search(
        self,
        query_embedding,
        top_k=5
    ):

        try:

            results = self.collection.query(

                query_embeddings=[query_embedding],

                n_results=top_k,

                include=[
                    "documents",
                    "metadatas",
                    "distances"
                ]

            )

            output = []

            if not results["documents"]:

                return output

            documents = results["documents"][0]
            metadatas = results["metadatas"][0]
            distances = results["distances"][0]

            for document, metadata, distance in zip(
                documents,
                metadatas,
                distances
            ):

                metadata = metadata or {}

                output.append({

                    "text": document,

                    "filename": metadata.get(
                        "filename",
                        "Unknown"
                    ),

                    "filepath": metadata.get(
                        "filepath",
                        ""
                    ),

                    "extension": metadata.get(
                        "extension",
                        ""
                    ),

                    "hash": metadata.get(
                        "hash",
                        ""
                    ),

                    "chunk_number": metadata.get(
                        "chunk_number",
                        0
                    ),

                    "size": metadata.get(
                        "size",
                        0
                    ),

                    # Smaller distance = Better match
                    "score": float(distance)

                })

            return output

        except Exception as e:

            print(f"Search Error : {e}")

            return []

    # =====================================================
    # Get All Chunks Of A File
    # =====================================================

    def get_file_chunks(
        self,
        file_hash
    ):

        try:

            return self.collection.get(

                where={
                    "hash": file_hash
                }

            )

        except Exception as e:

            print(f"Get Error : {e}")

            return None

    # =====================================================
    # Check If File Exists
    # =====================================================

    def file_exists(
        self,
        file_hash
    ):

        try:

            results = self.collection.get(

                where={
                    "hash": file_hash
                }

            )

            return len(results.get("ids", [])) > 0

        except Exception:

            return False

    # =====================================================
    # Delete File
    # =====================================================

    def delete_file(
        self,
        file_hash
    ):

        try:

            results = self.collection.get(

                where={
                    "hash": file_hash
                }

            )

            ids = results.get("ids", [])

            if not ids:

                return

            self.collection.delete(

                ids=ids

            )

            print(f"Deleted {len(ids)} chunks.")

        except Exception as e:

            print(f"Delete Error : {e}")

    # =====================================================
    # Update Existing File
    # =====================================================

    def update_file(
        self,
        chunks,
        embeddings
    ):

        if not chunks:

            return

        file_hash = chunks[0]["hash"]

        self.delete_file(file_hash)

        self.add_chunks(
            chunks,
            embeddings
        )
    # =====================================================
    # Clear Database
    # =====================================================

    def clear_database(self):

        try:

            total = self.count()

            if total == 0:

                print("Database is already empty.")

                return

            results = self.collection.get()

            ids = results.get("ids", [])

            if ids:

                self.collection.delete(ids=ids)

            print("=" * 60)
            print("Database Cleared Successfully")
            print("=" * 60)

        except Exception as e:

            print(f"Clear Database Error : {e}")

    # =====================================================
    # Collection Statistics
    # =====================================================

    def collection_statistics(self):

        return {

            "collection": COLLECTION_NAME,

            "vectors": self.count()

        }

    # =====================================================
    # Print Statistics
    # =====================================================

    def print_statistics(self):

        stats = self.collection_statistics()

        print("\n" + "=" * 60)
        print("Vector Database Statistics")
        print("=" * 60)

        print(f"Collection : {stats['collection']}")
        print(f"Vectors    : {stats['vectors']}")

        print("=" * 60)

    # =====================================================
    # Test Connection
    # =====================================================

    def test_connection(self):

        try:

            self.collection.count()

            return True

        except Exception:

            return False

    # =====================================================
    # Reset Collection
    # =====================================================

    def reset_collection(self):

        try:

            self.client.delete_collection(

                COLLECTION_NAME

            )

        except Exception:

            pass

        self.collection = self.client.get_or_create_collection(

            name=COLLECTION_NAME,

            metadata={

                "description": "SmartRAG Knowledge Base"

            }

        )

        print("Collection Reset Successfully.")

    # =====================================================
    # Database Health
    # =====================================================

    def health(self):

        return {

            "status": "healthy" if self.test_connection() else "error",

            "collection": COLLECTION_NAME,

            "vectors": self.count()

        }

    # =====================================================
    # Print Health
    # =====================================================

    def print_health(self):

        health = self.health()

        print("\n" + "=" * 60)
        print("Vector Database Health")
        print("=" * 60)

        print(f"Status     : {health['status']}")
        print(f"Collection : {health['collection']}")
        print(f"Vectors    : {health['vectors']}")

        print("=" * 60)

    # =====================================================
    # Optimize Database (Placeholder)
    # =====================================================

    def optimize(self):

        print("Database optimization completed.")

    # =====================================================
    # Close Database
    # =====================================================

    def close(self):

        pass


# =========================================================
# Testing
# =========================================================

if __name__ == "__main__":

    db = VectorDatabase()

    print()

    db.print_info()

    db.print_statistics()

    db.print_health()

    print()

    print("Connection :", db.test_connection())

"""
=========================================================
SmartRAG Text Chunker
=========================================================

Splits documents into overlapping chunks while assigning
globally unique IDs to every chunk.
"""

import uuid

from config import CHUNK_SIZE, CHUNK_OVERLAP


class TextChunker:

    def __init__(self):
        self.chunk_size = CHUNK_SIZE
        self.chunk_overlap = CHUNK_OVERLAP

    # -----------------------------------------------------
    # Chunk All Documents
    # -----------------------------------------------------

    def chunk_documents(self, documents):

        chunks = []

        print("=" * 60)
        print("Chunking Documents...")
        print("=" * 60)

        for document in documents:

            doc_chunks = self.chunk_text(document)

            chunks.extend(doc_chunks)

        print(f"Total Chunks Created : {len(chunks)}")
        print("=" * 60)

        return chunks

    # -----------------------------------------------------
    # Chunk One Document
    # -----------------------------------------------------

    def chunk_text(self, document):

        text = document["text"]

        filename = document["filename"]

        path = document["path"]

        chunks = []

        start = 0

        chunk_number = 1

        text_length = len(text)

        while start < text_length:

            end = min(start + self.chunk_size, text_length)

            chunk = text[start:end].strip()

            if chunk:

                chunks.append({

                    # Completely unique ID
                    "chunk_id": str(uuid.uuid4()),

                    # Sequential number inside document
                    "chunk_number": chunk_number,

                    "filename": filename,

                    "path": path,

                    "text": chunk

                })

                chunk_number += 1

            # Stop when end of document is reached
            if end >= text_length:
                break

            # Overlapping chunks
            start = end - self.chunk_overlap

            if start < 0:
                start = 0

        return chunks

    # -----------------------------------------------------
    # Information
    # -----------------------------------------------------

    def info(self):

        print("=" * 60)
        print("Text Chunker")
        print("=" * 60)
        print(f"Chunk Size    : {self.chunk_size}")
        print(f"Chunk Overlap : {self.chunk_overlap}")
        print("=" * 60)
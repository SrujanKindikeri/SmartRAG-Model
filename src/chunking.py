"""
=========================================================
SmartRAG Document Chunker
=========================================================

Features
--------
✓ Fixed-size Chunking
✓ Overlapping Chunks
✓ UUID Chunk IDs
✓ Metadata Preservation
✓ Production Ready
=========================================================
"""

import uuid
from typing import Dict, List

from config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP
)


class DocumentChunker:

    def __init__(self):

        self.chunk_size = CHUNK_SIZE
        self.chunk_overlap = CHUNK_OVERLAP

    # =====================================================
    # Normalize Text
    # =====================================================

    def clean_text(self, text: str) -> str:

        text = text.replace("\r", "\n")

        lines = []

        for line in text.split("\n"):

            line = line.strip()

            if line:

                lines.append(line)

        return "\n".join(lines)

    # =====================================================
    # Split Text
    # =====================================================

    def split_text(self, text: str) -> List[str]:

        text = self.clean_text(text)

        if not text:

            return []

        chunks = []

        start = 0

        length = len(text)

        while start < length:

            end = start + self.chunk_size

            chunk = text[start:end].strip()

            if chunk:

                chunks.append(chunk)

            start += self.chunk_size - self.chunk_overlap

        return chunks

    # =====================================================
    # Chunk One Document
    # =====================================================

    def chunk_document(self, document: Dict) -> List[Dict]:

        pieces = self.split_text(document["text"])

        output = []

        for index, piece in enumerate(pieces, start=1):

            output.append({

                "chunk_id": str(uuid.uuid4()),

                "chunk_number": index,

                "filename": document["filename"],

                "filepath": document["filepath"],

                "extension": document["extension"],

                "hash": document["hash"],

                "size": document["size"],

                "text": piece

            })

        return output

    # =====================================================
    # Chunk Multiple Documents
    # =====================================================

    def chunk_documents(self, documents: List[Dict]) -> List[Dict]:

        all_chunks = []

        for document in documents:

            chunks = self.chunk_document(document)

            all_chunks.extend(chunks)

        return all_chunks

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self, chunks: List[Dict]):

        if not chunks:

            return {

                "chunks": 0,

                "average_length": 0

            }

        total = sum(

            len(chunk["text"])

            for chunk in chunks

        )

        return {

            "chunks": len(chunks),

            "average_length": total / len(chunks)

        }

    # =====================================================
    # Preview
    # =====================================================

    def preview(self, chunks: List[Dict], count: int = 3):

        print("=" * 60)
        print("Chunk Preview")
        print("=" * 60)

        for chunk in chunks[:count]:

            print(f"\nChunk #{chunk['chunk_number']}")
            print(f"File : {chunk['filename']}")
            print("-" * 60)

            preview = chunk["text"][:250]

            if len(chunk["text"]) > 250:

                preview += "..."

            print(preview)

        print("=" * 60)


# =========================================================
# Testing
# =========================================================

if __name__ == "__main__":

    from loader import DocumentLoader

    loader = DocumentLoader()

    documents = loader.load_documents()

    chunker = DocumentChunker()

    chunks = chunker.chunk_documents(documents)

    print()

    print(chunker.statistics(chunks))

    chunker.preview(chunks)
"""
=========================================================
SmartRAG Document Loader
=========================================================

Supported Formats
-----------------
✓ PDF
✓ DOCX
✓ TXT

Features
--------
✓ SHA256 Hashing
✓ Metadata Extraction
✓ Automatic File Discovery
✓ Error Handling
✓ Duplicate Detection Support
=========================================================
"""

import hashlib
from pathlib import Path
from typing import Dict, List

import fitz                  # PyMuPDF
from docx import Document

from config import (
    DATA_DIR,
    SUPPORTED_EXTENSIONS
)


class DocumentLoader:

    def __init__(self):

        self.data_dir = DATA_DIR

    # =====================================================
    # SHA256
    # =====================================================

    def calculate_hash(self, filepath: Path) -> str:

        sha = hashlib.sha256()

        with open(filepath, "rb") as file:

            while True:

                chunk = file.read(8192)

                if not chunk:
                    break

                sha.update(chunk)

        return sha.hexdigest()

    # =====================================================
    # PDF
    # =====================================================

    def read_pdf(self, filepath: Path) -> str:

        document = fitz.open(filepath)

        pages = []

        for page in document:

            pages.append(page.get_text())

        document.close()

        return "\n".join(pages)

    # =====================================================
    # DOCX
    # =====================================================

    def read_docx(self, filepath: Path) -> str:

        document = Document(filepath)

        paragraphs = []

        for para in document.paragraphs:

            text = para.text.strip()

            if text:

                paragraphs.append(text)

        return "\n".join(paragraphs)

    # =====================================================
    # TXT
    # =====================================================

    def read_txt(self, filepath: Path) -> str:

        with open(
            filepath,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            return file.read()

    # =====================================================
    # Read Any File
    # =====================================================

    def read_file(self, filepath: Path) -> str:

        suffix = filepath.suffix.lower()

        if suffix == ".pdf":

            return self.read_pdf(filepath)

        elif suffix == ".docx":

            return self.read_docx(filepath)

        elif suffix == ".txt":

            return self.read_txt(filepath)

        else:

            raise ValueError(f"Unsupported file: {filepath}")

    # =====================================================
    # Load Single File
    # =====================================================

    def load_file(self, filepath: Path) -> Dict:

        text = self.read_file(filepath)

        return {

            "filename": filepath.name,

            "filepath": str(filepath.resolve()),

            "extension": filepath.suffix.lower(),

            "hash": self.calculate_hash(filepath),

            "size": filepath.stat().st_size,

            "text": text.strip()

        }

    # =====================================================
    # Discover Files
    # =====================================================

    def discover_files(self) -> List[Path]:

        files = []

        for extension in SUPPORTED_EXTENSIONS:

            files.extend(

                self.data_dir.rglob(f"*{extension}")

            )

        return sorted(files)

    # =====================================================
    # Load All Documents
    # =====================================================

    def load_documents(self) -> List[Dict]:

        documents = []

        files = self.discover_files()

        print("=" * 60)
        print(f"Found {len(files)} documents")
        print("=" * 60)

        for filepath in files:

            try:

                document = self.load_file(filepath)

                documents.append(document)

                print(f"Loaded : {filepath.name}")

            except Exception as e:

                print(f"Failed : {filepath.name}")

                print(e)

        print("=" * 60)
        print(f"Successfully Loaded : {len(documents)}")
        print("=" * 60)

        return documents

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self):

        files = self.discover_files()

        return {

            "directory": str(self.data_dir),

            "documents": len(files),

            "extensions": sorted(
                list(SUPPORTED_EXTENSIONS)
            )

        }


# =========================================================
# Testing
# =========================================================

if __name__ == "__main__":

    loader = DocumentLoader()

    stats = loader.statistics()

    print(stats)

    documents = loader.load_documents()

    print()

    for doc in documents:

        print(doc["filename"])
        print(doc["hash"][:20])
        print(doc["size"])
        print("-" * 40)
        
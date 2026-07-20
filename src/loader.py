import fitz
from docx import Document
from pathlib import Path

from config import DATA_DIR, SUPPORTED_FILES


class DocumentLoader:
    """
    Loads PDF, DOCX and TXT documents from the data directory.
    """

    def __init__(self):
        self.data_dir = DATA_DIR

    # -------------------------------------------------------
    # Load Every Document
    # -------------------------------------------------------

    def load_documents(self):

        documents = []

        if not self.data_dir.exists():
            print(f"Data directory not found: {self.data_dir}")
            return documents

        print("=" * 60)
        print("Loading Documents...")
        print("=" * 60)

        for file in self.data_dir.rglob("*"):

            if not file.is_file():
                continue

            if file.suffix.lower() not in SUPPORTED_FILES:
                continue

            try:

                if file.suffix.lower() == ".pdf":
                    text = self._load_pdf(file)

                elif file.suffix.lower() == ".docx":
                    text = self._load_docx(file)

                elif file.suffix.lower() == ".txt":
                    text = self._load_txt(file)

                else:
                    continue

                if text.strip():

                    documents.append({
                        "filename": file.name,
                        "path": str(file),
                        "type": file.suffix.lower(),
                        "text": text
                    })

                    print(f"Loaded : {file.name}")

            except Exception as e:
                print(f"Failed : {file.name}")
                print(e)

        print("=" * 60)
        print(f"Documents Loaded : {len(documents)}")
        print("=" * 60)

        return documents

    # -------------------------------------------------------
    # PDF
    # -------------------------------------------------------

    def _load_pdf(self, path):

        pdf = fitz.open(path)

        text = ""

        for page in pdf:
            text += page.get_text()

        pdf.close()

        return text

    # -------------------------------------------------------
    # DOCX
    # -------------------------------------------------------

    def _load_docx(self, path):

        doc = Document(path)

        return "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
        )

    # -------------------------------------------------------
    # TXT
    # -------------------------------------------------------

    def _load_txt(self, path):

        with open(path, "r", encoding="utf-8", errors="ignore") as file:
            return file.read()

    # -------------------------------------------------------
    # Loader Information
    # -------------------------------------------------------

    def info(self):

        print("=" * 60)
        print("Document Loader")
        print("=" * 60)
        print(f"Data Folder : {self.data_dir}")
        print(f"Supported   : {SUPPORTED_FILES}")
        print("=" * 60)
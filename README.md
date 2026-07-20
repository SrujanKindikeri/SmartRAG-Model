# 🧠 SmartRAG-Model

> An Intelligent Self-Learning Retrieval-Augmented Generation (RAG) System that continuously improves its knowledge base by learning from unanswered questions and newly uploaded documents.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Under%20Development-orange)
![AI](https://img.shields.io/badge/AI-RAG-red)

---

## 📖 Overview

SmartRAG is a local Retrieval-Augmented Generation (RAG) system designed to answer user queries using information extracted from PDFs and DOCX files.

Unlike traditional RAG systems, SmartRAG continuously learns.

If the system cannot answer a question, it stores the query in an **Unanswered Questions Database**. Once new documents or answers are added, the system automatically learns and can answer similar questions in future conversations.

Everything runs locally from the terminal.

---

# ✨ Features

- 📄 PDF Knowledge Extraction
- 📄 DOCX Knowledge Extraction
- 🔍 Semantic Search using Embeddings
- 🧠 Self-Learning Knowledge Base
- 📚 Automatic Document Indexing
- ❓ Stores Unanswered Questions
- 🔄 Incremental Knowledge Updates
- ⚡ Fast Vector Search
- 🤖 Local LLM Support (Ollama)
- 💻 Terminal-based Chat Interface
- 📊 Query Logging
- 📁 Modular Architecture

---

# 🏗️ Project Structure

```text
SmartRAG-Model/
│
├── data/
│   ├── documents/
│   ├── processed/
│   ├── unanswered_questions.json
│   └── logs/
│
├── embeddings/
│
├── vector_store/
│
├── models/
│
├── src/
│   ├── ingestion/
│   ├── retrieval/
│   ├── embeddings/
│   ├── learning/
│   ├── llm/
│   ├── database/
│   └── utils/
│
├── tests/
│
├── requirements.txt
├── config.py
├── main.py
├── README.md
└── .gitignore
```

---

# 🚀 Workflow

```text
          Upload PDF / DOCX
                   │
                   ▼
         Extract Document Text
                   │
                   ▼
        Generate Text Embeddings
                   │
                   ▼
       Store in Vector Database
                   │
                   ▼
          User asks Question
                   │
                   ▼
         Semantic Similarity Search
                   │
        ┌──────────┴──────────┐
        │                     │
   Answer Found          No Answer
        │                     │
        ▼                     ▼
 Return Response      Save Question
                              │
                              ▼
                 Add New Knowledge Later
                              │
                              ▼
                     SmartRAG Learns
```

---

# 🛠 Tech Stack

### Programming

- Python

### Machine Learning

- Sentence Transformers
- HuggingFace
- Scikit-Learn

### Vector Database

- FAISS
- ChromaDB

### Document Processing

- PyMuPDF
- pdfplumber
- python-docx

### LLM

- Ollama
- Llama 3
- Mistral

### Utilities

- NumPy
- Pandas
- Rich
- tqdm

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/SrujanKindikeri/SmartRAG-Model.git
```

Move into the project

```bash
cd SmartRAG-Model
```

Create virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run

```bash
python main.py
```

---

# 💬 Example

```text
You : What is Machine Learning?

SmartRAG :
Machine Learning is a branch of Artificial Intelligence that enables computers to learn patterns from data without being explicitly programmed.
```

---

# 📚 Self-Learning Example

User asks

```text
Explain Apache Airflow DAG Scheduling.
```

Knowledge not available.

SmartRAG stores

```text
unanswered_questions.json
```

Later...

User uploads

```
BigData.pdf
```

System indexes document.

Now the same question receives an answer automatically.

No manual retraining required.

---

# 🎯 Future Features

- Web Interface
- Voice Assistant
- Multi-user Support
- Image Retrieval
- OCR Support
- Hybrid Search
- Knowledge Graph
- Automatic Web Crawling
- REST API
- Docker Deployment
- Authentication
- Conversation Memory

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push your branch
5. Open a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Srujan Kindikeri**

B.Tech CSE (Data Science & Data Engineering)

GitHub: https://github.com/SrujanKindikeri

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates further development.

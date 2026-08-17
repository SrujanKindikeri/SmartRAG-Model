# 🚀 SmartRAG

A production-ready **Retrieval-Augmented Generation (RAG)** system that learns from your documents and answers questions using local LLMs through **Ollama**.

---

# Features

- 📄 PDF, DOCX and TXT support
- ⚡ Incremental indexing
- 🧠 Semantic search using Sentence Transformers
- 🗂 Persistent ChromaDB vector database
- 🤖 Local LLM support via Ollama
- 💬 Conversation memory
- 📚 Source-aware answers
- 🔄 Automatic document updates
- 🖥 Terminal interface
- 🔒 100% Local (No OpenAI API Required)

---

# Project Structure

```text
SmartRAG/
│
├── data/
│   ├── documents/
│   ├── processed/
│   └── unanswered_questions.json
│
├── logs/
├── metadata/
├── models/
│
├── src/
│   ├── chunking.py
│   ├── config.py
│   ├── database.py
│   ├── embeddings.py
│   ├── llm.py
│   ├── loader.py
│   ├── memory.py
│   ├── prompt_builder.py
│   ├── rag.py
│   ├── search.py
│   └── utils.py
│
├── vector_db/
├── indexer.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/yourusername/SmartRAG.git

cd SmartRAG
```

Create virtual environment

```bash
python -m venv venv
```

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

# Install Ollama

Install Ollama

https://ollama.com

Download a model

```bash
ollama pull llama3.2:3b
```

Start Ollama

```bash
ollama serve
```

---

# Add Documents

Place all your documents inside

```text
data/documents/
```

Example

```text
data/documents/

AI.pdf

Python.pdf

ML.docx

Notes.txt
```

---

# Build Vector Database

Run

```bash
python indexer.py
```

Only new or modified documents are indexed.

---

# Ask Questions

```bash
python main.py
```

Example

```text
You:
What is Machine Learning?

SmartRAG:
Machine Learning is a branch of Artificial Intelligence...
```

---

# Architecture

```text
Documents

↓

Loader

↓

Chunker

↓

Embedding Model

↓

ChromaDB

↓

Retriever

↓

Prompt Builder

↓

Ollama

↓

Answer
```

---

# Tech Stack

- Python
- ChromaDB
- Sentence Transformers
- Ollama
- PyMuPDF
- python-docx
- Requests

---

# Roadmap

- [x] Incremental indexing
- [x] Persistent vector database
- [x] Conversation memory
- [x] Local LLM
- [ ] Hybrid Search
- [ ] Reranking
- [ ] Multi-document citations
- [ ] Telegram Bot
- [ ] REST API
- [ ] Web Interface
- [ ] Multi-user support

---

# License

MIT License# RagModel-For-ML

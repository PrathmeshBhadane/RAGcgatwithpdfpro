# AI chat with pdf system

A lightweight PDF document processing and retrieval prototype built with Python. This repository is designed to ingest PDF content, create a searchable vector store, and support retrieval-augmented generation for document-based question answering.

## Features

- PDF text extraction and processing
- Vector embedding storage with FAISS
- Retrieval-augmented responses from document context
- Simple pipeline structure for rapid prototyping

## Repository Structure

- `app.py` — Main application entrypoint or Flask/FastAPI server starter
- `main.py` — Alternative execution script or command-line helper
- `README.md` — Project documentation
- `requirements.txt` — Python dependencies
- `data/` — Input data or downloaded documents
- `rag/pipeline.py` — RAG pipeline and vector store creation logic
- `vectorstore/index.faiss` — Serialized FAISS vector index

## Installation

1. Create a Python virtual environment:

```powershell
python -m venv .venv
```

2. Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Usage

- Run the main application:

```powershell
python app.py
```

- Or execute the alternate entrypoint:

```powershell
python main.py
```

## Notes

- Ensure the `vectorstore/` folder exists and contains a valid `index.faiss` file before running retrieval operations.
- Update the `requirements.txt` file if additional libraries are required for your specific PDF processing or embedding workflow.

## License

This project is provided as-is for experimentation and prototyping.

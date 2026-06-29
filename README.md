# ClauseIQ

ClauseIQ is a personal document intelligence project for asking natural-language questions over uploaded documents. It accepts PDF and DOCX files, extracts their text, retrieves the most relevant passages with vector search, and returns concise answers generated from the retrieved document context.

The project is intentionally small and practical: a FastAPI backend handles document parsing, embeddings, retrieval, and LLM calls, while a lightweight HTML frontend provides a simple upload-and-query interface.

## Objectives

- Make document review faster by answering questions directly from uploaded files.
- Support both single-question and multi-question workflows.
- Keep answers grounded in the source document instead of open-ended model knowledge.
- Provide a simple local interface that can also be deployed as an API service.

## Features

- PDF and DOCX text extraction.
- File upload endpoint for browser-based use.
- URL-based document endpoint for API integrations.
- Overlapping text chunking for better retrieval coverage.
- Sentence Transformer embeddings using `all-MiniLM-L6-v2`.
- FAISS similarity search for retrieving relevant chunks.
- OpenRouter-backed LLM responses.
- Static frontend with document upload, question input, and formatted results.
- Health check endpoint for deployment monitoring.

## How It Works

1. A user uploads a PDF or DOCX file and submits one or more questions.
2. The backend extracts raw text from the document.
3. Text is split into overlapping chunks.
4. Each chunk is embedded with a Sentence Transformer model.
5. FAISS indexes the embeddings and retrieves the most relevant chunks for each question.
6. The retrieved context and question are sent to the configured OpenRouter model.
7. ClauseIQ returns answers in the same order as the submitted questions.

## Tech Stack

- **Backend:** FastAPI, Uvicorn, Pydantic
- **Document parsing:** pdfplumber, python-docx
- **Embeddings:** sentence-transformers
- **Vector search:** FAISS
- **LLM provider:** OpenRouter
- **Frontend:** HTML, Tailwind via CDN, vanilla JavaScript
- **Deployment config:** Render-compatible `render.yml`

## Project Structure

```text
ClauseIQ/
|-- backend/
|   |-- app/
|   |   |-- api/
|   |   |   `-- routes.py              # API endpoints
|   |   |-- core/
|   |   |   |-- config.py              # Environment-based settings
|   |   |   `-- pipeline.py            # Document QA orchestration
|   |   |-- models/
|   |   |   `-- schemas.py             # Request and response models
|   |   `-- services/
|   |       |-- document_loader.py     # PDF/DOCX loading and parsing
|   |       |-- embedder.py            # Chunking and FAISS index creation
|   |       |-- retriever.py           # Similarity search
|   |       `-- llm.py                 # OpenRouter answer generation
|   |-- main.py                        # FastAPI application entrypoint
|   |-- requirements.txt               # Python dependencies
|   |-- .env.example                   # Environment variable template
|   `-- render.yml                     # Deployment configuration
|-- frontend/
|   `-- index.html                     # Static browser interface
`-- README.md
```

## API Endpoints

### `GET /`

Returns a welcome message.

### `GET /health`

Returns service health information.

```json
{
  "status": "ok",
  "app": "ClauseIQ"
}
```

### `POST /api/v1/query/upload`

Accepts a multipart form upload from the frontend.

Form fields:

- `file`: PDF or DOCX file.
- `questions`: either a plain question string or a JSON array of question strings.

Example `questions` values:

```json
["What is the grace period?", "Is cancellation allowed?"]
```

or:

```text
What is the effective date?
```

Response:

```json
{
  "answers": [
    "Answer to the first question.",
    "Answer to the second question."
  ]
}
```

### `POST /api/v1/query/run`

Accepts a document URL and a list of questions.

Request body:

```json
{
  "documents": "https://example.com/document.pdf",
  "questions": [
    "What is the termination clause?"
  ]
}
```

Response:

```json
{
  "answers": [
    "The termination clause states..."
  ]
}
```

## Setup

### Prerequisites

- Python 3.10 or newer
- An OpenRouter API key

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Update `.env` with your OpenRouter credentials:

```env
OPENROUTER_API_KEY="your_openrouter_api_key_here"
OPENROUTER_MODEL="openrouter/auto"
```

Run the API:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API docs are available at:

```text
http://127.0.0.1:8000/docs
```

### Frontend

The frontend is a static HTML file:

```text
frontend/index.html
```

Open it in a browser after the backend is running. The frontend currently sends requests to:

```text
http://127.0.0.1:8000/api/v1/query/upload
```

## Configuration

The backend settings are defined in `backend/app/core/config.py`.

| Setting | Environment variable | Default | Purpose |
| --- | --- | --- | --- |
| `openrouter_api_key` | `OPENROUTER_API_KEY` | empty | API key used for OpenRouter requests |
| `model_name` | `OPENROUTER_MODEL` | `openrouter/auto` | LLM model used for answer generation |
| `chunk_size` | not currently externalized | `500` | Number of words per text chunk |
| `chunk_overlap` | not currently externalized | `50` | Word overlap between chunks |
| `top_k` | not currently externalized | `5` | Number of chunks retrieved per question |

## Deployment Notes

The backend includes a Render service configuration in `backend/render.yml`.

Expected deployment command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Set `OPENROUTER_API_KEY` in the deployment provider's environment settings. The `/health` endpoint can be used as the health check path.

## Limitations

- The vector index is built in memory for each request, so very large documents may take longer to process.
- Extracted answer quality depends on the clarity of document text extraction and the selected OpenRouter model.
- Scanned PDFs without embedded text are not OCR-processed.
- The static frontend is configured for a local backend URL and should be updated before production hosting.

## License

No license has been specified yet.

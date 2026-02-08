# Action Item Extractor

A FastAPI + SQLite application that converts free-form notes into structured, actionable items. Supports both heuristic-based extraction and LLM-powered extraction via Ollama.

## Setup

### Prerequisites

- Python 3.10+
- [Conda](https://docs.conda.io/) (for environment management)
- [Poetry](https://python-poetry.org/) (for dependency management)
- [Ollama](https://ollama.com/) (for LLM extraction)

### Installation

1. Activate the conda environment:
   ```bash
   conda activate cs146s
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Pull the LLM model for Ollama:
   ```bash
   ollama pull llama3.1:8b
   ```

## Running the Application

Start the development server from the project root:

```bash
poetry run uvicorn week2.app.main:app --reload
```

Open http://127.0.0.1:8000/ in your browser.

## API Endpoints

### Notes

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/notes` | Create a new note |
| `GET` | `/notes` | List all saved notes |
| `GET` | `/notes/{note_id}` | Retrieve a single note by ID |

### Action Items

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/action-items/extract` | Extract action items using heuristic rules |
| `POST` | `/action-items/extract-llm` | Extract action items using LLM (Ollama) |
| `GET` | `/action-items` | List all action items (optional `?note_id=` filter) |
| `POST` | `/action-items/{id}/done` | Mark an action item as done/undone |

### Frontend

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serves the HTML frontend |

## Running Tests

```bash
poetry run pytest week2/tests/ -v
```

The test suite covers both heuristic and LLM-based extraction. LLM tests use mocked Ollama responses so they run without a live model.

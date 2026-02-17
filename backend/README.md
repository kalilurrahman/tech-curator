# TechCurator Backend

The backend for TechCurator is a FastAPI application designed to aggregate, deduplicate, and cluster tech news from various sources. It leverages Google's Gemini API for summarization and labeling.

## Features

- **News Aggregation**: Fetches news from RSS feeds.
- **Deduplication**: Uses `datasketch` (MinHash/LSH) to identify and remove duplicate articles.
- **Clustering**: Groups similar stories using `sentence-transformers` and `scikit-learn` (DBSCAN/KMeans).
- **AI Integration**: Utilizes Google Gemini API for generating concise summaries and topic labels.
- **API**: Exposes RESTful endpoints for the frontend to consume.

## Project Structure

- `app/main.py`: The entry point of the FastAPI application.
- `app/models.py`: Pydantic models for data validation and structure.
- `app/services/`: Contains the core logic modules.
  - `ingestion.py`: Handles fetching news from external sources.
  - `dedupe.py`: Implements deduplication logic.
  - `clustering.py`: Manages story clustering.
  - `llm.py`: Interfaces with the Google Gemini API.

## Requirements

- Python 3.9+
- `fastapi`
- `uvicorn`
- `requests`
- `feedparser`
- `datasketch`
- `scikit-learn`
- `sentence-transformers`
- `google-generativeai`
- `python-dotenv`
- `pydantic`

## Setup & Installation

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the `backend` directory (or use the root `.env`) and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Running the Application

Start the development server using Uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### `GET /feed`
Retrieves the current list of clustered stories.

**Response:**
```json
[
  {
    "id": "cluster_id",
    "label": "TOPIC_LABEL",
    "summary": "AI-generated summary of the cluster.",
    "articles": [
      {
        "title": "Article Title",
        "url": "https://example.com/article",
        "source": "Source Name",
        "published_at": "2023-10-27T10:00:00Z"
      },
      ...
    ]
  },
  ...
]
```

### `POST /refresh`
Triggers the ingestion pipeline (fetch -> dedupe -> cluster) in the background.

**Response:**
```json
{
  "status": "Ingestion triggered"
}
```

## Development

To add new features or modify existing logic, check the `app/services` directory. The application uses a modular design to keep concerns separated.

# TechCurator PWA

A 'Zero-UI' News Aggregator for Tech Professionals.

TechCurator is an intelligent news aggregation platform designed to declutter your tech news feed. It fetches articles from various sources, deduplicates them, clusters similar stories, and uses AI to generate concise summaries and topic labels. The result is a clean, focused stream of information delivered via a Progressive Web App (PWA).

## Features

- **Automated Aggregation**: Continuously fetches tech news from RSS feeds.
- **Smart Deduplication**: Identifies and merges duplicate articles using MinHash algorithms.
- **Intelligent Clustering**: Groups related stories together to reduce noise.
- **AI-Powered Summaries**: Uses Google Gemini API to provide brief, relevant summaries for each story cluster.
- **Search & Filtering**: Real-time searching of news stories by title, summary, or topic.
- **Zero-UI Design**: A minimalist interface that prioritizes content over clutter.
- **PWA Experience**: Installable on mobile and desktop, with offline capabilities.

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Data Processing**: `datasketch` (Deduplication), `scikit-learn` & `sentence-transformers` (Clustering)
- **AI/LLM**: Google Gemini API
- **Containerization**: Docker

### Frontend
- **Framework**: SvelteKit (Node.js)
- **Styling**: Tailwind CSS
- **PWA**: Service Workers for offline support and installation

## Project Structure

```
.
├── backend/            # FastAPI backend application
│   ├── app/            # Application source code
│   │   ├── services/   # Core logic (ingestion, dedupe, clustering, llm)
│   │   └── ...
│   ├── Dockerfile      # Backend Docker configuration
│   └── requirements.txt
├── frontend/           # SvelteKit frontend application
│   ├── src/            # Frontend source code
│   ├── Dockerfile      # Frontend Docker configuration
│   └── package.json
├── docs/               # Documentation assets
├── scripts/            # Utility scripts
│   └── capture_screenshots.py
├── docker-compose.yml  # Docker Compose orchestration
└── README.md           # This file
```

## Quick Start (Docker)

The easiest way to run TechCurator is using Docker Compose.

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd tech-curator
    ```

2.  **Configure Environment:**
    Create a `.env` file in the root directory and add your Google Gemini API key:
    ```env
    GEMINI_API_KEY=your_gemini_api_key_here
    ```

3.  **Run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```

    - Backend API: `http://localhost:8000`
    - Frontend App: `http://localhost:5173`

## Manual Setup

If you prefer to run the services individually without Docker, follow these steps.

### Backend

1.  Navigate to `backend/`.
2.  Install dependencies: `pip install -r requirements.txt`.
3.  Set `GEMINI_API_KEY` in `backend/.env`.
4.  Run the server: `uvicorn app.main:app --reload`.

### Frontend

1.  Navigate to `frontend/`.
2.  Install dependencies: `npm install`.
3.  Run the development server: `npm run dev`.

## Screenshots

<div align="center">
  <h3>Desktop View</h3>
  <img src="docs/screenshots/desktop_feed.png" alt="Desktop Feed" width="800"/>

  <h3>Mobile View</h3>
  <img src="docs/screenshots/mobile_feed.png" alt="Mobile Feed" width="375"/>
</div>

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the project.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## License

This project is licensed under the MIT License.

# RAG System Tester - Streamlit Frontend

A modern, user-friendly Streamlit interface for testing and interacting with the RAG (Retrieval-Augmented Generation) API.

## Features

- 💬 **Chat Tab**: Ask questions and get AI-generated answers based on indexed documents
- 📤 **Upload & Process Tab**: Upload and process documents for indexing
- 🔎 **Search Tab**: Semantic search through indexed documents
- 📊 **Index Info Tab**: View vector database index statistics

## Quick Start

### Prerequisites

Make sure the Docker Compose stack is running:

```bash
cd /mnt/m/Others/Fathi/RAG_001/Docker
docker compose up -d
```

### Install Dependencies

```bash
cd /mnt/m/Others/Fathi/RAG_001/streamlit_app
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run app.py
```

The app will be available at: **http://localhost:8501**

## API Endpoints Used

| Endpoint                                | Method | Description               |
| --------------------------------------- | ------ | ------------------------- |
| `/api/v1/`                              | GET    | Health check              |
| `/api/v1/data/upload/{project_id}`      | POST   | Upload files              |
| `/api/v1/data/process/{project_id}`     | POST   | Process files into chunks |
| `/api/v1/nlp/index/push/{project_id}`   | POST   | Index chunks to vector DB |
| `/api/v1/nlp/index/info/{project_id}`   | GET    | Get index info            |
| `/api/v1/nlp/index/search/{project_id}` | POST   | Semantic search           |
| `/api/v1/nlp/index/answer/{project_id}` | POST   | RAG-based Q&A             |

## UI Design

The interface features:

- Modern dark theme with gradient accents
- Glassmorphism effects
- Responsive layout
- Status indicators
- Chat history persistence

## Configuration

In the sidebar, you can configure:

- **API Base URL**: Default is `http://localhost:8000/api/v1`
- **Project ID**: Select which project to work with
- **API Health Check**: Verify API connectivity

## Quick Links (when running locally)

- 📊 Grafana: http://localhost:3000
- 📈 Prometheus: http://localhost:9090
- 🔍 Qdrant Dashboard: http://localhost:6333/dashboard
- 📚 FastAPI Swagger Docs: http://localhost:8000/docs

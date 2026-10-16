# FastAPI Prometheus Telemetry Service

A lightweight, production-oriented **FastAPI microservice** featuring real-time Prometheus metrics, structured JSON request logging, and health monitoring. The service includes a work simulation endpoint, request tracking, uptime reporting, and recent log retrieval.

![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?style=flat&logo=FastAPI&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?style=flat&logo=python&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-E6522C.svg?style=flat&logo=prometheus&logoColor=white)
![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7.svg?style=flat&logo=render&logoColor=white)

---

## 🚀 Live Deployment

**Base URL:** https://fastapi-prometheus-telemetry.onrender.com

Interactive API documentation: [Swagger UI](https://fastapi-prometheus-telemetry.onrender.com/docs)

## ✨ Features

- **Work Simulation (`/work`):** Executes a configurable number of work units and tracks incoming HTTP requests.
- **Prometheus Metrics (`/metrics`):** Exposes metrics in Prometheus text exposition format.
- **Health Monitoring (`/healthz`):** Reports service status and uptime in seconds.
- **Structured JSON Logging (`/logs/tail`):** Retrieves recent request logs containing timestamps, request paths, log levels, and unique request IDs.
- **Request Tracking:** Uses UUIDs to identify individual requests.
- **API Documentation:** Provides interactive API exploration through FastAPI's Swagger UI.
- **Docker Support:** Includes a Dockerfile for containerized deployment.

## 📌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/work` | Simulates work and records request metrics |
| GET | `/metrics` | Exposes Prometheus metrics |
| GET | `/healthz` | Returns service health and uptime |
| GET | `/logs/tail` | Returns recent structured request logs |
| GET | `/docs` | Opens interactive Swagger API documentation |

### 1. Work Simulation

**Endpoint:** `GET /work`

Simulates work for a specified number of units and optionally associates the request with an email address.

**Query parameters**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `n` | Integer | `1` | Number of work units to execute |
| `email` | String | `user@example.com` | Email tag associated with the request |

**Example request**

```bash
curl "https://fastapi-prometheus-telemetry.onrender.com/work?n=5"
```

**Example response**

```json
{
  "email": "user@example.com",
  "done": 5
}
```

### 2. Prometheus Metrics

**Endpoint:** `GET /metrics`

Exposes application metrics in Prometheus-compatible text format, allowing monitoring systems to scrape the service.

**Example request**

```bash
curl "https://fastapi-prometheus-telemetry.onrender.com/metrics"
```

**Example metric**

```text
# HELP http_requests_total Total HTTP requests received
# TYPE http_requests_total counter
http_requests_total 42.0
```

The metric value shown above is illustrative; the actual value depends on requests received by the running service.

**Content type**

```text
text/plain; version=0.0.4; charset=utf-8
```

### 3. Health Check

**Endpoint:** `GET /healthz`

Returns the service health status and the time elapsed since the application started.

**Example request**

```bash
curl "https://fastapi-prometheus-telemetry.onrender.com/healthz"
```

**Example response**

```json
{
  "status": "ok",
  "uptime_s": 128.4521
}
```

The uptime value is illustrative and changes while the service runs.

### 4. Recent Request Logs

**Endpoint:** `GET /logs/tail`

Returns recent structured JSON log records captured by the application's request middleware.

**Query parameters**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `limit` | Integer | `10` | Number of recent log records to return |

**Example request**

```bash
curl "https://fastapi-prometheus-telemetry.onrender.com/logs/tail?limit=5"
```

**Example response**

```json
[
  {
    "level": "INFO",
    "ts": "2026-10-16T15:30:00.000000+00:00",
    "path": "/work?n=5",
    "request_id": "a3b1c2d3-e4f5-6789-0123-456789abcdef"
  }
]
```

The response is illustrative. Actual log records depend on requests handled by the service.

## 🧪 Quick Testing with cURL

Run the following commands to test the deployed service.

```bash
# 1. Trigger work execution
curl "https://fastapi-prometheus-telemetry.onrender.com/work?n=5"

# 2. Check health and uptime
curl "https://fastapi-prometheus-telemetry.onrender.com/healthz"

# 3. Inspect Prometheus request metrics
curl -s "https://fastapi-prometheus-telemetry.onrender.com/metrics" \
  | grep http_requests_total

# 4. Retrieve the latest request logs
curl "https://fastapi-prometheus-telemetry.onrender.com/logs/tail?limit=5"
```

## 🛠️ Local Development and Setup

### Prerequisites

- Python 3.11 or later
- pip
- Git
- Docker (optional)

### 1. Clone the repository

Replace `YOUR_USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR_USERNAME/fastapi-prometheus-telemetry.git
cd fastapi-prometheus-telemetry
```

### 2. Create a virtual environment

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the development server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:

- API base URL: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Prometheus metrics: http://127.0.0.1:8000/metrics
- Health check: http://127.0.0.1:8000/healthz

## 🐳 Docker Support

Build and run the application in a Docker container.

### 1. Build the image

```bash
docker build -t fastapi-prometheus-telemetry .
```

### 2. Run the container

```bash
docker run -d \
  -p 8000:8000 \
  --name fastapi-telemetry \
  fastapi-prometheus-telemetry
```

### 3. Verify the container

```bash
docker ps
curl "http://localhost:8000/healthz"
```

To stop and remove the container:

```bash
docker stop fastapi-telemetry
docker rm fastapi-telemetry
```

## 📁 Repository Structure

```text
fastapi-prometheus-telemetry/
├── main.py             # FastAPI application, routes, and middleware
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker image configuration
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Core programming language |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| prometheus_client | Prometheus metric collection and exposition |
| JSON logging | Structured request log records |
| UUID | Unique request identification |
| Docker | Containerization |
| Render | Cloud deployment |

## 📊 Monitoring Workflow

1. A client sends a request to the FastAPI service.
2. Middleware captures request information and associates it with a unique request ID.
3. The application processes the request and updates the relevant metrics.
4. Prometheus-compatible metrics are exposed through `/metrics`.
5. The `/healthz` endpoint reports application status and uptime.
6. The `/logs/tail` endpoint provides access to recent structured log records.

## 🔒 Production Considerations

This project demonstrates core observability features for a FastAPI service. Before using it in a production environment, consider:

- Adding authentication and access controls for sensitive endpoints.
- Configuring Prometheus scraping and alerting rules.
- Exporting logs to a centralized logging platform.
- Applying request validation, rate limiting, and sensible resource limits.
- Using persistent or external storage if logs must survive application restarts.
- Configuring deployment health checks, timeouts, and graceful shutdown.
- Avoiding sensitive information, such as personal data, in logs and metric labels.

**Note:** Exposing metrics and log endpoints publicly may reveal operational information. Restrict access when necessary. Actual production readiness depends on the application's implementation and deployment configuration.


**Built with FastAPI and Prometheus for lightweight API observability.**

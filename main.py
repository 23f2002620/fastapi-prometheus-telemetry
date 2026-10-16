import time
import uuid
from datetime import datetime, timezone
from collections import deque
from typing import List, Dict, Any

from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="Instrumented FastAPI Service")

# Startup timestamp tracking
START_TIME = time.time()

# Prometheus counter for total HTTP requests
REQUEST_COUNTER = Counter("http_requests_total", "Total HTTP requests received")

# In-memory ring buffer for logs (retains the last 1000 entries)
MAX_LOG_ENTRIES = 1000
LOG_BUFFER: deque = deque(maxlen=MAX_LOG_ENTRIES)


@app.middleware("http")
async def middleware_instrumentation(request: Request, call_next):
    # Increment Prometheus counter on every incoming request
    REQUEST_COUNTER.inc()

    # Generate unique request ID
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start_ts = datetime.now(timezone.utc).isoformat()
    
    # Process request
    response = await call_next(request)

    # Capture raw path with query string if present
    full_path = request.url.path
    if request.url.query:
        full_path += f"?{request.url.query}"

    # Build structured log record
    log_entry = {
        "level": "INFO" if response.status_code < 400 else "ERROR",
        "ts": start_ts,
        "path": full_path,
        "request_id": request_id,
    }
    LOG_BUFFER.append(log_entry)

    response.headers["X-Request-ID"] = request_id
    return response


@app.get("/work")
async def do_work(n: int = 1, email: str = "user@example.com"):
    # Perform K units of computation
    accumulator = 0
    for i in range(n):
        accumulator += (i + 1) ** 2

    return {"email": email, "done": n}


@app.get("/metrics")
async def get_metrics():
    # Return standard Prometheus exposition text format
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/healthz")
async def health_check():
    uptime = time.time() - START_TIME
    return {"status": "ok", "uptime_s": round(uptime, 4)}


@app.get("/logs/tail")
async def get_log_tail(limit: int = 10):
    logs = list(LOG_BUFFER)
    if limit > 0:
        return logs[-limit:]
    return []
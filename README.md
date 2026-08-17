#  FastAPI Social Media API

A robust backend for a social media platform built with **FastAPI**, **PostgreSQL**, and **Docker** — JWT authentication, full post/vote CRUD, Alembic migrations, and a pytest + Locust testing suite.

This project focuses on high-concurrency optimization: verified clean scaling up to **500 concurrent users**, with a specific, diagnosed breaking point beyond that (details below, not just a number).

---

##  Setup & Installation

### 1. Prerequisites
- Python 3.10+
- Docker Desktop (Recommended)
  **OR**
- PostgreSQL 15+

---

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
DB_HOST=db
DB_NAME=fastapi
DB_USER=postgres
DB_PASSWORD=your_password

SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

### 3. Running with Docker (Recommended)

This method is optimized for high concurrency and avoids Windows networking limitations.

```bash
# 1. Build and start containers
docker-compose up --build -d

# 2. Run database migrations
docker-compose exec app alembic upgrade head

# 3. Create a test user
curl -X POST "http://localhost:8000/users/" \
-H "Content-Type: application/json" \
-d "{\"email\": \"hello124@gmail.com\", \"password\": \"password123\"}"

# 4. Verify login
curl -X POST "http://localhost:8000/login" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=hello124@gmail.com&password=password123"
```

---

### 4. Running Locally (venv)

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn app.main:app --reload
```

---

##  Load Testing: What Actually Happens Under Concurrency

This API was stress-tested with **Locust**, staged at 100 / 250 / 500 concurrent users, resetting `posts`/`votes` between stages (`reset_db.py`) to keep each run comparable. Full raw reports for all three stages are attached in [`load_testing/`](load_testing/) — open any of them in a browser for the interactive charts.

### Results

| Metric | 100 users | 250 users | 500 users |
|---|---|---|---|
| Failure rate | 0.08% | 0.33% | **5.25%** |
| Aggregate RPS | 41.3 | 96.7 | 114.2 |
| Avg latency | 62.8 ms | 66.9 ms | 1228.6 ms |
| p50 (median) | 16 ms | 30 ms | 210 ms |
| p95 latency | 110 ms | 130 ms | 6,300 ms |
| p99 latency | 610 ms | 1,000 ms | 9,600 ms |

Scaling is clean and near-linear from 100 → 250 users. At 500 users, throughput growth flattens and tail latency (p99) jumps ~10x — the system has hit a real, specific limit, not a vague "it got slower."

### Root cause (not just "it broke")

Breaking down every failure at the 500-user stage instead of just reporting the failure %:

| Failure type | Share of failures |
|---|---|
| `401 Unauthorized` cascades on `/posts/` | 64% |
| `RemoteDisconnected` (connection dropped mid-request) | 29% |
| Client-side socket errors (`WinError 10053`/`10054`) | 7% |

##  Testing Suite

### Unit & Integration Testing

```bash
pytest
```

### Load Testing

```bash
# Start Locust
locust -f locustfile.py --host http://localhost:8000
```
Open `http://localhost:8089`, set concurrency/ramp rate, and run. Reset data between stages with `python reset_db.py` (truncates `posts`/`votes` only).

---

##  Future Roadmap

###  Redis Caching
- Cache `GET /posts/` reads to cut DB load
- **Note:** based on the root-cause analysis above, Redis would *not* have fixed the 500-user failures directly — those were login/CPU/networking issues, not database read load. It's still a valid next step for reducing read latency and DB pressure independently, just not a fix for the bottleneck actually found.

###  Async / Offloaded Password Hashing
- Move Argon2 verification off the request thread pool (e.g. `run_in_threadpool` tuning, or a dedicated worker queue) to directly address the diagnosed root cause above.

###  NGINX Load Balancing
- Reverse proxy, SSL termination, smarter request distribution across multiple app instances.

###  Cloud Deployment
- AWS (ECS + RDS) or Render, with a public production endpoint.

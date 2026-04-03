#  FastAPI High-Performance Social Media API

A robust, production-ready backend for a social media platform built with **FastAPI**, **PostgreSQL**, and **Docker**.

This project focuses on high-concurrency optimization, successfully scaling to handle **1,000 concurrent users**.

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
DATABASE_HOSTNAME=db
DATABASE_PORT=5432
DATABASE_PASSWORD=your_password
DATABASE_NAME=fastapi
DATABASE_USERNAME=postgres

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

##  The Testing Journey: Scaling to 1,000 Users

As part of an engineering exploration at **IIT Guwahati**, this API was stress-tested using **Locust** to uncover real-world bottlenecks.

---

###  The Struggles & Bottlenecks

- **64 Connection Limit (Windows)**  
  Encountered:
  ```
  ValueError: too many file descriptors in select()
  ```
  Fixed by moving to Docker (Linux `epoll`)

- **Connection Starvation**  
  Default SQLAlchemy pool size (`5`) caused **100% failures at 200 users**

- **CPU Saturation**  
  Argon2 password hashing maxed CPU → **34% failure rate at 1,000 users**

---

###  The Breakthrough (12% Failure Rate)

Optimized system to handle **1,000 users (spawn rate = 2)** with only **12% failures**:

- **Engine Tuning**
  ```python
  pool_size=50
  max_overflow=100
  ```

- **PostgreSQL Scaling**
  ```
  max_connections = 300
  ```

- **Multi-Worker Scaling**
  - 4 Uvicorn workers (Docker)

- **Data Hygiene**
  - `reset_db.py` script to truncate tables between tests

---

##  Testing Suite

### Unit & Integration Testing

```bash
pytest
```

---

### Load Testing

```bash
# Start Locust
locust -f locustfile.py
```
---

##  Future Roadmap: Path to 0% Failures

To push beyond current limits and scale to **5,000+ users**:

###  Redis Caching
- Cache `GET /posts/`
- Store JWT user objects in memory  
Reduce DB load by ~80%

---

###  NGINX Load Balancing
- Reverse proxy
- SSL termination
- Smarter request distribution

---

###  Cloud Deployment
- AWS (ECS + RDS) or Render
- Public production endpoint

---


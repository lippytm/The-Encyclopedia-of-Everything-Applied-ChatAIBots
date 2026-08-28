# B-052: Your First Docker Container

> *"A container is a promise: 'It works on my machine' becomes 'It works on every machine.'"*

---

## Learning Objectives

By the end of this book you will:

1. Understand what Docker is and why containers replaced VMs for most workloads
2. Write a `Dockerfile` for a Python application
3. Build, run, inspect, and debug containers with `docker` CLI
4. Use `.dockerignore` to keep images lean
5. Run multi-container setups with `docker compose`
6. Earn the `CSEL-L1-B052-ContainerEngineer` credential

---

## Chapter 1: Containers vs Virtual Machines

| Aspect | Virtual Machine | Container |
|---|---|---|
| Isolation | Full OS | Process + filesystem namespace |
| Boot time | 30–120 seconds | <1 second |
| Image size | 1–20 GB | 10–500 MB |
| Overhead | High (hypervisor) | Minimal (kernel namespaces) |
| Portability | Moderate | Excellent |

Docker packages your app + dependencies into a **layer-based image**. Every `RUN` instruction adds a read-only layer. The container is a writable layer on top.

---

## Chapter 2: Writing Your First Dockerfile

```dockerfile
# Use an official Python runtime as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies first (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port the app listens on
EXPOSE 8000

# Run the application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Key principles:
- **Order matters** — copy `requirements.txt` before code to cache the pip layer
- **`python:3.12-slim`** over full image — ~50 MB vs ~1 GB
- **`--no-cache-dir`** — never store pip cache in the image layer

---

## Chapter 3: .dockerignore

```
# .dockerignore
__pycache__/
*.pyc
*.pyo
.env
.env.*
.git/
.gitignore
*.md
tests/
.pytest_cache/
.mypy_cache/
node_modules/
dist/
build/
```

Every file NOT in `.dockerignore` is sent to the build context. A missing `.dockerignore` is the #1 cause of bloated images and leaked secrets.

---

## Chapter 4: Build and Run

```bash
# Build the image
docker build -t lippytmai/commit-reporter:latest .

# Run the container
docker run --rm \
  -e GITHUB_TOKEN=$GITHUB_TOKEN \
  lippytmai/commit-reporter:latest \
  python3 commit_reporter.py local .

# Run an interactive shell for debugging
docker run --rm -it lippytmai/commit-reporter:latest bash

# Inspect image layers
docker history lippytmai/commit-reporter:latest

# Check image size
docker images lippytmai/commit-reporter:latest
```

---

## Chapter 5: Debugging Containers

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# View logs from a running container
docker logs <container_id>

# Follow logs in real time
docker logs -f <container_id>

# Execute a command inside a running container
docker exec -it <container_id> bash

# Inspect container metadata (mounts, env, network)
docker inspect <container_id>

# Copy a file out of a stopped container
docker cp <container_id>:/app/output.json ./output.json
```

---

## Chapter 6: Docker Compose for Multi-Container Apps

```yaml
# docker-compose.yml
version: "3.9"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - DATABASE_URL=******db:5432/myapp
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d myapp"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

```bash
# Start all services
docker compose up -d

# Stop and remove containers (keep volumes)
docker compose down

# Stop and remove containers + volumes
docker compose down -v

# View logs for the api service
docker compose logs -f api
```

---

## Chapter 7: Proof of Work — Containerized Python App

Build and run the `commit_reporter.py` from B-051 inside Docker:

```dockerfile
# Dockerfile.reporter
FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir gitpython PyGithub
COPY commit_reporter.py .
ENTRYPOINT ["python3", "commit_reporter.py"]
```

```bash
# Build
docker build -f Dockerfile.reporter -t commit-reporter:b052 .

# Run local mode (mount current directory)
docker run --rm -v "$(pwd):/workspace" commit-reporter:b052 local /workspace

# Run remote mode (pass GitHub token via env)
docker run --rm \
  -e GITHUB_TOKEN="${GITHUB_TOKEN}" \
  commit-reporter:b052 \
  remote lippytm/The-Encyclopedia-of-Everything-Applied-ChatAIBots --days 3
```

Expected output: JSON commit report printed to stdout, zero code changes on host machine.

**Credential earned:** `CSEL-L1-B052-ContainerEngineer`

---

## Further Reading

- 📄 [`docs/B-051-git-with-python.md`](B-051-git-with-python.md) — The app we just containerized
- 📄 [`docs/B-053-environment-variables-and-security.md`](B-053-environment-variables-and-security.md) — Secrets in containers
- 📄 [`docs/ai-clone-engine-swarms.md`](ai-clone-engine-swarms.md) — ACSS CSEL layer
- 🏠 [`README.md`](../README.md) — Encyclopedia home

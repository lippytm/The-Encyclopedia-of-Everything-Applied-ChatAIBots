# B-012: The Container That Held Everything

### Docker Basics — Run Any Software, Anywhere, Without Breaking Anything

> *"Docker solves the oldest problem in software: 'but it works on my machine.' A Docker container packages your code and everything it needs to run — OS libraries, language runtime, dependencies, config — into a single, portable unit. It runs identically on your laptop, a teammate's Linux box, and a production cloud server."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Explain what a container is and how it differs from a virtual machine
2. Pull and run Docker images from Docker Hub
3. Write a `Dockerfile` to containerize a Python application
4. Use `docker-compose` to run multi-container applications (app + database)
5. Run PostgreSQL locally in Docker without installing it on your machine

**Prerequisite:** B-001 through B-011

**Build Artifact:** A `docker-compose.yml` that runs PostgreSQL + your Python project, with environment variables loaded from `.env`

**Credential:** `CSEL-L0-B012-ContainerPilot` — on-chain on Base

---

## Chapter 1: Containers vs. Virtual Machines

| Property | Virtual Machine | Container |
|---|---|---|
| **Isolation** | Full OS + kernel | Process-level (shares host kernel) |
| **Size** | GBs | MBs |
| **Startup time** | Minutes | Seconds (often <1s) |
| **Resource overhead** | High | Low |
| **Portability** | VM image (large) | Docker image (layered, cached) |
| **Use case** | Full OS isolation, legacy apps | Microservices, dev environments, CI/CD |

A container is like a shipping container for software: standardized shape, sealed contents, runs the same on any crane (any Linux host with Docker). *[Reality — Docker containers share the host Linux kernel; they are not full VMs]*

---

## Chapter 2: Docker Core Concepts

| Concept | What It Is |
|---|---|
| **Image** | A read-only template (like a class) |
| **Container** | A running instance of an image (like an object) |
| **Dockerfile** | Instructions to build a custom image |
| **Registry** | Storage for images (Docker Hub, GitHub Container Registry) |
| **Volume** | Persistent storage outside the container |
| **Network** | Virtual network connecting containers |

---

## Chapter 3: Docker Installation

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose-plugin
sudo usermod -aG docker $USER
newgrp docker

# Arch/OMARCHY
sudo pacman -S docker docker-compose
sudo systemctl enable --now docker
sudo usermod -aG docker $USER

# Verify
docker --version
docker run hello-world
```

---

## Chapter 4: Essential Docker Commands

```bash
# Pull an image from Docker Hub
docker pull python:3.12-slim
docker pull postgres:16-alpine

# Run a container
docker run python:3.12-slim python --version

# Run interactively (-it = interactive TTY)
docker run -it python:3.12-slim bash

# Run in background (-d = detached) with a name
docker run -d --name my-postgres \
    -e POSTGRES_PASSWORD=secret \
    -p 5432:5432 \
    postgres:16-alpine

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop and remove a container
docker stop my-postgres
docker rm my-postgres

# View container logs
docker logs my-postgres
docker logs -f my-postgres   # follow

# Execute a command inside a running container
docker exec -it my-postgres psql -U postgres

# Remove unused images
docker image prune
```

---

## Chapter 5: Writing a Dockerfile

```dockerfile
# Dockerfile for project-alpha (Python app)
# Best practice: pin the exact version

FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency file first (layer caching optimization)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY .env.example .env

# Run as non-root user (security best practice)
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Define the command to run
CMD ["python3", "src/hello_world.py"]
```

```bash
# Build the image
docker build -t project-alpha:latest .

# Run it
docker run --rm project-alpha:latest

# Build with a specific tag
docker build -t project-alpha:1.0.0 .
```

---

## Chapter 6: docker compose — Multi-Container Applications

`docker compose` manages multiple containers as a single application:

```yaml
# docker-compose.yml — B-012 Build Artifact
version: "3.9"

services:
  app:
    build: .
    container_name: project-alpha-app
    env_file: .env
    environment:
      - DATABASE_URL=postgresql://postgres:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./src:/app/src
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    container_name: project-alpha-db
    env_file: .env
    environment:
      - POSTGRES_DB=${POSTGRES_DB:-devdb}
      - POSTGRES_USER=${POSTGRES_USER:-postgres}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

volumes:
  postgres_data:
```

```bash
# Start all services
docker compose up -d

# View logs for all services
docker compose logs -f

# View logs for one service
docker compose logs -f db

# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v

# Rebuild after code changes
docker compose up -d --build
```

---

## Chapter 7: The Build

```bash
# Step 1: Add Docker-related env vars to .env
cd ~/developer-workspace/project-alpha
cat >> .env << 'EOF'
POSTGRES_DB=devdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=localdev-not-for-production
EOF

# Add to .env.example
cat >> .env.example << 'EOF'
POSTGRES_DB=yourdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=replace-with-strong-password
EOF

# Step 2: Create the Dockerfile (from Chapter 5)
# Step 3: Create docker-compose.yml (from Chapter 6)

# Step 4: Start the stack
docker compose up -d

# Step 5: Verify PostgreSQL is running
docker ps
docker compose logs db

# Step 6: Connect to PostgreSQL
docker exec -it project-alpha-db psql -U postgres devdb
# \l    -- list databases
# \q    -- quit

# Step 7: Stop the stack
docker compose down
```

---

## Chapter 8: Proof of Work

```bash
cd ~/developer-workspace/project-alpha

echo "=== B-012 Build Verification ==="
echo "Docker version:"
docker --version

echo ""
echo "Starting stack:"
docker compose up -d

echo ""
echo "Running containers:"
docker ps

echo ""
echo "PostgreSQL health:"
docker compose logs db | tail -5

echo ""
echo "Stopping stack:"
docker compose down
```

---

## Further Reading

- 📄 [`docs/B-011-environment-variables-and-secrets.md`](B-011-environment-variables-and-secrets.md) — .env pattern used throughout Docker
- 📄 [`docs/autonomous-continuous-development.md`](autonomous-continuous-development.md) — ACD deploys via Docker
- 📄 [`docs/P011-STACK-001-repo-stack-profile.md`](P011-STACK-001-repo-stack-profile.md) — Docker is in the ACSS stack
- 🏠 [`README.md`](../README.md) — Encyclopedia home

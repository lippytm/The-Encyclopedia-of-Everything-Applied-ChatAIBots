# B-042: Your First REST API

### FastAPI, GET/POST, Pydantic Models, and the Art of Building APIs

> *"Every great application eventually becomes an API. When your logic is accessible via HTTP, anything can consume it — mobile apps, other services, AI agents, dashboards. FastAPI makes building production-quality APIs in Python as fast as writing a function. It auto-documents itself. It validates everything. It's honest by design."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Create a FastAPI application with GET, POST, PUT, and DELETE routes
2. Define request/response models using Pydantic
3. Use path parameters, query parameters, and request bodies
4. Return structured JSON responses with correct HTTP status codes
5. Build a `todo_api.py` — a fully functional REST API with auto-generated docs

**Prerequisite:** B-033 (OOP/classes), B-036 (type hints — essential for FastAPI)

**Build Artifact:** `~/developer-workspace/projects/python-foundations/todo_api.py`

**Credential:** `CCSLL-L1-B042-APIBuilder` — on-chain on Base

---

## Chapter 1: FastAPI Concepts

FastAPI is built on three ideas:
1. **Type hints drive everything** — parameters, bodies, responses are all declared with Python types
2. **Pydantic validates automatically** — invalid input gets a 422 response with a clear error
3. **Docs are automatic** — visit `/docs` for a fully interactive Swagger UI

```python
from fastapi import FastAPI

app = FastAPI(title="My First API", version="1.0.0")

@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello from lippytmai API"}

# Run: uvicorn todo_api:app --reload
# Docs: http://localhost:8000/docs
```

---

## Chapter 2: Path and Query Parameters

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Path parameter — part of the URL
@app.get("/users/{user_id}")
def get_user(user_id: int) -> dict[str, int]:
    # FastAPI validates that user_id is an int automatically
    return {"user_id": user_id}

# Query parameters — after ?
@app.get("/items/")
def list_items(
    skip: int = 0,
    limit: int = 10,
    search: str | None = None,
) -> dict[str, object]:
    return {"skip": skip, "limit": limit, "search": search}
# GET /items/?skip=5&limit=20&search=laptop

# Multiple path params
@app.get("/orgs/{org}/repos/{repo}")
def get_repo(org: str, repo: str) -> dict[str, str]:
    return {"org": org, "repo": repo}
```

---

## Chapter 3: Pydantic Models

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from typing import Optional

app = FastAPI()

# Request model — validates incoming JSON
class CreateTodoRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: str = Field("medium", pattern="^(low|medium|high)$")

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        if v.strip() == "":
            raise ValueError("title cannot be blank")
        return v.strip()

# Response model — shapes the output
class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: str
    done: bool

@app.post("/todos/", response_model=TodoResponse, status_code=201)
def create_todo(body: CreateTodoRequest) -> TodoResponse:
    # FastAPI deserializes, validates, and injects 'body' automatically
    return TodoResponse(
        id=1,
        title=body.title,
        description=body.description,
        priority=body.priority,
        done=False,
    )
```

---

## Chapter 4: HTTP Status Codes

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()
db: dict[int, dict] = {}
next_id = 1

class Item(BaseModel):
    name: str
    price: float

# 200 OK (default for GET)
@app.get("/items/{item_id}")
def get_item(item_id: int) -> dict:
    if item_id not in db:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return db[item_id]

# 201 Created (for POST that creates a resource)
@app.post("/items/", status_code=status.HTTP_201_CREATED)
def create_item(item: Item) -> dict:
    global next_id
    db[next_id] = {"id": next_id, **item.model_dump()}
    result = db[next_id]
    next_id += 1
    return result

# 204 No Content (for DELETE)
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> None:
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Not found")
    del db[item_id]

# 422 Unprocessable Entity — returned automatically by FastAPI for validation errors
```

---

## Chapter 5: Dependency Injection

```python
from fastapi import FastAPI, Depends, HTTPException, Header
from typing import Annotated

app = FastAPI()

# Simple dependency — verify an API key
def verify_api_key(x_api_key: Annotated[str, Header()]) -> str:
    if x_api_key != "secret-dev-key":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

# Inject the dependency into a route
@app.get("/secure/data")
def get_secure_data(api_key: Annotated[str, Depends(verify_api_key)]) -> dict:
    return {"data": "This is protected", "key_used": api_key[:4] + "****"}

# Reusable pagination dependency
def pagination(skip: int = 0, limit: int = 10) -> dict[str, int]:
    return {"skip": skip, "limit": min(limit, 100)}

@app.get("/articles/")
def list_articles(page: Annotated[dict, Depends(pagination)]) -> dict:
    return {"articles": [], **page}
```

---

## Chapter 6: The Build — Todo List API

```python
#!/usr/bin/env python3
"""
todo_api.py — B-042 Build Artifact

A fully functional Todo REST API with in-memory storage.
Includes auto-generated Swagger docs at /docs.

Run:
    pip install fastapi uvicorn
    uvicorn todo_api:app --reload
    # Then open http://localhost:8000/docs
"""
from __future__ import annotations

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

app = FastAPI(
    title="lippytmai Todo API",
    description="B-042 build artifact — CCSLL Python Foundations",
    version="1.0.0",
)

# ---------- Models ----------

class CreateTodoRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, examples=["Learn FastAPI"])
    description: Optional[str] = Field(None, max_length=1000)
    priority: str = Field("medium", pattern="^(low|medium|high)$")
    due_date: Optional[str] = Field(None, examples=["2026-09-01"])

class UpdateTodoRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    done: Optional[bool] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: str
    done: bool
    due_date: Optional[str]
    created: str

# ---------- In-memory store ----------

_todos: dict[int, TodoResponse] = {}
_next_id: int = 1

# ---------- Routes ----------

@app.get("/", tags=["health"])
def root() -> dict[str, str]:
    return {"status": "ok", "api": "lippytmai Todo API", "docs": "/docs"}

@app.get("/todos/", response_model=list[TodoResponse], tags=["todos"])
def list_todos(
    done: Optional[bool] = None,
    priority: Optional[str] = None,
) -> list[TodoResponse]:
    """List all todos, optionally filtered by done status or priority."""
    items = list(_todos.values())
    if done is not None:
        items = [t for t in items if t.done == done]
    if priority is not None:
        items = [t for t in items if t.priority == priority]
    return items

@app.get("/todos/{todo_id}", response_model=TodoResponse, tags=["todos"])
def get_todo(todo_id: int) -> TodoResponse:
    """Get a single todo by ID."""
    if todo_id not in _todos:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
    return _todos[todo_id]

@app.post("/todos/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED, tags=["todos"])
def create_todo(body: CreateTodoRequest) -> TodoResponse:
    """Create a new todo."""
    global _next_id
    todo = TodoResponse(
        id=_next_id,
        title=body.title,
        description=body.description,
        priority=body.priority,
        done=False,
        due_date=body.due_date,
        created=date.today().isoformat(),
    )
    _todos[_next_id] = todo
    _next_id += 1
    return todo

@app.patch("/todos/{todo_id}", response_model=TodoResponse, tags=["todos"])
def update_todo(todo_id: int, body: UpdateTodoRequest) -> TodoResponse:
    """Partially update a todo (title, description, priority, or done status)."""
    if todo_id not in _todos:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
    existing = _todos[todo_id]
    updated_data = existing.model_dump()
    for field, value in body.model_dump(exclude_unset=True).items():
        updated_data[field] = value
    _todos[todo_id] = TodoResponse(**updated_data)
    return _todos[todo_id]

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["todos"])
def delete_todo(todo_id: int) -> None:
    """Delete a todo permanently."""
    if todo_id not in _todos:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
    del _todos[todo_id]

@app.get("/todos/stats/summary", tags=["todos"])
def stats() -> dict[str, object]:
    """Return summary statistics."""
    items = list(_todos.values())
    return {
        "total": len(items),
        "done": sum(1 for t in items if t.done),
        "pending": sum(1 for t in items if not t.done),
        "by_priority": {
            p: sum(1 for t in items if t.priority == p)
            for p in ("high", "medium", "low")
        },
    }
```

```bash
pip install fastapi uvicorn
uvicorn todo_api:app --reload --app-dir ~/developer-workspace/projects/python-foundations
# Open http://localhost:8000/docs
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-042 Verification ==="
python3 -c "
from pydantic import BaseModel, Field
from typing import Optional

class Todo(BaseModel):
    title: str = Field(..., min_length=1)
    priority: str = Field('medium', pattern='^(low|medium|high)$')
    done: bool = False

t = Todo(title='Test', priority='high')
print(f'Title: {t.title}, Priority: {t.priority}, Done: {t.done}')
try:
    bad = Todo(title='', priority='unknown')
except Exception as e:
    print(f'Validation caught: {type(e).__name__}')
print('✅ Pydantic works')
"
```

---

## Further Reading

- 📄 [`docs/B-036-type-hints-making-python-honest.md`](B-036-type-hints-making-python-honest.md) — Type hints power FastAPI
- 📄 [`docs/B-043-the-async-python-primer.md`](B-043-the-async-python-primer.md) — Async FastAPI routes
- 📄 [`docs/ai-trading-bots-intelligence.md`](ai-trading-bots-intelligence.md) — Real-world API use case
- 🏠 [`README.md`](../README.md) — Encyclopedia home

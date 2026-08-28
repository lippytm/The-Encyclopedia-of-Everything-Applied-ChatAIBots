# B-051: Git with Python

> *"Git is the time machine. Python is the pilot. Together, they automate the history of everything you build."*

---

## Learning Objectives

By the end of this book you will:

1. Use `GitPython` to open, inspect, and commit to repositories programmatically
2. Query the GitHub API using `PyGitHub` to read issues, PRs, and commits
3. Build a commit reporter that runs on a schedule
4. Understand when Python automation beats raw shell git commands
5. Earn the `CCSLL-L1-B051-GitEngineer` credential

---

## Chapter 1: Why Git + Python?

Shell scripting drives Git automation — until your logic grows beyond 10 lines. Python handles:

- Complex branching logic across multiple repos
- JSON/YAML parsing of CI configs
- GitHub API pagination without counting `curl` headers
- Cross-platform portability (Windows, macOS, Linux equally)

```python
from __future__ import annotations
import subprocess
from pathlib import Path

def git_status(repo_path: Path) -> str:
    """Return git status output for a given repository."""
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout
```

---

## Chapter 2: GitPython Fundamentals

```bash
pip install gitpython
```

```python
from __future__ import annotations
from pathlib import Path
from git import Repo, InvalidGitRepositoryError

def open_repo(path: Path) -> Repo:
    """Open an existing git repository."""
    try:
        return Repo(path, search_parent_directories=True)
    except InvalidGitRepositoryError as exc:
        raise ValueError(f"No git repo found at {path}") from exc

def list_recent_commits(repo: Repo, count: int = 10) -> list[dict[str, str]]:
    """Return the most recent commits as a list of dicts."""
    commits = []
    for commit in repo.iter_commits(max_count=count):
        commits.append({
            "sha": commit.hexsha[:8],
            "author": str(commit.author),
            "message": commit.message.strip().split("\n")[0],
            "date": commit.committed_datetime.isoformat(),
        })
    return commits
```

---

## Chapter 3: Reading Repository State

```python
from __future__ import annotations
from git import Repo
from pathlib import Path

def repo_summary(path: Path) -> dict[str, object]:
    """Summarize the state of a repository."""
    repo = Repo(path, search_parent_directories=True)
    return {
        "active_branch": repo.active_branch.name,
        "is_dirty": repo.is_dirty(),
        "untracked_files": repo.untracked_files,
        "staged_files": [item.a_path for item in repo.index.diff("HEAD")],
        "unstaged_files": [item.a_path for item in repo.index.diff(None)],
        "last_commit": repo.head.commit.hexsha[:8],
    }
```

---

## Chapter 4: Making Commits with GitPython

```python
from __future__ import annotations
from pathlib import Path
from git import Repo, Actor

def commit_file(
    repo_path: Path,
    file_path: Path,
    message: str,
    author_name: str = "lippytmai",
    author_email: str = "ai@lippytm.ai",
) -> str:
    """Stage a file and create a commit. Returns the new commit SHA."""
    repo = Repo(repo_path)
    repo.index.add([str(file_path.relative_to(repo_path))])
    author = Actor(author_name, author_email)
    commit = repo.index.commit(message, author=author, committer=author)
    return commit.hexsha[:8]
```

---

## Chapter 5: The GitHub API with PyGitHub

```bash
pip install PyGithub
```

```python
from __future__ import annotations
import os
from github import Github, Repository

def get_repo(repo_name: str) -> Repository.Repository:
    """Connect to GitHub API and return a repository object."""
    token = os.environ.get("GITHUB_TOKEN")
    gh = Github(token)
    return gh.get_repo(repo_name)

def list_open_prs(repo_name: str) -> list[dict[str, object]]:
    """Return all open pull requests for a repository."""
    repo = get_repo(repo_name)
    return [
        {
            "number": pr.number,
            "title": pr.title,
            "author": pr.user.login,
            "created_at": pr.created_at.isoformat(),
            "labels": [label.name for label in pr.labels],
        }
        for pr in repo.get_pulls(state="open")
    ]
```

---

## Chapter 6: Building a Commit Reporter

```python
from __future__ import annotations
import json
import os
from datetime import datetime, timedelta, timezone
from github import Github

def daily_commit_report(repo_name: str, days: int = 1) -> dict[str, object]:
    """Generate a commit report for the last N days."""
    gh = Github(os.environ.get("GITHUB_TOKEN"))
    repo = gh.get_repo(repo_name)
    since = datetime.now(tz=timezone.utc) - timedelta(days=days)

    commits_data: list[dict[str, str]] = []
    for commit in repo.get_commits(since=since):
        commits_data.append({
            "sha": commit.sha[:8],
            "author": commit.commit.author.name,
            "message": commit.commit.message.strip().split("\n")[0],
            "date": commit.commit.author.date.isoformat(),
        })

    return {
        "repo": repo_name,
        "period_days": days,
        "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        "commit_count": len(commits_data),
        "commits": commits_data,
    }

if __name__ == "__main__":
    report = daily_commit_report("lippytm/The-Encyclopedia-of-Everything-Applied-ChatAIBots")
    print(json.dumps(report, indent=2))
```

---

## Chapter 7: Proof of Work — Automated Commit Reporter

Build `commit_reporter.py`:

```python
from __future__ import annotations
import argparse
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from git import Repo
from github import Github

def local_report(repo_path: Path, count: int = 10) -> dict[str, object]:
    """Generate a report from a local repository."""
    repo = Repo(repo_path, search_parent_directories=True)
    commits = []
    for commit in repo.iter_commits(max_count=count):
        commits.append({
            "sha": commit.hexsha[:8],
            "author": str(commit.author),
            "message": commit.message.strip().split("\n")[0],
            "date": commit.committed_datetime.isoformat(),
        })
    return {
        "source": "local",
        "path": str(repo_path),
        "branch": repo.active_branch.name,
        "commits": commits,
    }

def remote_report(repo_name: str, days: int = 7) -> dict[str, object]:
    """Generate a report from the GitHub API."""
    token = os.environ.get("GITHUB_TOKEN", "")
    gh = Github(token or None)
    repo = gh.get_repo(repo_name)
    since = datetime.now(tz=timezone.utc) - timedelta(days=days)
    commits = []
    for c in repo.get_commits(since=since):
        commits.append({
            "sha": c.sha[:8],
            "author": c.commit.author.name,
            "message": c.commit.message.strip().split("\n")[0],
        })
    return {
        "source": "github",
        "repo": repo_name,
        "days": days,
        "commit_count": len(commits),
        "commits": commits,
    }

def main() -> None:
    parser = argparse.ArgumentParser(description="Git commit reporter")
    sub = parser.add_subparsers(dest="command", required=True)

    local_cmd = sub.add_parser("local", help="Report from local repo")
    local_cmd.add_argument("path", type=Path, nargs="?", default=Path("."))
    local_cmd.add_argument("--count", type=int, default=10)

    remote_cmd = sub.add_parser("remote", help="Report from GitHub API")
    remote_cmd.add_argument("repo", help="owner/repo")
    remote_cmd.add_argument("--days", type=int, default=7)

    args = parser.parse_args()
    if args.command == "local":
        report = local_report(args.path, args.count)
    else:
        report = remote_report(args.repo, args.days)
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
```

```bash
pip install gitpython PyGithub
python3 commit_reporter.py local .
python3 commit_reporter.py remote lippytm/The-Encyclopedia-of-Everything-Applied-ChatAIBots --days 3
```

**Credential earned:** `CCSLL-L1-B051-GitEngineer`

---

## Further Reading

- 📄 [`docs/B-008-files-that-never-get-lost.md`](B-008-files-that-never-get-lost.md) — Git foundations (Phase 1)
- 📄 [`docs/B-052-your-first-docker-container.md`](B-052-your-first-docker-container.md) — Next: containerize it
- 📄 [`docs/ai-clone-engine-swarms.md`](ai-clone-engine-swarms.md) — ACSS architecture
- 🏠 [`README.md`](../README.md) — Encyclopedia home

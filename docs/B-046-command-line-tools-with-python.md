# B-046: Command-Line Tools with Python

### argparse, click, typer, and the Art of Building CLI Programs

> *"The terminal is the developer's home. A well-designed CLI tool is a gift to every person who uses it — including your future self running it at 2 AM. Python's ecosystem gives you three tiers of CLI power: argparse for stdlib purity, click for composability, typer for type-hint magic. Learn all three. Choose the right one."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Build CLI tools with `argparse` — Python's built-in argument parser
2. Use `click` for composable command groups and decorators
3. Use `typer` to build CLIs from type-annotated functions with zero boilerplate
4. Add subcommands, options, flags, and file arguments
5. Build a `file_processor.py` CLI tool with full argument handling

**Prerequisite:** B-040 (pathlib/subprocess), B-036 (type hints)

**Build Artifact:** `~/developer-workspace/projects/python-foundations/file_processor.py`

**Credential:** `CCSLL-L1-B046-CLIEngineer` — on-chain on Base

---

## Chapter 1: argparse — The Standard Library CLI

```python
import argparse

# Basic parser
parser = argparse.ArgumentParser(
    prog="myapp",
    description="A sample CLI tool",
    epilog="Built with lippytmai",
)

# Positional argument (required)
parser.add_argument("filename", help="File to process")

# Optional argument with flag
parser.add_argument("--output", "-o", help="Output file path", default="output.txt")

# Boolean flag
parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

# Integer with type coercion
parser.add_argument("--lines", "-n", type=int, default=10, help="Number of lines")

# Choices
parser.add_argument("--format", choices=["json", "csv", "text"], default="text")

# Parse
args = parser.parse_args()
print(args.filename)    # positional
print(args.output)      # --output or -o
print(args.verbose)     # True/False
print(args.lines)       # int
print(args.format)      # one of json/csv/text

# Auto-generates --help:
# $ python3 myapp.py --help
```

---

## Chapter 2: Subcommands with argparse

```python
import argparse

parser = argparse.ArgumentParser(prog="toolkit")
subparsers = parser.add_subparsers(dest="command", required=True)

# Subcommand: count
count_parser = subparsers.add_parser("count", help="Count lines/words/chars in a file")
count_parser.add_argument("file")
count_parser.add_argument("--words", action="store_true")
count_parser.add_argument("--chars", action="store_true")

# Subcommand: convert
convert_parser = subparsers.add_parser("convert", help="Convert file format")
convert_parser.add_argument("file")
convert_parser.add_argument("--to", choices=["csv", "json", "yaml"], required=True)

args = parser.parse_args()

if args.command == "count":
    print(f"Counting in {args.file}")
elif args.command == "convert":
    print(f"Converting {args.file} to {args.to}")

# $ python3 toolkit.py count myfile.txt --words
# $ python3 toolkit.py convert data.csv --to json
```

---

## Chapter 3: click — Composable CLI Decorators

```python
import click

@click.group()
def cli() -> None:
    """lippytmai file toolkit."""
    pass

@cli.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--lines", "-n", default=10, help="Number of lines to show")
@click.option("--verbose", "-v", is_flag=True, help="Show extra info")
def head(filename: str, lines: int, verbose: bool) -> None:
    """Show the first N lines of a file."""
    if verbose:
        click.echo(f"Reading: {filename}")
    with open(filename) as f:
        for i, line in enumerate(f):
            if i >= lines:
                break
            click.echo(line, nl=False)

@cli.command()
@click.argument("source", type=click.Path(exists=True))
@click.argument("destination")
@click.option("--force", is_flag=True, help="Overwrite if exists")
def copy(source: str, destination: str, force: bool) -> None:
    """Copy a file."""
    import shutil
    from pathlib import Path
    dest = Path(destination)
    if dest.exists() and not force:
        raise click.ClickException(f"{destination} already exists. Use --force to overwrite.")
    shutil.copy2(source, destination)
    click.echo(f"✅ Copied {source} → {destination}")

if __name__ == "__main__":
    cli()
```

---

## Chapter 4: typer — Type-Hint CLIs

```python
#!/usr/bin/env python3
"""typer builds CLIs from type hints — no decorators needed for simple commands."""
import typer
from pathlib import Path
from typing import Optional
from enum import Enum

app = typer.Typer(help="lippytmai file utilities")

class Format(str, Enum):
    json = "json"
    csv  = "csv"
    text = "text"

@app.command()
def count(
    filename: Path = typer.Argument(..., help="File to count"),
    words: bool = typer.Option(False, "--words", "-w", help="Count words"),
    chars: bool = typer.Option(False, "--chars", "-c", help="Count chars"),
) -> None:
    """Count lines, words, or characters in a file."""
    text = filename.read_text()
    lines = len(text.splitlines())
    typer.echo(f"Lines: {lines}")
    if words:
        typer.echo(f"Words: {len(text.split())}")
    if chars:
        typer.echo(f"Chars: {len(text)}")

@app.command()
def search(
    pattern: str = typer.Argument(..., help="Search pattern"),
    path: Path = typer.Argument(Path("."), help="Directory to search"),
    ext: Optional[str] = typer.Option(None, "--ext", help="File extension filter (e.g. .py)"),
) -> None:
    """Search for a pattern in files."""
    import re
    glob = f"**/*{ext}" if ext else "**/*"
    for file in path.rglob(glob if ext else "*"):
        if file.is_file():
            try:
                for i, line in enumerate(file.read_text().splitlines(), 1):
                    if re.search(pattern, line):
                        typer.echo(f"{file}:{i}: {line.strip()}")
            except Exception:
                pass

if __name__ == "__main__":
    app()
```

---

## Chapter 5: Rich Output

```python
# Make CLI output beautiful with color, tables, and progress bars
import typer
from pathlib import Path

app = typer.Typer()

@app.command()
def stats(directory: Path = typer.Argument(Path("."))) -> None:
    """Show directory file stats with colors."""
    files = sorted(directory.rglob("*"))
    for f in files:
        if f.is_file():
            size = f.stat().st_size
            # typer.echo with ANSI or use 'rich' library for full formatting
            color = "green" if size < 1024 else "yellow" if size < 1024*100 else "red"
            typer.echo(
                f"{typer.style(f.name, fg=color)}  "
                f"{typer.style(str(size), bold=True)} bytes"
            )

# exit codes — important for scripting
@app.command()
def validate(filename: Path) -> None:
    """Validate a file exists and is non-empty."""
    if not filename.exists():
        typer.echo(f"❌ Not found: {filename}", err=True)
        raise typer.Exit(code=1)
    if filename.stat().st_size == 0:
        typer.echo(f"⚠️  Empty file: {filename}", err=True)
        raise typer.Exit(code=2)
    typer.echo(f"✅ Valid: {filename}")
```

---

## Chapter 6: The Build — file_processor.py

```python
#!/usr/bin/env python3
"""
file_processor.py — B-046 Build Artifact

A feature-rich CLI file processing tool.
Commands: count, search, convert, stats

Usage:
    pip install typer rich
    python3 file_processor.py --help
    python3 file_processor.py count README.md --words --chars
    python3 file_processor.py search "def " . --ext .py
    python3 file_processor.py stats .
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Optional

import typer

app = typer.Typer(
    name="file-processor",
    help="lippytmai file processing toolkit (B-046 build artifact)",
    add_completion=False,
)


@app.command()
def count(
    filename: Path = typer.Argument(..., help="File to analyze", exists=True),
    words: bool = typer.Option(False, "--words", "-w"),
    chars: bool = typer.Option(False, "--chars", "-c"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    """Count lines, words, and characters in a file."""
    text = filename.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    typer.echo(f"File:  {filename}")
    typer.echo(f"Lines: {typer.style(str(len(lines)), bold=True)}")
    if words:
        typer.echo(f"Words: {typer.style(str(len(text.split())), bold=True)}")
    if chars:
        typer.echo(f"Chars: {typer.style(str(len(text)), bold=True)}")
    if verbose:
        typer.echo(f"Size:  {filename.stat().st_size:,} bytes")


@app.command()
def search(
    pattern: str = typer.Argument(..., help="Regex pattern to search for"),
    path: Path = typer.Argument(Path("."), help="Directory or file to search"),
    ext: Optional[str] = typer.Option(None, "--ext", "-e", help="Extension filter e.g. .py"),
    ignore_case: bool = typer.Option(False, "--ignore-case", "-i"),
    max_results: int = typer.Option(50, "--max", "-n"),
) -> None:
    """Search for a regex pattern in files."""
    flags = re.IGNORECASE if ignore_case else 0
    regex = re.compile(pattern, flags)
    found = 0
    files = [path] if path.is_file() else path.rglob(f"*{ext}" if ext else "*")
    for file in files:
        if not file.is_file():
            continue
        try:
            for i, line in enumerate(file.read_text(errors="replace").splitlines(), 1):
                if regex.search(line):
                    typer.echo(f"{typer.style(str(file), fg='cyan')}:{i}: {line.strip()}")
                    found += 1
                    if found >= max_results:
                        typer.echo(f"\n... (max {max_results} results reached)")
                        raise typer.Exit()
        except (PermissionError, IsADirectoryError):
            pass
    typer.echo(f"\n{typer.style(str(found), bold=True)} match(es) found")


@app.command()
def stats(
    directory: Path = typer.Argument(Path("."), help="Directory to analyze"),
    top: int = typer.Option(10, "--top", "-n", help="Show top N largest files"),
) -> None:
    """Show file statistics for a directory."""
    files = [(f, f.stat().st_size) for f in directory.rglob("*") if f.is_file()]
    if not files:
        typer.echo("No files found.")
        return
    files.sort(key=lambda x: x[1], reverse=True)
    total = sum(s for _, s in files)
    typer.echo(f"\n{'File':<50} {'Size':>10}")
    typer.echo("-" * 62)
    for f, size in files[:top]:
        color = "green" if size < 10_000 else "yellow" if size < 100_000 else "red"
        name = str(f.relative_to(directory))[:49]
        typer.echo(f"{name:<50} {typer.style(f'{size:>9,}', fg=color)}")
    typer.echo(f"\n{'Total files:':<20} {len(files)}")
    typer.echo(f"{'Total size:':<20} {total:,} bytes ({total/1024:.1f} KB)")


@app.command()
def convert(
    source: Path = typer.Argument(..., exists=True, help="Source CSV file"),
    output: Optional[Path] = typer.Option(None, "--output", "-o"),
    fmt: str = typer.Option("json", "--format", "-f", help="Output format: json or text"),
) -> None:
    """Convert a CSV file to JSON or text."""
    with source.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    dest = output or source.with_suffix(f".{fmt}")
    if fmt == "json":
        dest.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    else:
        lines = [" | ".join(str(v) for v in row.values()) for row in rows]
        dest.write_text("\n".join(lines), encoding="utf-8")

    typer.echo(f"✅ Converted {source.name} → {dest.name} ({len(rows)} rows)")


if __name__ == "__main__":
    app()
```

```bash
pip install typer
python3 ~/developer-workspace/projects/python-foundations/file_processor.py --help
python3 ~/developer-workspace/projects/python-foundations/file_processor.py count README.md --words --chars
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-046 Verification ==="
python3 -c "
import argparse
p = argparse.ArgumentParser(prog='demo')
p.add_argument('name')
p.add_argument('--upper', action='store_true')
args = p.parse_args(['lippytmai', '--upper'])
result = args.name.upper() if args.upper else args.name
print(f'Result: {result}')
print('✅ argparse works')
"
```

---

## Further Reading

- 📄 [`docs/B-040-automation-scripts-that-save-hours.md`](B-040-automation-scripts-that-save-hours.md) — pathlib + subprocess
- 📄 [`docs/B-044-modules-packages-and-imports.md`](B-044-modules-packages-and-imports.md) — Packaging CLI tools
- 📄 [`docs/B-049-logging-the-programs-memory.md`](B-049-logging-the-programs-memory.md) — Add logging to CLIs
- 🏠 [`README.md`](../README.md) — Encyclopedia home

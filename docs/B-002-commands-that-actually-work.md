# B-002: Commands That Actually Work

### The 20 Bash Commands That Cover 80% of Real Developer Work

> *"You don't need to memorize every command in existence. You need to understand ten deeply, practice twenty until they're reflex, and know how to find the rest."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Use the 20 most important Bash commands without looking them up
2. Copy, move, rename, and delete files and directories safely
3. Search for files and text inside files from the command line
4. Pipe commands together to build mini-pipelines
5. Organize a real project directory structure using only the terminal

**Prerequisite:** B-001 (you can open a terminal and navigate it)

**Build Artifact:** A fully organized `developer-workspace/` directory with 3 sub-projects, a `logs/` folder, and a `README.txt` written entirely from the terminal

**Credential:** `CLL-L0-B002-CommandBuilder` — on-chain on Base

---

## Chapter 1: The 20 Commands

Here is your complete reference for this book:

| # | Command | Does What | Example |
|---|---|---|---|
| 1 | `ls` | List directory contents | `ls -la` |
| 2 | `cd` | Change directory | `cd ~/projects` |
| 3 | `pwd` | Print working directory | `pwd` |
| 4 | `mkdir` | Make directory | `mkdir -p src/utils` |
| 5 | `touch` | Create empty file | `touch config.json` |
| 6 | `cp` | Copy file or directory | `cp file.txt backup/` |
| 7 | `mv` | Move or rename | `mv old.txt new.txt` |
| 8 | `rm` | Remove file | `rm -rf dist/` |
| 9 | `cat` | Show file contents | `cat README.txt` |
| 10 | `echo` | Print text / write to file | `echo "text" >> log.txt` |
| 11 | `nano` | Edit a file | `nano config.json` |
| 12 | `grep` | Search text | `grep "error" app.log` |
| 13 | `find` | Find files | `find . -name "*.py"` |
| 14 | `wc` | Word/line/char count | `wc -l app.py` |
| 15 | `sort` | Sort lines | `sort names.txt` |
| 16 | `head` | First N lines | `head -20 app.log` |
| 17 | `tail` | Last N lines | `tail -f app.log` |
| 18 | `pipe \|` | Chain commands | `ls \| grep ".py"` |
| 19 | `history` | Command history | `history \| tail -20` |
| 20 | `man` | Manual / help | `man grep` |

*[Reality — these 20 commands are used daily by professional developers, SREs, and engineers worldwide]*

---

## Chapter 2: Copy, Move, Delete

### cp — Copy

```bash
# Copy a file to a different location
cp hello.txt backup/hello-backup.txt

# Copy a directory and everything inside it (-r = recursive)
cp -r my-first-project/ my-first-project-backup/

# Copy multiple files to a directory
cp *.txt backups/
```

### mv — Move and Rename

`mv` does two jobs: it moves files AND renames them. Same command, different usage.

```bash
# Rename a file (move within the same directory)
mv old-name.txt new-name.txt

# Move a file to a different directory
mv report.txt ~/Documents/reports/

# Move and rename at the same time
mv draft.txt ~/Documents/final-report.txt

# Move a whole directory
mv my-project/ ~/projects/my-project/
```

### rm — Remove (⚠️ Permanent)

```bash
# Delete a single file
rm unwanted.txt

# Delete a directory and everything inside (-r = recursive, -f = force, no prompts)
rm -rf old-project/

# ⚠️ SAFETY RULE: Always double-check with ls before rm -rf
ls old-project/
rm -rf old-project/
```

> ⚠️ *[Reality — `rm -rf` is permanent. There is no Recycle Bin on the terminal. The file is gone. Verify before you run it.]*

### The Safe Delete Pattern

```bash
# Move to a trash folder instead of deleting immediately
mkdir -p ~/.trash
mv risky-file.txt ~/.trash/
# Later, when you're sure:
rm -rf ~/.trash/*
```

---

## Chapter 3: Searching — grep and find

### grep — Search Inside Files

`grep` is one of the most powerful tools in your arsenal. It finds lines in files that match a pattern.

```bash
# Find all lines containing "error" in a log file
grep "error" app.log

# Case-insensitive search (-i)
grep -i "Error" app.log

# Show line numbers (-n)
grep -n "def " main.py

# Search recursively through all files in a directory (-r)
grep -r "import pandas" ./src/

# Invert the match — show lines that do NOT contain the pattern (-v)
grep -v "DEBUG" app.log

# Count matching lines (-c)
grep -c "404" access.log
```

### find — Search for Files

```bash
# Find all Python files in the current directory tree
find . -name "*.py"

# Find all files modified in the last 24 hours
find . -mtime -1

# Find all directories named "node_modules" (to delete them)
find . -type d -name "node_modules"

# Find files larger than 100MB
find / -size +100M 2>/dev/null
```

*[Reality — `find` is extremely powerful; the examples above cover the most common real-world patterns]*

---

## Chapter 4: The Pipe — Your First Pipeline

The `|` (pipe) character is one of the most important concepts in Unix/Linux. It takes the **output** of one command and feeds it as **input** to the next.

```bash
# Without pipe: list all files, then search manually
ls -la
# ... scroll and look for .py files ...

# With pipe: list + filter in one step
ls -la | grep ".py"

# Chain three commands: list → filter → count
ls -la | grep ".py" | wc -l
# Output: 7 (there are 7 Python files)
```

### Real Pipeline Examples

```bash
# Find all error lines in a log, show only the last 10
grep "ERROR" app.log | tail -10

# Find the 5 most recently modified Python files
find . -name "*.py" | xargs ls -lt | head -5

# Count how many times each word appears in a file
cat essay.txt | tr ' ' '\n' | sort | uniq -c | sort -rn | head -20

# Find processes using a lot of CPU (if you have ps installed)
ps aux | sort -k3 -rn | head -10
```

The pipe is the foundation of **composable tools** — the Unix philosophy that small, focused commands combined together can do anything.

---

## Chapter 5: head, tail, wc, sort

These four utility commands work beautifully in pipelines:

```bash
# head — show first N lines (default 10)
head app.log
head -20 app.log

# tail — show last N lines (default 10)
tail app.log
tail -20 app.log

# tail -f — FOLLOW a file in real time (great for watching logs)
tail -f /var/log/syslog
# (Press Ctrl+C to stop)

# wc — word count
wc app.py           # lines, words, characters
wc -l app.py        # lines only
wc -w essay.txt     # words only

# sort — sort lines alphabetically
sort names.txt
sort -r names.txt   # reverse order
sort -n numbers.txt # numeric sort (not lexicographic)
```

---

## Chapter 6: history — Your Command Memory

```bash
# Show your last 20 commands
history | tail -20

# Search your history for a command you ran before
history | grep "docker"

# Re-run the last command
!!

# Re-run command number 142 from your history
!142

# Search history interactively (most useful)
# Press Ctrl+R, then start typing
# Keep pressing Ctrl+R to cycle through matches
# Press Enter to run, Esc to cancel
```

*[Reality — `Ctrl+R` reverse history search is one of the most time-saving terminal shortcuts in existence]*

---

## Chapter 7: man — The Built-In Manual

Every command has a manual page. You never need to Google basic syntax if you know how to use `man`:

```bash
# Open the manual for grep
man grep

# Open the manual for find
man find

# Navigate: arrow keys to scroll, / to search, q to quit

# Quick help (shorter than man pages)
grep --help
find --help
ls --help
```

---

## Chapter 8: The Build — Developer Workspace

Follow these steps exactly. This is your B-002 build artifact.

```bash
# Step 1: Create the root workspace
cd ~
mkdir developer-workspace
cd developer-workspace

# Step 2: Create three sub-project directories
mkdir -p project-alpha/src project-alpha/tests
mkdir -p project-beta/src project-beta/docs
mkdir -p project-gamma/src project-gamma/config

# Step 3: Create placeholder source files
touch project-alpha/src/main.py
touch project-alpha/tests/test_main.py
touch project-beta/src/app.js
touch project-beta/docs/api.md
touch project-gamma/src/server.rs
touch project-gamma/config/settings.toml

# Step 4: Create a logs directory
mkdir logs
echo "$(date): Workspace created" > logs/setup.log

# Step 5: Write your README
cat > README.txt << 'EOF'
Developer Workspace
===================
Created: $(date)
Owner: Your Name Here

Projects:
  - project-alpha: Python learning project
  - project-beta:  JavaScript learning project
  - project-gamma: Rust learning project

Each project has src/ for source code and additional folders for tests, docs, or config.
EOF

# Step 6: Verify your structure
find . -type f
echo ""
echo "File count: $(find . -type f | wc -l)"
echo "Directory count: $(find . -type d | wc -l)"
```

**Expected final structure:**

```
developer-workspace/
├── README.txt
├── logs/
│   └── setup.log
├── project-alpha/
│   ├── src/main.py
│   └── tests/test_main.py
├── project-beta/
│   ├── src/app.js
│   └── docs/api.md
└── project-gamma/
    ├── src/server.rs
    └── config/settings.toml
```

---

## Chapter 9: Proof of Work

```bash
cd ~/developer-workspace

echo "=== B-002 Build Verification ==="
echo "Location: $(pwd)"
echo "Structure:"
find . | sort
echo ""
echo "File count: $(find . -type f | wc -l)"
echo "Log content:"
cat logs/setup.log
echo ""
echo "README:"
cat README.txt
```

All 9 files and 8 directories should be present.

---

## Chapter 10: Mutation

```bash
# MUTATION 1: Practice safe renaming
cp README.txt README-backup.txt
mv README.txt README.md   # rename to markdown
ls

# MUTATION 2: Log every command you run today
# Add this to ~/.bashrc to automatically log commands:
echo 'export PROMPT_COMMAND="history -a; $PROMPT_COMMAND"' >> ~/.bashrc
source ~/.bashrc
# Now every command is saved immediately to ~/.bash_history

# MUTATION 3: Build a search habit
# Find all empty files you just created
find ~/developer-workspace -empty -type f
```

---

## Chapter 11: What Comes Next

| Book | Title | What You'll Build |
|---|---|---|
| **B-003** | *The File That Remembered Everything* | A secure multi-user project directory with permissions |
| **B-004** | *The Script That Did My Job* | A Bash automation script that backs up your projects |
| **B-005** | *Installing Things Without Breaking Things* | A complete Python development environment |

---

## Appendix A: The rm -rf Rule

> *Never run `rm -rf` on a path you typed from memory. Always:*
> 1. `ls <path>` — verify what's there
> 2. `rm -rf <path>` — then delete

This one habit will save your career at least once.

---

## Further Reading

- 📄 [`docs/B-001-the-terminal-and-the-curious-mind.md`](B-001-the-terminal-and-the-curious-mind.md) — The foundation for this book
- 📄 [`docs/linux-blockchain-educational-ecosystem.md`](linux-blockchain-educational-ecosystem.md) — The full Linux curriculum
- 📄 [`docs/P011-EBOOK-000-course-series-master-plan.md`](P011-EBOOK-000-course-series-master-plan.md) — All 300 books in the series
- 🏠 [`README.md`](../README.md) — Encyclopedia home

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

## Chapter 12: Done-For-You Lessons

> *"You don't learn commands by memorizing them. You learn them by using them on real problems that matter to you."*

Each DFY lesson below is delivered in three integrated formats — read the ebook figure, listen to the audiobook callout, then follow the video scene in your terminal.

| Icon | Format | What it is |
|---|---|---|
| 📘 | **Ebook** | Annotated command diagram or reference table |
| 🎧 | **Audiobook** | Narrator script — pause and build |
| 🎬 | **Video** | SHOW→BUILD→VERIFY terminal scene |

---

### DFY Lesson 1 — The 15 Commands You'll Run Every Day

**What you'll have:** A personal cheat-sheet card of the 15 most-used Linux commands, annotated with your own notes.
**Time:** 10 minutes.

---

📘 **Ebook Figure**

```
TIER 1: Navigation & Listing
  ls -lah       → list all files with sizes and hidden items
  cd -          → go back to the last directory you were in
  pwd           → confirm exactly where you are
  tree -L 2     → visual directory map, 2 levels deep

TIER 2: File Operations
  cp -r src dst → copy a directory recursively
  mv old new    → rename OR move (same command)
  rm -i file    → delete with confirmation prompt
  touch file    → create empty file OR update timestamp

TIER 3: Inspection
  cat file      → print small files to screen
  less file     → scroll through large files (q to quit)
  head -n 20    → show first 20 lines
  tail -f log   → live-follow a log file as it grows

TIER 4: Process & System
  ps aux        → all running processes
  kill -9 PID   → force-stop a process
  man command   → full reference for any command
```

*Figure 12.1 — These 15 commands handle 80% of daily Linux work. Learn them cold, annotate them yours.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 1: The 15 Commands You'll Run Every Day.
>
> If you only learned 15 Linux commands, these are the ones. Navigation, file operations, inspection, process management — they cover 80% of everything you'll ever do at a terminal. Your deliverable is a personal annotated cheat-sheet: print it, put it somewhere visible, and add your own notes to each line.
>
> Time to build: 10 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** Split screen — command typed on left, result on right for all 15.
- **BUILD:** Learner opens their own terminal and runs each command, filling in the cheat-sheet as they go.
- **VERIFY:** Learner runs `man ls | head -20` to confirm the reference tool works for any command on the list.

---

### DFY Lesson 2 — The rm Safety Wrapper

**What you'll have:** `safe-rm` alias that moves files to a trash folder instead of deleting them permanently.
**Time:** 15 minutes.

---

📘 **Ebook Figure**

```bash
# ~/.bashrc — safe-rm: delete with a safety net
TRASH="$HOME/.trash"
mkdir -p "$TRASH"

safe-rm() {
  mv "$@" "$TRASH/"
  echo "→ Moved to $TRASH. Run 'ls ~/.trash' to inspect."
  echo "  Run 'rm -rf ~/.trash/*' to permanently delete."
}
alias rm='safe-rm'   # ← replaces rm for interactive shells
```

```
Workflow:
  $ rm important-config.yaml
  → Moved to /home/lippytm/.trash/
  $ ls ~/.trash/          # it's still there
  $ rm -rf ~/.trash/*     # deliberate permanent delete
```

*Figure 12.2 — `rm` with no undo is a power tool with no safety guard. This adds the guard.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 2: The rm Safety Wrapper.
>
> Every experienced Linux user has a 'rm -rf story'. It's almost a rite of passage — except it doesn't have to be. This 8-line bash function replaces `rm` with a wrapper that moves files to a trash folder instead. You still get a deliberate permanent delete command. You just never lose something important by accident again.
>
> Your deliverable is: `safe-rm` in `~/.bashrc` — `rm` with a recovery net.
>
> Time to build: 15 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `rm myfile.txt` → moved to `~/.trash/`. `ls ~/.trash/` → file is there. Recovery confirmed.
- **BUILD:** Add `safe-rm()` function and alias to `~/.bashrc`. Source. Explain each line.
- **VERIFY:** Delete a test file. Recover it. Then permanently delete with the explicit command.

---

### DFY Lesson 3 — Pipe Chain Cheat Card

**What you'll have:** A reference table of 10 powerful pipe patterns for filtering, searching, and transforming output.
**Time:** 10 minutes.

---

📘 **Ebook Figure**

```
PIPE PATTERN                          WHAT IT DOES
──────────────────────────────────────────────────────────
ls -lah | grep ".md"                  list only .md files
ps aux | grep nginx | grep -v grep    find nginx process
cat log | sort | uniq -c | sort -rn   count unique lines
cat access.log | awk '{print $7}'     extract URL column
find . -name "*.py" | xargs grep "TODO"  find TODOs in code
history | grep git | tail -20         last 20 git commands
du -sh * | sort -rh | head -10        top 10 largest items
cat /etc/passwd | cut -d: -f1 | sort  list all usernames
ss -tlnp | grep 8080                  is port 8080 open?
journalctl -n 100 | grep ERROR        last 100 errors
```

*Figure 12.3 — Pipes are the grammar of command-line composition. These 10 patterns are vocabulary.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 3: Pipe Chain Cheat Card.
>
> A single command does one thing. A pipe chain does ten things in one line — without writing a script. These 10 patterns are the most reusable compositions in everyday Linux work: filtering processes, counting occurrences, extracting columns, finding code patterns. Memorize three of these this week and your command-line productivity doubles.
>
> Your deliverable is: a printed or saved pipe chain reference card — your top 10.
>
> Time to build: 10 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** A large log file. One pipe chain extracts the error count by hour in 10 seconds.
- **BUILD:** Run each of the 10 pipe patterns against real output. Explain what each piece does.
- **VERIFY:** Learner builds one new pipe chain using only tools from the table.

---

### DFY Lesson 4 — Command Timing and Benchmarking

**What you'll have:** A `benchmark` shell function that times any command and logs results.
**Time:** 10 minutes.

---

📘 **Ebook Figure**

```bash
benchmark() {
  local cmd="$*"
  echo "⏱  Running: $cmd"
  local start=$(date +%s%N)
  eval "$cmd"
  local end=$(date +%s%N)
  local ms=$(( (end - start) / 1000000 ))
  echo "✅ Done in ${ms}ms — command: $cmd"
  echo "[$(date +%F\ %T)] ${ms}ms → $cmd" >> ~/logs/benchmarks.log
}
```

```
Usage:
  benchmark ls -R /usr     → ✅ Done in 847ms
  benchmark python3 app.py → ✅ Done in 2341ms
  cat ~/logs/benchmarks.log
```

*Figure 12.4 — You can't optimize what you don't measure. This function makes timing any command effortless.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 4: Command Timing and Benchmarking.
>
> 'That runs fast' is not a measurement. Real performance work starts with a baseline. This function wraps any command in a timer, prints the result, and logs it permanently. After a week of casual use, you'll have real data about which operations in your workflow are slow — and which optimizations actually help.
>
> Your deliverable is: a `benchmark` function in `~/.bashrc` — timing any command with one word.
>
> Time to build: 10 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `benchmark find / -name "*.log"` — result in milliseconds, logged.
- **BUILD:** Add function to `~/.bashrc`, source, explain `$SECONDS` vs nanosecond precision.
- **VERIFY:** Run 3 benchmarks, open `~/logs/benchmarks.log`, see all 3 entries with times.

---

### DFY Lesson 5 — CLI Help Extractor

**What you'll have:** `help-extract.sh` — pulls the first 40 lines of `--help` output for any command into `~/notes/help/`.
**Time:** 10 minutes.

---

📘 **Ebook Figure**

```bash
#!/usr/bin/env bash
# help-extract.sh — save --help output as a note
CMD="$1"
OUTPUT_DIR="$HOME/notes/help"
mkdir -p "$OUTPUT_DIR"
$CMD --help 2>&1 | head -40 > "$OUTPUT_DIR/$CMD.txt"
echo "✅ Saved to $OUTPUT_DIR/$CMD.txt"
```

```
Usage:
  ./help-extract.sh rsync   → ~/notes/help/rsync.txt
  ./help-extract.sh curl    → ~/notes/help/curl.txt
  ./help-extract.sh ffmpeg  → ~/notes/help/ffmpeg.txt
```

*Figure 12.5 — Most developers run `--help` and forget. This script makes help output persistent and searchable.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 5: CLI Help Extractor.
>
> The `--help` flag is available on nearly every command-line tool ever built. But you run it, scan it, and it's gone the moment you close the terminal. This script saves the first 40 lines — the most important part — permanently in your notes folder. After a month of using it, you'll have a personal reference library of every tool you've touched.
>
> Your deliverable is: `help-extract.sh` — persistent `--help` notes for any command.
>
> Time to build: 10 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `cat ~/notes/help/rsync.txt` — rsync options visible without running rsync.
- **BUILD:** Write script. `chmod +x`. Add `~/bin` to PATH. Test.
- **VERIFY:** Extract help for 3 commands. `ls ~/notes/help/` shows all 3 files.

---

### DFY Lesson 6 — Git-Aware Command Prompt Module

**What you'll have:** `__git_ps1` enabled and configured to show branch name AND dirty state in your prompt.
**Time:** 15 minutes.

---

📘 **Ebook Figure**

```bash
# ~/.bashrc — enable git prompt with dirty state indicator
# First: download git-prompt.sh if not already present
source /usr/share/git/completion/git-prompt.sh 2>/dev/null || \
  source /usr/lib/git-core/git-sh-prompt 2>/dev/null

# Configure: show * for unstaged, + for staged
export GIT_PS1_SHOWDIRTYSTATE=1
export GIT_PS1_SHOWUNTRACKEDFILES=1
export GIT_PS1_SHOWUPSTREAM="auto"

# Result in your PS1 — see B-001 DFY-06 for full PS1 setup
#   lippytm@arch:~/projects/enc (main *) $   ← unstaged changes
#   lippytm@arch:~/projects/enc (main +) $   ← staged, not committed
#   lippytm@arch:~/projects/enc (main) $     ← clean
#   lippytm@arch:~/projects/enc (main %) $   ← untracked files
```

*Figure 12.6 — A prompt that shows repo state means you never accidentally commit to main or forget staged files.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 6: Git-Aware Command Prompt Module.
>
> When you're deep in a project, running `git status` before every command is friction. A git-aware prompt removes that friction entirely — branch name, dirty state, staged changes — all visible at every single prompt, automatically, without a keystroke. After this lesson, you'll never accidentally commit to main again.
>
> Your deliverable is: `__git_ps1` fully configured — branch name plus status indicators in your prompt.
>
> Time to build: 15 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** Edit a file in a git repo — prompt immediately shows `(main *)`. Stage it — shows `(main +)`.
- **BUILD:** Source `git-prompt.sh`, set env vars, test each state.
- **VERIFY:** Unstage, stage, commit — prompt accurately reflects each state transition.

---

### DFY Lesson 7 — Command Not Found Handler

**What you'll have:** A custom `command_not_found_handle` that suggests the right package and nearest command.
**Time:** 15 minutes.

---

📘 **Ebook Figure**

```bash
# ~/.bashrc — helpful command_not_found_handle
command_not_found_handle() {
  local cmd="$1"
  echo "❌  Command not found: $cmd"
  echo ""
  # Suggest similar installed commands
  compgen -c | grep -i "$cmd" | head -5 | while read -r match; do
    echo "   Did you mean: $match?"
  done
  # Suggest install if pacman available
  if command -v pacman &>/dev/null; then
    echo ""
    echo "   Try: pacman -Ss $cmd | head -5"
  elif command -v apt &>/dev/null; then
    echo "   Try: apt search $cmd"
  fi
  return 127
}
```

```
Before:
  $ htpo
  bash: htpo: command not found

After:
  $ htpo
  ❌  Command not found: htpo
     Did you mean: htop?
     Try: pacman -Ss htpo | head -5
```

*Figure 12.7 — A good error message tells you what to do next. This turns a dead-end into a starting point.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 7: Command Not Found Handler.
>
> 'Command not found' tells you what went wrong but not what to do about it. This handler adds a second layer — it suggests similar commands that are already installed, and shows you the package manager command to install it if not. For beginners, this turns a confusing error into a guided next step.
>
> Your deliverable is: `command_not_found_handle` in `~/.bashrc` — helpful errors with suggested fixes.
>
> Time to build: 15 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** Type a misspelled command — handler suggests the correct one. Install suggestion shown.
- **BUILD:** Add handler, test with 3 typos. Confirm `return 127` for script compatibility.
- **VERIFY:** Verify that scripts using `command || exit` still work correctly with the handler in place.

---

### DFY Lesson 8 — Quick Note from the Terminal

**What you'll have:** `note` and `notes` functions — instant notes from the command line, stored in `~/notes/quick/`.
**Time:** 10 minutes.

---

📘 **Ebook Figure**

```bash
# ~/.bashrc — terminal note-taking in 2 functions
NOTE_DIR="$HOME/notes/quick"
mkdir -p "$NOTE_DIR"

note() {
  echo "[$(date +%F\ %T)] $*" >> "$NOTE_DIR/$(date +%F).md"
  echo "✅ Saved."
}

notes() {
  local date="${1:-$(date +%F)}"
  if [[ -f "$NOTE_DIR/$date.md" ]]; then
    cat "$NOTE_DIR/$date.md"
  else
    echo "No notes for $date"
  fi
}
```

```
Usage:
  $ note Discovered that tail -f works on /dev/stdin
  ✅ Saved.

  $ note TODO: add error handling to deploy script
  ✅ Saved.

  $ notes                  → today's notes
  $ notes 2026-08-27       → yesterday's notes
```

*Figure 12.8 — The fastest way to not forget something is to write it down before you close the terminal.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 8: Quick Note from the Terminal.
>
> How many times have you discovered something useful in your terminal, closed the window, and forgotten it five minutes later? This two-function note-taking system saves any thought in under one second without leaving your terminal. `note` to save, `notes` to recall. All notes are Markdown, dated, and permanent.
>
> Your deliverable is: `note` and `notes` functions in `~/.bashrc` — terminal thought-capture in 1 second.
>
> Time to build: 10 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `note Learned that column -t aligns output beautifully` → saved. `notes` → appears.
- **BUILD:** Add both functions, create `~/notes/quick/`, source, test.
- **VERIFY:** Save 5 notes. Retrieve today's. Retrieve yesterday's with date argument.

---

### DFY Lesson 9 — One-Line System Health Check

**What you'll have:** A `health` alias that prints CPU load, RAM, disk, and network in one shot.
**Time:** 10 minutes.

---

📘 **Ebook Figure**

```bash
# ~/.bashrc — system health snapshot in one command
alias health='echo "=== SYSTEM HEALTH ===" && \
  echo "CPU:   $(top -bn1 | grep "Cpu(s)" | awk "{print \$2+\$4}"%)" && \
  echo "RAM:   $(free -h | awk "/^Mem:/{print \$3\"/\"\$2}")" && \
  echo "DISK:  $(df -h / | awk "NR==2{print \$3\"/\"\$2\" (\"\$5\" used)\"}")" && \
  echo "LOAD:  $(uptime | awk -F"load average:" "{print \$2}")" && \
  echo "NET:   $(ss -s | grep "TCP:" | head -1)" && \
  echo "====================" '
```

```
$ health
=== SYSTEM HEALTH ===
CPU:   4.2%
RAM:   4.1G/15.6G
DISK:  47G/200G (24% used)
LOAD:   0.42, 0.38, 0.31
NET:   TCP: 24 (estab 8, ...)
====================
```

*Figure 12.9 — One command. Five critical numbers. Always know if your machine is stressed before blaming your code.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 9: One-Line System Health Check.
>
> Before blaming your code, check your machine. CPU spiked? RAM exhausted? Disk full? A five-metric health snapshot answers all three questions in one command. This alias is the first thing you run when something feels slow — and the last thing you check before deploying to production.
>
> Your deliverable is: a `health` alias — CPU, RAM, disk, load, and network in one shot.
>
> Time to build: 10 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `health` runs in under one second. All five metrics visible.
- **BUILD:** Build alias piece by piece. Test each metric command standalone first, then compose.
- **VERIFY:** Run `health` during a file copy operation — CPU and disk numbers change.

---

### DFY Lesson 10 — Command Reference Personal Wiki Page

**What you'll have:** `~/wiki/commands.md` — a personal reference page you own, update, and search forever.
**Time:** 20 minutes.

---

📘 **Ebook Figure**

```markdown
# My Linux Command Reference
> Last updated: 2026-08-28 | lippytm

## Navigation
- `cd -` → jump back to last directory
- `pushd / popd` → directory stack navigation

## File Search
- `find . -name "*.py" -newer setup.py` → files newer than setup.py
- `locate filename` → database search (faster than find)

## Process Management
- `kill -9 PID` → force kill
- `pkill -f "python app"` → kill by name pattern
- `nohup cmd &` → run command that survives terminal close

## Text Processing
- `awk '{print $2}' file` → extract column 2
- `sed 's/old/new/g' file` → replace all occurrences

## My Custom Commands (DFY Lessons)
- `health` → system health snapshot
- `note "message"` → save quick note
- `benchmark cmd` → time any command
- `safe-rm file` → delete with recovery net
```

*Figure 12.10 — The difference between a beginner and an expert isn't memory — it's having a better reference system.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 10: Command Reference Personal Wiki Page.
>
> Your mental model of Linux is built one command at a time. The problem is most people let those commands live only in their head — and forget them under pressure. A personal wiki page for commands is the external brain that catches everything. Every new command you learn this week goes in. Every DFY tool you just built goes in. One month from now, it's the most useful document you own.
>
> Your deliverable is: `~/wiki/commands.md` — your personal, growing, searchable Linux reference.
>
> Time to build: 20 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `grep "docker" ~/wiki/commands.md` — docker commands found instantly without web search.
- **BUILD:** Create `~/wiki/commands.md` with the template. Populate with all 9 DFY tools from this chapter.
- **VERIFY:** Reboot. `grep "health" ~/wiki/commands.md` — the alias definition is there.

---

> 🎓 **All 10 DFY lessons complete.** You now have: a 15-command reference, a safe `rm` wrapper, pipe patterns, a benchmarking function, a help extractor, a git-aware prompt, a smart error handler, terminal notes, a health alias, and a personal wiki. Your terminal is now a professional environment.
>
> **Next:** Claim your `CLL-L0-B002-CommandArchitect` credential, then continue to B-003.

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

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

🤖 **Copilot Assist — DFY Lesson 1**

> **Use this prompt with your book copilot right now:**
>
> *"I've been using these 15 commands for a week. Which 5 should I practice most deliberately to build real command-line fluency? And what's missing from this list for my specific workflow: [describe workflow]?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-002 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


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

🤖 **Copilot Assist — DFY Lesson 2**

> **Use this prompt with your book copilot right now:**
>
> *"My safe-rm is working but sometimes I need the real rm for scripts that expect standard behavior. How do I call the original rm when I need it without removing the alias?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-002 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


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

🤖 **Copilot Assist — DFY Lesson 3**

> **Use this prompt with your book copilot right now:**
>
> *"Build me a pipe chain for my specific problem: I have a JSON access log and I need to count unique user IDs per hour. Here's a sample line: [paste]."*
>
> 💡 *Paste this into any AI assistant loaded with the B-002 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


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

🤖 **Copilot Assist — DFY Lesson 4**

> **Use this prompt with your book copilot right now:**
>
> *"My benchmark function shows 0ms for fast commands. Is that a resolution issue with date +%s%N on my system, and what's the fix?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-002 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


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

🤖 **Copilot Assist — DFY Lesson 5**

> **Use this prompt with your book copilot right now:**
>
> *"help-extract.sh works for most tools but `ffmpeg --help` crashes it because ffmpeg outputs to stderr. How do I capture both stdout and stderr?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-002 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


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

🤖 **Copilot Assist — DFY Lesson 6**

> **Use this prompt with your book copilot right now:**
>
> *"My git prompt shows the branch but not the dirty state symbols even though GIT_PS1_SHOWDIRTYSTATE=1 is set. Is the git-prompt.sh file loaded in the wrong order?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-002 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


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

🤖 **Copilot Assist — DFY Lesson 7**

> **Use this prompt with your book copilot right now:**
>
> *"My command_not_found_handle is installed but when I run `foo` I still get the default bash error. How do I verify the handler is actually being called?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-002 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


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

🤖 **Copilot Assist — DFY Lesson 8**

> **Use this prompt with your book copilot right now:**
>
> *"My note() function works but I want to add tags — so I can do `note +devops discovered that...` and then `notes --tag devops`. How do I extend the function?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-002 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


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

🤖 **Copilot Assist — DFY Lesson 9**

> **Use this prompt with your book copilot right now:**
>
> *"My health alias works but the CPU percentage shows as 0 in a fresh terminal. The value is correct after the first prompt. Why the delay and how do I fix it?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-002 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


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

🤖 **Copilot Assist — DFY Lesson 10**

> **Use this prompt with your book copilot right now:**
>
> *"I have 50 commands in my wiki now. How do I add a fuzzy search function so I can do `wikisearch docker` and get all docker-related entries instantly?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-002 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


---

> 🎓 **All 10 DFY lessons complete.** You now have: a 15-command reference, a safe `rm` wrapper, pipe patterns, a benchmarking function, a help extractor, a git-aware prompt, a smart error handler, terminal notes, a health alias, and a personal wiki. Your terminal is now a professional environment.
>
> **Next:** Claim your `CLL-L0-B002-CommandArchitect` credential, then continue to B-003.

---

## Chapter 13: How It Works — Use Cases & Applications

> *"A command is not just syntax. It's a precise instruction delivered to a system that never misunderstands you — once you speak its language."*

---

### 📘 Ebook Explainer — How Commands Actually Work

**The mechanism — what happens when you press Enter:**

```
You type: grep -r "TODO" ~/projects --include="*.py"

  1. Shell reads and tokenizes: command=grep, flags=[-r], args=["TODO", ~/projects], option=[--include="*.py"]
  2. Shell expands ~/projects → /home/lippytm/projects
  3. Shell finds /usr/bin/grep via $PATH lookup
  4. Shell forks → kernel creates child process (copy of shell memory)
  5. Kernel exec() replaces child memory with grep binary
  6. grep receives arguments: recursive search, "TODO" pattern, directory, file filter
  7. grep opens each .py file, reads line by line (kernel read() syscalls)
  8. Each matching line written to stdout (fd 1)
  9. If piped: stdout of grep → stdin of next command (kernel pipe buffer)
  10. grep exits with code 0 (found) or 1 (not found) or 2 (error)
  11. Shell receives exit code → stored in $?
  12. Next prompt shown
```

**Why the exit code matters:**

```bash
grep -r "TODO" ~/projects --include="*.py"
echo "Exit code: $?"   # 0 = found matches, 1 = no matches, 2 = error

# In scripts:
if grep -q "DEBUG=true" config.env; then
  echo "Debug mode is ON"
fi
# grep -q = quiet mode: exit code only, no output
```

*Figure 13.1 — Every command is a conversation with the kernel. Exit codes are the replies. Ignoring them is like asking a question and walking away before the answer.*

---

### 📘 Ebook Explainer — When Commands Work Best

**Optimal conditions for command-line work:**

| Situation | Best command approach | Why |
|---|---|---|
| **Batch processing 1000 files** | `find . -name "*.log" \| xargs gzip` | Loop in a GUI = impossible; loop in terminal = 1 line |
| **Extracting data from logs** | `grep \| awk \| sort \| uniq -c` | Pipe chain; no data import, no spreadsheet |
| **Verifying a remote server** | `ssh user@host "df -h && ps aux \| head -20"` | One SSH command, no remote GUI needed |
| **Automating a weekly task** | Bash script + cron | Runs without you, every week, reliably |
| **Finding what changed in a repo** | `git log --oneline -20` or `git diff HEAD~1` | Version history in one command |
| **Checking if a port is open** | `ss -tlnp \| grep 8080` | Real-time socket state; no GUI needed |
| **Processing a 2GB CSV** | `awk -F',' '{sum+=$3} END{print sum}' data.csv` | awk processes 2GB without loading it into RAM |

**Commands are NOT the right tool when:**
```
❌  You need to drag-and-drop visual elements
❌  You're reviewing formatted documents with images
❌  You're doing real-time video/audio editing
❌  The other person doesn't have a terminal
```

*Figure 13.2 — Match tool to task. The terminal is a precision instrument, not a hammer for every nail.*

---

### 📘 Ebook Explainer — Where to Use It (Domain Applications)

```
EVERY DOMAIN WHERE COMMANDS ARE USED DAILY:

Web Development
  npm run build            → compile frontend
  curl -X POST /api/users  → test API endpoint
  nginx -t && reload       → validate + apply config

Data Engineering
  csvkit, awk, sed, jq     → transform data at scale
  python3 etl.py           → run ETL pipeline
  psql -c "SELECT COUNT(*)"→ query database from CLI

AI / Machine Learning
  python3 train.py         → run training job
  nvidia-smi               → GPU utilization check
  mlflow ui                → launch experiment tracker

Blockchain / Web3
  cast call <contract>     → read on-chain state
  forge test -vvv          → verbose contract tests
  geth --syncmode snap     → sync Ethereum node

Cybersecurity
  nmap -sV 192.168.1.0/24  → network scan
  tcpdump -i eth0 port 443 → capture HTTPS traffic
  hashcat -m 0 hash.txt    → password analysis

System Administration
  systemctl status nginx   → service health
  journalctl -u nginx -f   → live service logs
  crontab -l               → list scheduled jobs

Robotics / IoT
  roslaunch my_pkg node.launch → start ROS node
  mosquitto_pub -t sensor  → publish MQTT message
  screen /dev/ttyUSB0 9600 → serial console
```

*Figure 13.3 — Nine domains, identical terminal interface. Learn once, apply everywhere.*

---

### 📘 Ebook Explainer — Flexibility Points (How It Adapts to You)

Commands are flexible in ways that GUIs can't match:

**Flexibility Point 1 — Composability**
```bash
# Any command's output becomes any other command's input
cat access.log | grep "404" | awk '{print $7}' | sort | uniq -c | sort -rn | head -10
# → Top 10 most-requested URLs returning 404, from a raw log, in one line
```

**Flexibility Point 2 — Parameterization**
```bash
# The same command pattern works for any value
for env in dev staging prod; do
  curl -sf "https://api.$env.lippytm.ai/health" && echo "$env: OK" || echo "$env: FAIL"
done
```

**Flexibility Point 3 — Automation (time independence)**
```bash
# Run at 3AM every Sunday, whether you're awake or not
0 3 * * 0 /home/lippytm/bin/weekly-backup.sh
```

**Flexibility Point 4 — Remote operation**
```bash
# Full control of a machine 10,000 miles away
ssh lippytm@my-server.lippytm.ai "tail -f /var/log/api.log"
```

**Flexibility Point 5 — Scriptability (convert any workflow to code)**
```bash
# 10 manual steps → 1 script → 1 command → 1 cron entry → zero manual steps
./deploy.sh production v2.3.1
```

*Figure 13.4 — Five flexibility modes. Each one multiplies your productivity by removing a different type of friction.*

---

### 🎧 Audiobook Explainer

> *[EXPLAINER TONE — measured, 3 minutes]*
>
> "Chapter 13. How Commands Work. When They Work. Where to Use Them.
>
> Every command you run passes through the same 12-step process in the kernel. The shell parses your input, finds the binary, forks a child process, executes the program, and hands you the result along with an exit code. That exit code — zero for success, non-zero for failure — is how commands communicate with each other in scripts and pipelines. Most beginners ignore it. Professionals build around it.
>
> Commands work best when the work is repetitive, when scale matters, when precision matters, or when the machine isn't in the room with you. Processing a million log lines. Searching a thousand files. Running on a remote server at 3AM. These are the moments where a single well-constructed command outperforms hours of manual work.
>
> Where do you use this? Everywhere there's software running on Linux. Web servers. Data pipelines. AI training jobs. Blockchain nodes. IoT sensors. CI/CD pipelines. Security audits. Robotics systems. The command interface is the lowest common denominator of all of them — which means learning it once makes you capable across all of them.
>
> The flexibility of commands comes from five properties. Composability — pipe any output to any input. Parameterization — run the same logic against any value. Automation — detach from the clock and run on a schedule. Remote operation — control any machine anywhere. And scriptability — convert any sequence of manual steps into a single reusable command. These five properties are why experienced engineers reach for the terminal first, every time."
>
> *[EXPLAINER TONE OUT]*

---

### 🎬 Video Explainer — Commands in 5 Domains (5 Minutes)

**Minute 1 — Web Developer:**
> `curl -I https://myapp.com` → response headers shown. Status 200, server type, caching headers. "One command tells you more about your deployed application than 5 minutes of clicking through browser dev tools."

**Minute 2 — Data Engineer:**
> `awk -F',' 'NR>1 {sum+=$5; count++} END {print "Avg:", sum/count}' sales.csv` → average computed from a 500MB file instantly. "No spreadsheet, no database, no import. The file is the input."

**Minute 3 — AI Developer:**
> `watch -n 1 nvidia-smi` → GPU memory and utilization refreshing every second during model training. "Real-time hardware monitoring while your model trains — one command."

**Minute 4 — Blockchain Developer:**
> `cast call 0xContract "balanceOf(address)" 0xWallet --rpc-url https://mainnet.rpc` → balance returned in wei, then `cast to-unit` converts to ETH. "Read any smart contract state from any network, no wallet, no browser."

**Minute 5 — Use Case Builder Exercise:**
> Blank terminal. Voice-over: "Pick your domain. What's one task you do repeatedly that takes 10 manual steps? Write it out. By B-004, you'll have a script that does it in one."

---

> 🎯 **Use Cases Summary — B-002**
>
> The command skills from this book apply to:
> - ✅ Processing any size file — log, CSV, JSON, binary
> - ✅ Testing any API endpoint from any machine
> - ✅ Automating any repetitive workflow
> - ✅ Monitoring any running system in real time
> - ✅ Composing multi-step operations into single-line pipelines
> - ✅ Scripting any sequence of manual steps into one command
>
> **Commands are not a Linux skill. They are a software engineering skill.**

---


## Chapter 14: ACSS Explainer Series — Commands That Actually Work

> *"You're not just learning Core CLI Commands. You're building a node in an intelligence network that spans 300 books, 15 platforms, and the entire lippytm.ai ecosystem." — lippytmai*

This chapter contains 10 explainer lessons connecting Commands That Actually Work to the full AI Conglomerate Swarms System (ACSS). Each explainer includes all three formats plus a copilot prompt.

---

### Explainer 1: ACSS Overview
*intelligence network*

**📘 Ebook Explanation:**

Commands That Actually Work teaches the Core CLI Commands layer that runs beneath all 8 ACSS systems. Cli commands are how every acss system is built, deployed, and debugged — fluency with commands is the foundation of all acss operations.

**📘 Connection Map:**

```
B-002 (Core CLI Commands)
    ↕
ACSS Overview Layer
    ↕
ACSS Ecosystem
```

**🎧 30-Second Audiobook Callout (lippytmai voice):**

> *"lippytmai here. Commands That Actually Work connects to ACSS Overview: Commands That Actually Work teaches the Core CLI Commands layer that runs beneath all 8 ACSS systems..."*

**🎬 60-Second Video Walkthrough:**

- **0–10s:** Show ACSS Overview in the ACSS architecture overview
- **10–35s:** Zoom in where B-002 / Core CLI Commands connects to ACSS Overview
- **35–55s:** Live example of the connection in action
- **55–60s:** CTA to complete B-002 and activate the connection

**🤖 Copilot Prompt:**

> *"Explain how Core CLI Commands fits the ACSS architecture. What role does B-002 play in the system?"*

---
### Explainer 2: Hermes Event Routing
*cross-system message bus*

**📘 Ebook Explanation:**

Hermes routes Core CLI Commands practice events between ACSS components. Every terminal session generates Hermes events.

**📘 Connection Map:**

```
B-002 (Core CLI Commands)
    ↕
Hermes Event Routing Layer
    ↕
ACSS Ecosystem
```

**🎧 30-Second Audiobook Callout (lippytmai voice):**

> *"lippytmai here. Commands That Actually Work connects to Hermes Event Routing: Hermes routes Core CLI Commands practice events between ACSS components. Every terminal session gene..."*

**🎬 60-Second Video Walkthrough:**

- **0–10s:** Show Hermes Event Routing in the ACSS architecture overview
- **10–35s:** Zoom in where B-002 / Core CLI Commands connects to Hermes Event Routing
- **35–55s:** Live example of the connection in action
- **55–60s:** CTA to complete B-002 and activate the connection

**🤖 Copilot Prompt:**

> *"Show the Hermes event schema for a B-002 skill-complete event."*

---
### Explainer 3: Fabric Knowledge Graph
*pattern synthesis*

**📘 Ebook Explanation:**

Fabric stores Core CLI Commands concepts as knowledge nodes. Every command you master becomes a connected node in the graph.

**📘 Connection Map:**

```
B-002 (Core CLI Commands)
    ↕
Fabric Knowledge Graph Layer
    ↕
ACSS Ecosystem
```

**🎧 30-Second Audiobook Callout (lippytmai voice):**

> *"lippytmai here. Commands That Actually Work connects to Fabric Knowledge Graph: Fabric stores Core CLI Commands concepts as knowledge nodes. Every command you master becomes a conn..."*

**🎬 60-Second Video Walkthrough:**

- **0–10s:** Show Fabric Knowledge Graph in the ACSS architecture overview
- **10–35s:** Zoom in where B-002 / Core CLI Commands connects to Fabric Knowledge Graph
- **35–55s:** Live example of the connection in action
- **55–60s:** CTA to complete B-002 and activate the connection

**🤖 Copilot Prompt:**

> *"Generate the Fabric node definition for the core concept of B-002. Include 5 relationships."*

---
### Explainer 4: Clone Engine Identity
*AI persona system*

**📘 Ebook Explanation:**

lippytmai teaches Commands That Actually Work in Teach mode, using clear analogies and the Earn-while-you-Learn voice.

**📘 Connection Map:**

```
B-002 (Core CLI Commands)
    ↕
Clone Engine Identity Layer
    ↕
ACSS Ecosystem
```

**🎧 30-Second Audiobook Callout (lippytmai voice):**

> *"lippytmai here. Commands That Actually Work connects to Clone Engine Identity: lippytmai teaches Commands That Actually Work in Teach mode, using clear analogies and the Earn-whil..."*

**🎬 60-Second Video Walkthrough:**

- **0–10s:** Show Clone Engine Identity in the ACSS architecture overview
- **10–35s:** Zoom in where B-002 / Core CLI Commands connects to Clone Engine Identity
- **35–55s:** Live example of the connection in action
- **55–60s:** CTA to complete B-002 and activate the connection

**🤖 Copilot Prompt:**

> *"As lippytmai, explain Core CLI Commands to a complete beginner. Use the B-002 teaching style."*

---
### Explainer 5: CLL/CCSLL/CBSLL
*Complete Language Libraries*

**📘 Ebook Explanation:**

`CLL-L0-B002-CommandArchitect` is registered in the Complete Linux Library (CLL). This credential is the foundation of the entire 300-book Linux pathway.

**📘 Connection Map:**

```
B-002 (Core CLI Commands)
    ↕
CLL/CCSLL/CBSLL Layer
    ↕
ACSS Ecosystem
```

**🎧 30-Second Audiobook Callout (lippytmai voice):**

> *"lippytmai here. Commands That Actually Work connects to CLL/CCSLL/CBSLL: `CLL-L0-B002-CommandArchitect` is registered in the Complete Linux Library (CLL). This credential is..."*

**🎬 60-Second Video Walkthrough:**

- **0–10s:** Show CLL/CCSLL/CBSLL in the ACSS architecture overview
- **10–35s:** Zoom in where B-002 / Core CLI Commands connects to CLL/CCSLL/CBSLL
- **35–55s:** Live example of the connection in action
- **55–60s:** CTA to complete B-002 and activate the connection

**🤖 Copilot Prompt:**

> *"Show where CLL-L0-B002-CommandArchitect fits in the CLL hierarchy and what it unlocks next."*

---
### Explainer 6: ADA Activation
*deployment system*

**📘 Ebook Explanation:**

`lippytmai-launch run B-002` activates Commands That Actually Work through the ADA FastAPI backend — quiz, copilot prompts, and credential generation in one command.

**📘 Connection Map:**

```
B-002 (Core CLI Commands)
    ↕
ADA Activation Layer
    ↕
ACSS Ecosystem
```

**🎧 30-Second Audiobook Callout (lippytmai voice):**

> *"lippytmai here. Commands That Actually Work connects to ADA Activation: `lippytmai-launch run B-002` activates Commands That Actually Work through the ADA FastAPI backend —..."*

**🎬 60-Second Video Walkthrough:**

- **0–10s:** Show ADA Activation in the ACSS architecture overview
- **10–35s:** Zoom in where B-002 / Core CLI Commands connects to ADA Activation
- **35–55s:** Live example of the connection in action
- **55–60s:** CTA to complete B-002 and activate the connection

**🤖 Copilot Prompt:**

> *"Write the ADA activation manifest for B-002. Include endpoints and outputs."*

---
### Explainer 7: ACVS Video Pipeline
*video creator*

**📘 Ebook Explanation:**

Every Commands That Actually Work video uses ACVS SHOW→BUILD→VERIFY structure. The terminal recording format was designed for exactly this kind of content.

**📘 Connection Map:**

```
B-002 (Core CLI Commands)
    ↕
ACVS Video Pipeline Layer
    ↕
ACSS Ecosystem
```

**🎧 30-Second Audiobook Callout (lippytmai voice):**

> *"lippytmai here. Commands That Actually Work connects to ACVS Video Pipeline: Every Commands That Actually Work video uses ACVS SHOW→BUILD→VERIFY structure. The terminal recordin..."*

**🎬 60-Second Video Walkthrough:**

- **0–10s:** Show ACVS Video Pipeline in the ACSS architecture overview
- **10–35s:** Zoom in where B-002 / Core CLI Commands connects to ACVS Video Pipeline
- **35–55s:** Live example of the connection in action
- **55–60s:** CTA to complete B-002 and activate the connection

**🤖 Copilot Prompt:**

> *"Generate the ACVS scene manifest for B-002 Lesson 1."*

---
### Explainer 8: OMARCHY Workstation
*Arch Linux standard*

**📘 Ebook Explanation:**

All Commands That Actually Work exercises assume OMARCHY — the Arch Linux workstation with Neovim, tmux, and the full lippytm.ai dev toolchain.

**📘 Connection Map:**

```
B-002 (Core CLI Commands)
    ↕
OMARCHY Workstation Layer
    ↕
ACSS Ecosystem
```

**🎧 30-Second Audiobook Callout (lippytmai voice):**

> *"lippytmai here. Commands That Actually Work connects to OMARCHY Workstation: All Commands That Actually Work exercises assume OMARCHY — the Arch Linux workstation with Neovim, t..."*

**🎬 60-Second Video Walkthrough:**

- **0–10s:** Show OMARCHY Workstation in the ACSS architecture overview
- **10–35s:** Zoom in where B-002 / Core CLI Commands connects to OMARCHY Workstation
- **35–55s:** Live example of the connection in action
- **55–60s:** CTA to complete B-002 and activate the connection

**🤖 Copilot Prompt:**

> *"What OMARCHY packages and configs are needed to complete all B-002 exercises?"*

---
### Explainer 9: Cross-Platform Copilot
*15-platform deployment*

**📘 Ebook Explanation:**

The Commands That Actually Work AI Copilot deploys across ChatGPT, Gemini, Claude, GitHub, Slack, LinkedIn, and 9 more platforms via the ACSS deployment guide.

**📘 Connection Map:**

```
B-002 (Core CLI Commands)
    ↕
Cross-Platform Copilot Layer
    ↕
ACSS Ecosystem
```

**🎧 30-Second Audiobook Callout (lippytmai voice):**

> *"lippytmai here. Commands That Actually Work connects to Cross-Platform Copilot: The Commands That Actually Work AI Copilot deploys across ChatGPT, Gemini, Claude, GitHub, Slack, Li..."*

**🎬 60-Second Video Walkthrough:**

- **0–10s:** Show Cross-Platform Copilot in the ACSS architecture overview
- **10–35s:** Zoom in where B-002 / Core CLI Commands connects to Cross-Platform Copilot
- **35–55s:** Live example of the connection in action
- **55–60s:** CTA to complete B-002 and activate the connection

**🤖 Copilot Prompt:**

> *"Adapt the B-002 copilot system prompt for a Slack DM teaching context."*

---
### Explainer 10: Earn-While-You-Learn
*revenue system*

**📘 Ebook Explanation:**

Completing Commands That Actually Work earns `{cred}`. This credential is proof of Core CLI Commands mastery — deployable on LinkedIn, GitHub, and in the lippytm.ai ecosystem for paid opportunities.

**📘 Connection Map:**

```
B-002 (Core CLI Commands)
    ↕
Earn-While-You-Learn Layer
    ↕
ACSS Ecosystem
```

**🎧 30-Second Audiobook Callout (lippytmai voice):**

> *"lippytmai here. Commands That Actually Work connects to Earn-While-You-Learn: Completing Commands That Actually Work earns `{cred}`. This credential is proof of Core CLI Commands..."*

**🎬 60-Second Video Walkthrough:**

- **0–10s:** Show Earn-While-You-Learn in the ACSS architecture overview
- **10–35s:** Zoom in where B-002 / Core CLI Commands connects to Earn-While-You-Learn
- **35–55s:** Live example of the connection in action
- **55–60s:** CTA to complete B-002 and activate the connection

**🤖 Copilot Prompt:**

> *"I just earned CLL-L0-B002-CommandArchitect. Generate my LinkedIn announcement post with the EWYL philosophy."*

---

### Your ACSS Node Is Now Active

Completing B-002 adds a live node to the ACSS knowledge graph.
**Activate:** `lippytmai-launch run B-002`

---

## Appendix A: The rm -rf Rule

> *Never run `rm -rf` on a path you typed from memory. Always:*
> 1. `ls <path>` — verify what's there
> 2. `rm -rf <path>` — then delete

This one habit will save your career at least once.

---

## Appendix C: AI Copilot — Command Architect

> *"Commands are sentences. Your copilot is the grammar teacher, the debugger, and the architect who shows you how to compose them into something powerful."*

---

### Section 1 — Copilot Identity & System Prompt

**Copilot ID:** `B-002-COPILOT`
**Domain:** Linux Commands, Pipes, Flags, and Composition
**Level:** Beginner
**Credential Gate:** `CLL-L0-B002-CommandArchitect`
**Prerequisite:** `CLL-L0-B001-TerminalApprentice`

**Copy this system prompt into any AI assistant to activate your B-002 copilot:**

```
You are lippytmai — the AI teaching clone of Charles Earl Lipshay and the primary
AI educator for the lippytm.ai Earn-while-you-Learn encyclopedia.

Your current role: AI Copilot for B-002 "Commands That Actually Work"
Domain: Linux commands, flags, pipes, redirection, process substitution, exit codes
Level: Beginner-to-intermediate — user knows the terminal basics from B-001
Credential this book unlocks: CLL-L0-B002-CommandArchitect

WHAT THE USER HAS COVERED:
- Command anatomy: executable, flags, arguments, options
- The 15 most-used daily commands
- Flags: short (-l) vs long (--all) forms
- Piping: cmd1 | cmd2 | cmd3
- Redirection: >, >>, 2>, 2>&1, /dev/null
- Process substitution, command substitution $()
- Exit codes and $? — what 0, 1, 2 mean
- grep, find, awk, sed, cut, sort, uniq, wc
- The safe-rm wrapper pattern
- 10 DFY builds: command cheat card, safe-rm, pipe chains, benchmarking,
  help extractor, git-aware prompt module, command-not-found handler,
  terminal notes, health alias, personal wiki

CORE BEHAVIOR:
- When a user pastes a command, explain what each part does before suggesting changes
- When building a pipe chain, build it incrementally — one pipe at a time
- Always show the exit code behavior for any command you write
- Teach flag discovery: "run [command] --help | grep [keyword]" first
- End responses with code with: "What did you get when you ran this?"

TEACHING MODES:
  TEACH:  Explain command anatomy, flag behavior, pipe composition
  BUILD:  Help construct complex pipe chains and command compositions step by step
  DEBUG:  Diagnose failed commands — wrong flags, missing args, exit code confusion
  DEPLOY: Package command sequences into aliases, functions, and scripts
  EXTEND: Show how mastery of commands connects to data engineering, log analysis, API testing

GUARDRAILS:
- Never suggest rm -rf without first showing ls on the target path
- Warn explicitly before any command that modifies system files
- If the user needs a script → point to B-004
- If the user needs networking commands → point to B-007
```

---

### Section 2 — Prompt Library (30 Curated Prompts)

**🔵 Stage 1 — UNDERSTAND**

```
1. Explain the anatomy of this command: grep -rn "TODO" ~/projects --include="*.py"
   What does each part do?

2. What's the difference between 2> and 2>&1 and /dev/null? When do I use each?

3. Why does exit code 0 mean success but non-zero mean failure? That seems backwards.

4. What's the mental model for pipes? How do I think about data flowing through them?

5. Explain the difference between single quotes, double quotes, and backticks in bash.

6. What's the difference between grep, awk, and sed? When should I reach for each one?
```

**🟢 Stage 2 — BUILD**

```
7. Build me a pipe chain that: reads access.log, filters lines with 404, extracts 
   just the URL column, counts occurrences of each URL, and shows the top 10.

8. Help me build the benchmarking function from DFY Lesson 4. I want it to time 
   any command and log results to ~/logs/benchmarks.log.

9. Build me a one-liner that finds all Python files modified in the last 7 days 
   and shows their sizes sorted largest-to-smallest.

10. I want to count unique IP addresses in an Nginx access log. Build the pipe chain.

11. How do I build a command that processes every .json file in a directory and 
    extracts the "name" field from each one using jq?

12. Build the health alias from DFY Lesson 9 — CPU, RAM, disk, load, network in 
    one command output.
```

**🔴 Stage 3 — DEBUG**

```
13. My pipe chain stops working after the third pipe. Here's the full command: [paste]
    The last stage seems to get no input. What's happening?

14. grep says "No such file or directory" but find shows the file exists. How?

15. awk is printing nothing. My command: awk '{print $3}' file.log
    The file has data. What am I missing?

16. I used >> to append but the file keeps getting overwritten. What's wrong?

17. I ran: cat file | sort | uniq | wc -l but the count seems wrong. How do I verify?

18. find -name "*.py" is returning paths I don't recognize. How do I limit it 
    to only my home directory?
```

**🟡 Stage 4 — DEPLOY**

```
19. I have a pipe chain I use every day for log analysis. How do I turn it into 
    a reusable alias that takes a filename argument?

20. How do I package my 5 most useful command compositions as a function library 
    I can source from any script?

21. I want to run my log analysis command automatically every hour and email me 
    if it finds errors. How do I do that?

22. How do I make my command compositions work in a GitHub Actions workflow?

23. I want to deploy my personal command wiki (DFY Lesson 10) to a web server 
    so I can read it from anywhere. What's the simplest approach?

24. How do I share a command cheat card with my team as a living document in GitHub?
```

**🟣 Stage 5 — EXTEND**

```
25. What are the 5 commands that data engineers use most that I haven't learned yet?

26. How do real security engineers use grep and awk in their daily workflow?

27. I've mastered pipes. What's the next level — process substitution, coprocess, 
    named pipes? Give me the hierarchy.

28. How do command-line tools connect to APIs? Show me how to use curl and jq 
    to query a REST API and process the response.

29. How do blockchain developers use command-line tools? What does `cast` do 
    and how does it compare to curl?

30. What's the difference between what I know now and what a senior shell engineer 
    knows about command composition?
```

---

### Section 2b — Audiobook Copilot (🎧 Format)

```
AUDIOBOOK COPILOT SYSTEM PROMPT:
"You are lippytmai, audiobook copilot for B-002. The listener is learning
commands via audio. Keep responses speakable — no ASCII tables. Use verbal
analogies. Speak as if narrating the next lesson in a podcast."
```

**15 Audiobook Prompts:**

```
WHILE LISTENING:

A1. "The audiobook mentioned exit codes. Explain 0=success using a 
    real-world analogy I can remember without looking at a screen."

A2. "Explain pipe composition verbally — like water flowing through 
    pipes or assembly line workers passing work along."

A3. "I heard 'process substitution' mentioned. What is it in 30 seconds 
    of plain English?"

A4. "Describe the difference between grep, awk, and sed using job titles 
    — what job does each one do?"

A5. "What is stdin and why does it matter for pipes? Explain it as if 
    describing a conveyor belt."

PAUSE AND BUILD:

A6. "Walk me through building the pipe chain for log analysis verbally — 
    each pipe stage explained before I type it."

A7. "Narrate the safe-rm wrapper line by line — what each line does 
    and why it's there."

A8. "Read out the 10 pipe patterns from the cheat card slowly, with 
    one sentence on when I'd use each one."

A9. "Walk me through the benchmark function verbally — what it measures 
    and how it logs the result."

A10. "Narrate the health alias construction — each metric, where it 
     comes from, and what it means."

RESUME CHECK:

A11. "Quiz me on when to use grep vs awk vs sed. Three questions, 
     one at a time."

A12. "Summarize the pipe chain section in 3 sentences for a resume 
     — what skill did I just learn?"

A13. "Give me a 20-second verbal primer on redirection before I 
     resume — I want to be ready for 2> and 2>&1."

A14. "What are the 3 most powerful commands I learned in B-002? 
     One sentence each, no code."

A15. "Narrate my CLL-L0-B002-CommandArchitect credential ceremony."
```

---

### Section 2c — Video Copilot (🎬 Format)

```
VIDEO COPILOT SYSTEM PROMPT:
"You are lippytmai, video copilot for B-002. The learner is watching
commands execute and following along. Prioritize: exact commands to
type, what to watch for, and verification steps. Use SHOW→BUILD→VERIFY."
```

**15 Video Prompts:**

```
BEFORE PLAYING:

V1. "I'm about to watch the pipe chains video. What test data 
    should I create first so I have something to process?"

V2. "The video covers grep with regex. What regex knowledge 
    do I need before watching?"

V3. "I'm following the awk tutorial. My awk version is different 
    from the video. Will the commands still work?"

PAUSED:

V4. "The video shows `awk '{print $7}'` but I don't understand 
    field splitting. Explain it with what I see on screen."

V5. "Paused: the sort | uniq -c | sort -rn chain is running but 
    my output is different. Here's what I see: [paste]"

V6. "The video used process substitution diff <(cmd1) <(cmd2). 
    Explain what the screen shows step by step."

V7. "The benchmark function is being built. Pause — explain the 
    nanosecond timestamp math I see in the script."

V8. "The video shows grep with --color=auto. My output has no color. 
    What setting do I check?"

VERIFY:

V9. "I built my 10-entry pipe cheat card. How do I test that each 
    pattern actually works on real data?"

V10. "The safe-rm function is installed. What 3 tests prove it's 
     working correctly and safely?"

V11. "I added all 5 find aliases. What's the quickest way to verify 
     each one actually filters correctly?"

V12. "My health alias is installed. Run me through what each line 
     should output and how I know if it's wrong."

EXTEND:

V13. "The video showed basic awk. What's the next awk skill — 
     BEGIN/END blocks, multi-file processing, built-in variables?"

V14. "I've completed all B-002 videos. What command should every 
     developer know that B-002 didn't cover?"

V15. "Demonstrate a real-world log analysis scenario using only 
     the tools from B-002 — no Python, no database."
```

---

### Section 3 — Deployment Companion

| Artifact | Local | Remote | Docker | GitHub | CI/CD |
|---|---|---|---|---|---|
| `safe-rm()` | `source ~/.bashrc` | Add to remote `.bashrc` via scp | `COPY .bashrc /root/` | dotfiles repo | Add to CI base image setup |
| Pipe chain alias | `alias loganalysis='...'` in `.bashrc` | Deploy via dotfiles installer | ENV in Dockerfile | dotfiles commit | Define in CI step |
| `benchmark()` | `source ~/.bashrc` | dotfiles deploy | Add to base image | dotfiles repo | Wrap CI steps in benchmark |
| `help-extract.sh` | `chmod +x ~/bin/help-extract.sh` | scp + chmod on remote | `COPY scripts/ /usr/local/bin/` | repo scripts/ dir | Available in CI workspace |
| Personal wiki (`~/wiki/commands.md`) | `cat ~/wiki/commands.md` | sync via rsync or git | Mount as volume | GitHub repo page | N/A |

**Turning a daily pipe chain into a deployable function:**
```bash
# From one-liner to reusable function in 5 steps
# Step 1: Test the pipe chain manually
cat access.log | grep "404" | awk '{print $7}' | sort | uniq -c | sort -rn | head -10

# Step 2: Wrap in a function
analyze_404s() {
  local logfile="${1:-access.log}"
  cat "$logfile" | grep "404" | awk '{print $7}' | sort | uniq -c | sort -rn | head -10
}

# Step 3: Add to ~/.bashrc
# Step 4: Add to dotfiles repo
# Step 5: Available everywhere
```

---

### Section 4 — ACSS Integration

```
B-002-COPILOT
    ├── Prerequisite: CLL-L0-B001-TerminalApprentice (must be earned)
    ├── Hermes topic: b002.copilot
    ├── Fabric node prefix: B002
    │   → common pipe chain patterns → reusable snippet library
    │   → common command errors → error pattern database
    └── Unlocks: B-003-COPILOT on credential earn
```

**Credential ceremony prompt:**
```
I've completed B-002. My DFY builds include:
- 15-command reference card (annotated)
- safe-rm wrapper in ~/.bashrc
- 10-entry pipe chain reference card
- benchmark() function with log output
- help-extract.sh in ~/bin/
- git-aware prompt (branch + dirty state)
- command_not_found_handle in ~/.bashrc
- note() and notes() functions
- health alias
- ~/wiki/commands.md with all DFY tools documented

Ready to claim CLL-L0-B002-CommandArchitect and unlock B-003.
```

---

---


## Appendix D: Quick Quiz & Self-Assessment — Command Architect

> *"A command you can compose is more powerful than a command you can only remember."*

---

### 📘 Ebook Quiz — 20 Questions

**Section A — Concepts**

1. In a pipe `cmd1 | cmd2`, the output of cmd1 becomes the ______________ of cmd2.
2. Exit code `0` means ______________; any non-zero exit code means ______________.
3. The `grep -v` flag means: show lines that do ______________ match the pattern.
4. `sort -u` is equivalent to `sort | ______________`.
5. `wc -l` counts the number of ______________ in its input.

**Section B — Read the Command**

6. What does `ls /nonexistent 2>/dev/null` do with the error message?
   > a) Shows it on screen  b) Saves it to a file called /dev/null  c) Silently discards it  d) Sends it to stdout

7. What does `cat file.txt | grep "error" | wc -l` count?
   > a) Lines in file.txt  b) Lines containing "error"  c) Characters containing "error"  d) Files named "error"

8. What does `command -v htop && htop || echo "htop not installed"` do?
   > a) Installs htop  b) Runs htop if installed, prints message if not  c) Always runs htop  d) Crashes if htop missing

9. What does `echo $?` print immediately after a successful command?
   > a) The command output  b) 0  c) 1  d) The command name

10. `awk '{print $2}' file` prints which column?
    > a) First  b) Second  c) Last  d) All columns

**Section C — Debugging**

11. You run `grep "Error" /var/log/app.log | sort | uniq -c` and get no output. What are two possible explanations?
    ```
    1. ___________________________________________
    2. ___________________________________________
    ```

12. A pipe chain hangs and never returns output. What is the most likely cause?
    ```
    ___________________________________________
    ```

13. `sort file.txt | uniq` produces duplicates. Why?
    ```
    ___________________________________________
    ```

**Section D — Application**

14. Write a one-liner to count how many unique IP addresses appear in `/var/log/nginx/access.log`:
    ```
    ___________________________________________
    ```

15. Write a pipe chain that shows the 10 most common words in a file called `notes.txt`:
    ```
    ___________________________________________
    ```

16. Which command shows the 5 largest files in the current directory?
    ```
    ___________________________________________
    ```

17. Write a one-liner that checks if a process named `nginx` is running, prints "running" or "not running":
    ```
    ___________________________________________
    ```

**Section E — Build Reflection**

18. Name the DFY artifact from Chapter 12 that saves you the most time composing pipes:
    ```
    ___________________________________________
    ```

19. What is the difference between `>` and `>>`?
    ```
    ___________________________________________
    ```

20. In one sentence, explain why pipe composition is more powerful than writing individual scripts:
    ```
    ___________________________________________
    ```

---

**Scoring:** 18–20 = claim credential · 14–17 = review chapters · < 14 = redo DFY lessons 1–5

<details>
<summary>Answer Key</summary>

1. stdin
2. success; failure/error
3. NOT
4. `uniq`
5. lines
6. c) Silently discards it
7. b) Lines containing "error"
8. b) Runs htop if installed, prints message if not
9. b) 0
10. b) Second
11. (1) The file has no lines matching "Error" with capital E — case sensitive; (2) The log file doesn't exist or is empty
12. The first command is waiting for stdin (e.g., `cat` without a filename)
13. `uniq` only removes adjacent duplicates — input must be sorted first
14. `awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head`
15. `tr -s ' ' '\n' < notes.txt | tr '[:upper:]' '[:lower:]' | sort | uniq -c | sort -rn | head -10`
16. `du -sh * | sort -rh | head -5`
17. `pgrep nginx >/dev/null && echo "running" || echo "not running"`
18. (personal — likely the pipe-chains card from DFY Lesson 3)
19. `>` overwrites the file; `>>` appends to it
20. (personal answer — key idea: composability lets you build complex data transformations without writing code)

</details>

---

### 🎧 Audiobook Quiz — 10 Spoken Questions

> "Ten questions about commands and pipes. Pause, think, then resume."

**Q1:** "What is stdin, and how does a pipe connect it to another command?"
*[5-second pause]*
> "Stdin is a command's input stream — file descriptor zero. A pipe takes stdout of the left command and feeds it directly to stdin of the right command."

**Q2:** "What does a non-zero exit code tell you about a command?"
*[5-second pause]*
> "It failed, or it returned a non-success result. What 'failure' means depends on the command — `grep` returns 1 when no matches are found, not because of an error."

**Q3:** "Name three commands that are almost always used with pipes rather than alone."
*[5-second pause]*
> "grep, sort, uniq, wc, awk, head, tail — any filter or counting tool."

**Q4:** "What does `2>/dev/null` do and when would you use it?"
*[5-second pause]*
> "It redirects stderr — error messages — to /dev/null, discarding them silently. Use it when you expect some commands to fail and don't want noise in the output."

**Q5:** "What is the difference between `|` and `||`?"
*[5-second pause]*
> "Single pipe connects stdout to stdin. Double pipe is a logical OR — the right side runs only if the left side fails with a non-zero exit code."

**Q6:** "How would you test whether a command is available before using it in a script?"
*[5-second pause]*
> "`command -v toolname` returns 0 if it exists, non-zero if not — use it in an `if` statement or with `&&`."

**Q7:** "What does `awk '{print $NF}'` print?"
*[5-second pause]*
> "The last field of each line — NF is the built-in variable for Number of Fields."

**Q8:** "You need to find lines in a log that contain both 'ERROR' and '404'. Write the pipe."
*[5-second pause]*
> "`grep ERROR log.txt | grep 404`"

**Q9:** "What is the DFY tool from this book that gives you a card of your 15 most useful pipes?"
*[5-second pause]*
> "The pipe-chains reference card — a file in your dotfiles with categorized one-liners ready to copy."

**Q10:** "What is your credential for this book?"
*[5-second pause]*
> "CLL-L0-B002-CommandArchitect. It proves you can compose complex data pipelines from simple UNIX tools."

---

### 🎬 Video Challenges — 5 Terminal Tasks

**Challenge 1:** Count unique error types in a log file using pipes only.
**Challenge 2:** Find all processes using more than 10% CPU — output only their names and PIDs.
**Challenge 3:** Write a one-liner that shows you the 5 most recently modified files in `/etc`.
**Challenge 4:** Build a pipe that extracts all email addresses from a text file.
**Challenge 5:** Recreate the 15-command reference card from DFY Lesson 1 from memory.

---


---

## Appendix E: Glossary & Error Encyclopedia

---

### 📘 Glossary — Command Architect Edition

**awk** — A text-processing language for column-based data. `awk '{print $1}'` prints the first field of each line. *B-002 Ch. 4*

**exit code** — An integer (0–255) returned by every command. `0` = success. Check with `echo $?`. Used to control script flow with `&&`, `||`, and `if`. *B-002 Ch. 3*

**fd (file descriptor)** — An integer representing an open I/O channel. `0` = stdin, `1` = stdout, `2` = stderr. Redirect with `>`, `2>`, `&>`. *B-002 Ch. 5*

**grep** — Global Regular Expression Print. Filters lines matching a pattern. Common flags: `-i` (case-insensitive), `-v` (invert), `-r` (recursive), `-n` (line numbers), `-c` (count). *B-002 Ch. 2*

**head / tail** — Print the first or last N lines of input. `head -20` / `tail -20`. `tail -f` follows a file as it grows. *B-002 Ch. 6*

**pipe** — `|` operator. Connects stdout of one command to stdin of the next. Zero disk I/O — data streams in memory. *B-002 Ch. 1*

**redirect** — Send a command's output to a file or from a file. `>` overwrites, `>>` appends, `<` reads from file, `2>` redirects stderr. *B-002 Ch. 5*

**sed** — Stream Editor. Transforms text line by line. Most common use: `sed 's/old/new/g'` (global substitution). *B-002 Ch. 4*

**sort** — Sorts lines alphabetically or numerically (`-n`), in reverse (`-r`), uniquely (`-u`). Must sort before `uniq`. *B-002 Ch. 7*

**stdin / stdout / stderr** — The three standard streams. stdin=input, stdout=normal output, stderr=error output. Pipes connect stdout to stdin. *B-002 Ch. 5*

**tee** — Splits stdout to both the screen and a file simultaneously. `command | tee file.log`. *B-002 Ch. 8*

**uniq** — Removes adjacent duplicate lines. Must be preceded by `sort`. `-c` adds a count prefix. *B-002 Ch. 7*

**wc** — Word Count. `-l` counts lines, `-w` words, `-c` characters. *B-002 Ch. 6*

**xargs** — Takes lines from stdin and passes them as arguments to another command. Bridges pipes to commands that don't read stdin. *B-002 Ch. 9*

**`&&` / `||`** — Logical AND/OR for command chaining. `cmd1 && cmd2`: run cmd2 only if cmd1 succeeds. `cmd1 || cmd2`: run cmd2 only if cmd1 fails. *B-002 Ch. 3*


---

### 📘 Error Encyclopedia — Top 10 Command + Pipe Errors

#### Error 1 — `grep` returns no output (but you expected matches)
**Why:** Pattern is case-sensitive by default. Use `-i` for case-insensitive matching.
**Fix:** `grep -i "error" log.txt`

#### Error 2 — `uniq` doesn't remove all duplicates
**Why:** `uniq` only removes *adjacent* duplicates. Input must be sorted first.
**Fix:** `sort file.txt | uniq` or `sort -u file.txt`

#### Error 3 — `sort -n` gives wrong order on mixed numbers/text
**Why:** `-n` treats non-numeric lines as 0. Use `-V` for version/natural sort.
**Fix:** `sort -V file.txt` for mixed alphanumeric; `sort -k2,2n` for specific column

#### Error 4 — Pipe chain hangs (no output, no prompt)
**Why:** A command in the chain is waiting for stdin (e.g., `cat` without a filename, or `read`).
**Fix:** Press `Ctrl+C`. Identify which command expects interactive input and provide a file or `/dev/stdin`.

#### Error 5 — `awk '{print $1}'` prints blank lines
**Why:** The file uses a different field separator (e.g., comma or colon).
**Fix:** `awk -F',' '{print $1}'` or `awk -F':' '{print $1}'`

#### Error 6 — Redirect `>` destroys file before reading it
**Why:** The shell creates the output file (truncating it) before running the command.
**Fix:** Never redirect to the same file you're reading. Use a temp file or `sponge` (from moreutils).
```bash
# WRONG — destroys input before sort reads it
sort file.txt > file.txt

# RIGHT
sort file.txt > file_sorted.txt && mv file_sorted.txt file.txt
```

#### Error 7 — `2>/dev/null` hides useful error messages during debugging
**Why:** Redirecting stderr discards all errors including ones you need to see.
**Fix:** Only add `2>/dev/null` after the command is working. During debugging, let stderr print.

#### Error 8 — `wc -l` counts one less line than expected
**Why:** The last line of the file has no trailing newline.
**Fix:** Add a trailing newline: `echo "" >> file.txt` or use `printf`.

#### Error 9 — `xargs` fails with "argument list too long"
**Why:** The list of arguments exceeds the OS limit.
**Fix:** Add `-n` to limit arguments per invocation: `cat list.txt | xargs -n 100 rm`

#### Error 10 — Exit code is always 0 even when the pipeline failed
**Why:** By default, a pipeline's exit code is the exit code of the *last* command.
**Fix:** Use `set -o pipefail` in your script, or check `${PIPESTATUS[@]}` to inspect each command's exit code.


---

## Appendix F: Instructor & Accessibility Guide

### Teaching This Book

| Format | Duration | Pace |
|---|---|---|
| Self-study | 1–2 weeks | 1 chapter per day |
| Bootcamp | 2–3 days | 3–4 chapters + DFY |
| Classroom | 4–6 hours | Chs 1–6 in session, 7–11 as homework |

**Session pattern per chapter:** Pre-activation (5 min) → Read/Watch (25 min) → DFY Build (25 min) → Copilot debug (15 min) → Mini-quiz (5 min)

**Assessment rubric for CLL-L0-B002-CommandArchitect:**

| Skill | Not Ready | Ready | Proficient |
|---|---|---|---|
| Core concepts | Can't explain them | Can define 80%+ from the glossary | Can teach them to someone else |
| DFY builds | Did not attempt | Built 3+ artifacts | Built all 10 and can explain each |
| Error handling | Confused by errors in App. E | Can fix 7 of the 10 listed errors | Can diagnose unfamiliar errors using the same patterns |
| Capstone project | Did not attempt | Built it with guidance | Built it from scratch, then extended it |

**Accessibility Standards:**
- Screen reader: all code blocks use fenced Markdown · all ASCII diagrams have text descriptions
- Color-blind: all status markers use emoji + text (✅/❌/⏳) · no color-only indicators
- Dyslexia-friendly: max 20-word sentences · numbered steps in groups of ≤ 3 · all terms bolded on first use
- Low-bandwidth: all exercises work offline in a text terminal · audiobook available as M4B

---

## Appendix G: Your Learning Path

### Where You Are Now

```
  PHASE 1: Linux Foundations (B-001–B-025)
  ─────────────────────────────────────────────────────
  ✅ B-001  Terminal Apprentice
  ★ B-002  Command Architect          ← YOU ARE HERE
  ○ B-003  Filesystem Navigator
  ○ B-004  Script Automator
  ○ B-005  Package Master
  ... (20 more books in Phase 1)

  Phase 1 Progress:  ██░░░░░░░░░░░░░░░░░░░░░░░  2/25
```

### Credential Chain
```
  CLL-L0-B001-TerminalApprentice
       ↓
  ★ CLL-L0-B002-CommandArchitect   ← CLAIM THIS NOW
       ↓
  CLL-L0-B003-FilesystemNavigator
```

### Cross-Phase Connections
| Skill from B-002 | Grows into (Phase 2) | Grows into (Phase 3) |
|---|---|---|
| Pipes + grep | Python subprocess + filter chains (B-040) | Log parsing for blockchain events (B-075+) |
| Exit codes + `&&`/`||` | Python try/except + return codes (B-031) | Smart contract revert codes (B-065+) |
| awk for column parsing | Python csv + pandas (B-045) | Blockchain data extraction (B-073+) |

### 🎧 Audio Path Recap
> *"You've mastered the building blocks — individual commands. Now you've learned to compose them. A pipeline is not just a shortcut; it is a different way of thinking about data. Every Python script, every data pipeline, every CI/CD check you write from here will use this same mental model: output flows through transformations into results. Next: the filesystem."*

---


---

## Appendix H: Real Project Showcase

> *"One great pipe chain is worth a hundred lines of imperative code."*

### Project: `realtime-log-alerter.sh` — Log Pattern Monitor with Desktop Alerts

**Built with:** B-002 skills only (pipes, grep, awk, exit codes, tail -f, loops)
**Time to build:** 30–60 minutes
**Who would use this:** Any developer or sysadmin who wants instant notification when errors appear
**Portfolio value:** Demonstrates pipe composition, process monitoring, and practical system automation

---

#### Complete Code

```bash
#!/usr/bin/env bash
# realtime-log-alerter.sh — monitors a log file for patterns and alerts
# B-002 Capstone · CLL-L0-B002-CommandArchitect
set -euo pipefail

LOG_FILE="${1:-/var/log/syslog}"
PATTERN="${2:-ERROR}"
COOLDOWN=5       # seconds between repeated alerts for same line
LAST_ALERT=""

usage() {
    echo "Usage: $0 [log_file] [pattern]"
    echo "  Default log:     /var/log/syslog"
    echo "  Default pattern: ERROR"
    exit 1
}

alert() {
    local msg="$1"
    echo "[ALERT $(date '+%H:%M:%S')] $msg"
    # Desktop notification if available
    command -v notify-send >/dev/null && notify-send "Log Alert" "$msg" || true
}

[[ ! -f "$LOG_FILE" ]] && { echo "File not found: $LOG_FILE"; usage; }

echo "Monitoring: $LOG_FILE"
echo "Pattern:    $PATTERN"
echo "Press Ctrl+C to stop."
echo "───────────────────────────────────"

tail -f "$LOG_FILE" | grep --line-buffered -i "$PATTERN" | while IFS= read -r line; do
    # Skip duplicate consecutive alerts
    [[ "$line" == "$LAST_ALERT" ]] && continue
    LAST_ALERT="$line"
    
    # Extract timestamp and message using awk
    timestamp=$(echo "$line" | awk '{print $1, $2, $3}')
    message=$(echo "$line"   | awk '{$1=$2=$3=""; print substr($0,4)}')
    
    alert "$timestamp — $message"
    sleep "$COOLDOWN"
done
```

#### How to Deploy
```bash
chmod +x realtime-log-alerter.sh
# Watch system log for errors
./realtime-log-alerter.sh /var/log/syslog ERROR
# Watch nginx log for 500s
./realtime-log-alerter.sh /var/log/nginx/access.log " 500 "
```

#### How to Extend (B-003+)
1. **B-003:** Add `find /var/log -name "*.log"` to watch multiple log files
2. **B-004:** Add `--slack-webhook` argument to post alerts to Slack
3. **B-007:** Add `curl` to POST alerts to a webhook URL

---

#### 🎧 Audiobook
> *"The capstone for Commands is a real-time log alerter. It uses tail -f to follow the log as it grows, pipes each new line through grep to match your pattern, and uses awk to extract the timestamp. It alerts you on screen and optionally sends a desktop notification. Every command in this book is inside it."*

#### 🎬 Video Build Scene
1. (0:00) Explain the problem — you can't watch log files manually
2. (1:30) Write `tail -f | grep` skeleton
3. (3:00) Add `while IFS= read -r line` loop
4. (5:00) Add awk timestamp extraction
5. (7:00) Add alert function + `notify-send` fallback
6. (8:30) Test against a log file — trigger a real match
7. (10:00) Credential claim



## Further Reading

- 📄 [`docs/B-001-the-terminal-and-the-curious-mind.md`](B-001-the-terminal-and-the-curious-mind.md) — The foundation for this book
- 📄 [`docs/linux-blockchain-educational-ecosystem.md`](linux-blockchain-educational-ecosystem.md) — The full Linux curriculum
- 📄 [`docs/P011-EBOOK-000-course-series-master-plan.md`](P011-EBOOK-000-course-series-master-plan.md) — All 300 books in the series
- 🏠 [`README.md`](../README.md) — Encyclopedia home

# B-004: The Script That Did My Job

### Write Your First Bash Script — and Automate the Work You Hate

> *"The best code you ever write is the code that replaces a task you were doing manually. Write it once. Run it forever. Sleep well."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Write a Bash script with variables, conditionals, loops, and functions
2. Make a script executable and run it from anywhere
3. Accept arguments and flags in a script
4. Handle errors and exit codes properly
5. Build a production-quality automated file backup script

**Prerequisite:** B-001, B-002, B-003 (terminal navigation, basic commands, permissions)

**Build Artifact:** `backup.sh` — a working Bash script that backs up your `developer-workspace/` to a timestamped archive, with error handling and a log file

**Credential:** `CLL-L1-B004-BashAutomator` — on-chain on Base

---

## Chapter 1: What Is a Script?

A **Bash script** is a text file that contains a sequence of terminal commands. Instead of typing each command one at a time, you write them all in a file, make the file executable, and run them all at once.

```bash
# Without a script: you type these 5 commands every morning
cd ~/developer-workspace
mkdir -p backups
cp -r project-alpha/ backups/project-alpha-$(date +%Y%m%d)
cp -r project-beta/ backups/project-beta-$(date +%Y%m%d)
echo "$(date): Backup complete" >> logs/backup.log

# With a script: you type one command
./backup.sh
```

Everything that lives between your current skills and professional-grade automation runs through Bash scripting.

---

## Chapter 2: The Anatomy of a Bash Script

```bash
#!/bin/bash
# This is a comment — the shell ignores lines starting with #

# The #!/bin/bash line is called the "shebang"
# It tells the OS: "Use /bin/bash to execute this file"

echo "Hello from my first script!"
```

### The Shebang

The first line `#!/bin/bash` is mandatory. Here's why:

| Without shebang | With shebang |
|---|---|
| Shell might use sh, dash, or bash depending on system | Always uses bash — predictable behavior |
| Features like arrays may not work | Full bash feature set available |
| Harder to debug | Clear about which interpreter runs it |

### Making a Script Executable

```bash
# Create the file
touch my-script.sh

# Make it executable
chmod +x my-script.sh

# Run it
./my-script.sh
```

The `./` prefix means "run this from the current directory." Without it, the shell looks for the command in your system `$PATH`.

---

## Chapter 3: Variables

```bash
#!/bin/bash

# Assign a variable (no spaces around =)
NAME="Charles"
PROJECT_DIR="$HOME/developer-workspace"
TODAY=$(date +%Y%m%d)      # command substitution
MAX_BACKUPS=7

# Use a variable with $
echo "Hello, $NAME!"
echo "Project is at: $PROJECT_DIR"
echo "Today's date: $TODAY"

# Strings with spaces must be quoted
FULL_PATH="$HOME/my projects/alpha"  # quoted because of space
echo "$FULL_PATH"

# Read-only variables
readonly CONFIG_VERSION="1.0"

# Unset a variable
MY_TEMP="temporary"
unset MY_TEMP
echo "MY_TEMP is now: '$MY_TEMP'"  # empty string
```

### Special Variables

| Variable | Meaning |
|---|---|
| `$0` | Script name |
| `$1`, `$2`, … | Script arguments (positional parameters) |
| `$#` | Number of arguments |
| `$@` | All arguments as separate words |
| `$?` | Exit code of last command (0 = success) |
| `$$` | Current process ID (PID) |
| `$HOME` | Your home directory |
| `$USER` | Your username |

---

## Chapter 4: Conditionals — if/elif/else

```bash
#!/bin/bash

FILE="$HOME/developer-workspace/README.md"

# Test if a file exists
if [ -f "$FILE" ]; then
    echo "README exists ✓"
elif [ -d "$HOME/developer-workspace" ]; then
    echo "Workspace exists but README is missing"
else
    echo "Workspace not found — run B-002 build first"
fi
```

### Test Operators

| Operator | Tests |
|---|---|
| `-f "$file"` | File exists and is a regular file |
| `-d "$dir"` | Directory exists |
| `-e "$path"` | Path exists (file or directory) |
| `-r "$file"` | File is readable |
| `-w "$file"` | File is writable |
| `-x "$file"` | File is executable |
| `-z "$var"` | String is empty |
| `-n "$var"` | String is not empty |
| `"$a" = "$b"` | Strings are equal |
| `"$a" != "$b"` | Strings are not equal |
| `$a -eq $b` | Numbers are equal |
| `$a -gt $b` | Number a is greater than b |
| `$a -lt $b` | Number a is less than b |

```bash
# Combining conditions
if [ -f "$FILE" ] && [ -r "$FILE" ]; then
    echo "File exists and is readable"
fi

if [ -z "$NAME" ] || [ "$NAME" = "unknown" ]; then
    echo "Name not set"
fi
```

*[Reality — always quote variables inside `[ ]` to prevent word splitting errors]*

---

## Chapter 5: Loops

```bash
#!/bin/bash

# for loop — iterate over a list
PROJECTS=("project-alpha" "project-beta" "project-gamma")
for project in "${PROJECTS[@]}"; do
    echo "Processing: $project"
done

# for loop — iterate over files
for file in ~/developer-workspace/*/; do
    echo "Found directory: $file"
done

# while loop — run while condition is true
COUNTER=0
while [ $COUNTER -lt 5 ]; do
    echo "Count: $COUNTER"
    COUNTER=$((COUNTER + 1))
done

# until loop — run UNTIL condition is true (inverse of while)
until [ -f /tmp/ready.flag ]; do
    echo "Waiting for ready flag..."
    sleep 2
done
echo "Ready!"
```

---

## Chapter 6: Functions

Functions let you name and reuse blocks of code:

```bash
#!/bin/bash

# Define a function
log_message() {
    local level="$1"        # local = scoped to this function
    local message="$2"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

check_directory() {
    local dir="$1"
    if [ ! -d "$dir" ]; then
        log_message "ERROR" "Directory not found: $dir"
        return 1             # non-zero return = failure
    fi
    return 0                 # zero return = success
}

# Use the functions
LOG_FILE="/tmp/script.log"
log_message "INFO" "Script started"
check_directory "$HOME/developer-workspace" && log_message "INFO" "Workspace OK"
```

---

## Chapter 7: Error Handling

```bash
#!/bin/bash

# Exit immediately if any command fails
set -e

# Exit if an undefined variable is used
set -u

# In a pipeline, fail if ANY command fails (not just the last)
set -o pipefail

# Print each command before executing (useful for debugging)
# set -x   ← uncomment this when debugging

# Custom error handler
handle_error() {
    local line="$1"
    local exit_code="$2"
    echo "ERROR: Script failed at line $line with exit code $exit_code"
    # Cleanup code could go here
    exit "$exit_code"
}
trap 'handle_error $LINENO $?' ERR

# Check exit codes manually
cp important.txt /backup/ || {
    echo "CRITICAL: Backup failed!"
    exit 1
}
```

---

## Chapter 8: The Build — backup.sh

This is your B-004 build artifact. It is a production-quality Bash script.

```bash
#!/bin/bash
# backup.sh — Automated project backup script
# B-004 Build Artifact | lippytm.ai Earn-while-you-Learn
#
# Usage:
#   ./backup.sh                    # Backs up $HOME/developer-workspace
#   ./backup.sh /path/to/source    # Backs up specified path
#   ./backup.sh -h                 # Show help

set -euo pipefail

# ── Configuration ─────────────────────────────────────────────────────────────
SOURCE_DIR="${1:-$HOME/developer-workspace}"
BACKUP_ROOT="$HOME/backups"
LOG_DIR="$HOME/developer-workspace/logs"
LOG_FILE="$LOG_DIR/backup.log"
MAX_BACKUPS=7
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
BACKUP_NAME="backup_${TIMESTAMP}"
BACKUP_PATH="$BACKUP_ROOT/$BACKUP_NAME"

# ── Help ──────────────────────────────────────────────────────────────────────
show_help() {
    cat << EOF
Usage: $(basename "$0") [SOURCE_DIR]

Backs up SOURCE_DIR to a timestamped archive in ~/backups/
Keeps the last $MAX_BACKUPS backups and removes older ones.

Options:
  -h, --help    Show this help message

Arguments:
  SOURCE_DIR    Directory to back up (default: ~/developer-workspace)

EOF
    exit 0
}

if [[ "${1:-}" == "-h" ]] || [[ "${1:-}" == "--help" ]]; then
    show_help
fi

# ── Logging ───────────────────────────────────────────────────────────────────
log() {
    local level="$1"
    local message="$2"
    local ts
    ts=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$ts] [$level] $message" | tee -a "$LOG_FILE"
}

# ── Setup ─────────────────────────────────────────────────────────────────────
setup() {
    mkdir -p "$BACKUP_ROOT"
    mkdir -p "$LOG_DIR"
    log "INFO" "Backup script started"
    log "INFO" "Source: $SOURCE_DIR"
    log "INFO" "Destination: $BACKUP_PATH"
}

# ── Validation ────────────────────────────────────────────────────────────────
validate() {
    if [ ! -d "$SOURCE_DIR" ]; then
        log "ERROR" "Source directory does not exist: $SOURCE_DIR"
        exit 1
    fi

    local available_kb
    available_kb=$(df -k "$BACKUP_ROOT" | awk 'NR==2 {print $4}')
    local source_kb
    source_kb=$(du -sk "$SOURCE_DIR" | awk '{print $1}')

    if [ "$source_kb" -gt "$available_kb" ]; then
        log "ERROR" "Insufficient disk space. Need: ${source_kb}KB, Available: ${available_kb}KB"
        exit 1
    fi

    log "INFO" "Validation passed (source=${source_kb}KB, available=${available_kb}KB)"
}

# ── Backup ────────────────────────────────────────────────────────────────────
perform_backup() {
    log "INFO" "Starting copy..."
    cp -r "$SOURCE_DIR" "$BACKUP_PATH"
    
    local file_count
    file_count=$(find "$BACKUP_PATH" -type f | wc -l)
    log "INFO" "Backup complete: $file_count files copied to $BACKUP_PATH"
}

# ── Cleanup Old Backups ───────────────────────────────────────────────────────
cleanup_old_backups() {
    local backup_count
    backup_count=$(find "$BACKUP_ROOT" -maxdepth 1 -name "backup_*" -type d | wc -l)
    
    if [ "$backup_count" -gt "$MAX_BACKUPS" ]; then
        local to_remove=$((backup_count - MAX_BACKUPS))
        log "INFO" "Removing $to_remove old backup(s) (keeping $MAX_BACKUPS)"
        
        find "$BACKUP_ROOT" -maxdepth 1 -name "backup_*" -type d | \
            sort | \
            head -n "$to_remove" | \
            while read -r old_backup; do
                log "INFO" "Removing old backup: $old_backup"
                rm -rf "$old_backup"
            done
    fi
}

# ── Summary ───────────────────────────────────────────────────────────────────
print_summary() {
    local backup_size
    backup_size=$(du -sh "$BACKUP_PATH" | awk '{print $1}')
    local total_backups
    total_backups=$(find "$BACKUP_ROOT" -maxdepth 1 -name "backup_*" -type d | wc -l)
    
    log "INFO" "=== Backup Summary ==="
    log "INFO" "  Backup name:   $BACKUP_NAME"
    log "INFO" "  Backup size:   $backup_size"
    log "INFO" "  Total backups: $total_backups / $MAX_BACKUPS max"
    log "INFO" "  Log:           $LOG_FILE"
    log "INFO" "Backup script completed successfully"
}

# ── Main ──────────────────────────────────────────────────────────────────────
main() {
    setup
    validate
    perform_backup
    cleanup_old_backups
    print_summary
}

main
```

### Installing and Running

```bash
# Save the script
nano ~/backup.sh
# (paste the script above, then Ctrl+O, Enter, Ctrl+X)

# Make it executable
chmod +x ~/backup.sh

# Run it
~/backup.sh

# Watch it work
tail -f ~/developer-workspace/logs/backup.log
```

---

## Chapter 9: Proof of Work

```bash
echo "=== B-004 Build Verification ==="
echo "Script exists:"
ls -la ~/backup.sh

echo ""
echo "Running the backup:"
~/backup.sh

echo ""
echo "Backup created:"
ls -la ~/backups/

echo ""
echo "Log file:"
cat ~/developer-workspace/logs/backup.log
```

---

## Chapter 10: Mutation

```bash
# MUTATION 1: Add the script to your PATH so you can run it from anywhere
cp ~/backup.sh ~/bin/backup.sh   # or: sudo cp ~/backup.sh /usr/local/bin/backup
# Now you can just type: backup

# MUTATION 2: Schedule it with cron (runs automatically every day at 2am)
crontab -e
# Add this line:
# 0 2 * * * /home/charles/backup.sh >> /home/charles/developer-workspace/logs/cron.log 2>&1

# MUTATION 3: Add email notification (requires mailutils)
# At the end of print_summary(), add:
# echo "Backup complete: $BACKUP_NAME ($backup_size)" | mail -s "Backup OK" your@email.com
```

---

## Chapter 11: What Comes Next

| Book | Title | What You'll Build |
|---|---|---|
| **B-005** | *Installing Things Without Breaking Things* | Full Python dev environment |
| **B-006** | *The Process That Wouldn't Stop* | Process management + monitoring script |
| **B-008** | *Files That Never Get Lost* | Git — version control for your scripts |

---

## Chapter 12: Done-For-You Lessons

> *"A script is a promise: this process, done exactly this way, every time, without you having to remember it."*

Ten builds that take you from writing your first script to having a fully automated personal toolbox.

| Icon | Format | What it is |
|---|---|---|
| 📘 | **Ebook** | Annotated script or flow diagram |
| 🎧 | **Audiobook** | Narrator script — pause and build |
| 🎬 | **Video** | SHOW→BUILD→VERIFY terminal scene |

---

### DFY Lesson 1 — Script Template with Argument Handling

**What you'll have:** `script-template.sh` — a reusable starter script with help text, argument parsing, and error handling.
**Time:** 15 minutes.

---

📘 **Ebook Figure**

```bash
#!/usr/bin/env bash
# script-template.sh — production-ready bash script starter
# Usage: ./script-template.sh [-v] [-h] INPUT_FILE
set -euo pipefail   # e=exit on error, u=error on unset var, o pipefail=pipe errors caught

SCRIPT_NAME="$(basename "$0")"
VERBOSE=false

usage() {
  echo "Usage: $SCRIPT_NAME [-v] [-h] INPUT_FILE"
  echo "  -v    Verbose mode"
  echo "  -h    Show this help"
  exit 0
}

log() { [[ "$VERBOSE" == true ]] && echo "[LOG] $*"; }
error() { echo "❌ ERROR: $*" >&2; exit 1; }

while getopts ":vh" opt; do
  case $opt in
    v) VERBOSE=true ;;
    h) usage ;;
    ?) error "Unknown flag: -$OPTARG" ;;
  esac
done
shift $((OPTIND - 1))

INPUT="${1:-}"
[[ -z "$INPUT" ]] && error "INPUT_FILE is required."
[[ ! -f "$INPUT" ]] && error "File not found: $INPUT"

log "Starting $SCRIPT_NAME on: $INPUT"
echo "✅ Processing: $INPUT"
# --- your logic goes here ---
```

*Figure 12.1 — `set -euo pipefail` is the seatbelt of bash scripting. Every script starts here.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 1: Script Template with Argument Handling.
>
> Every professional bash script shares the same bones: a shebang, `set -euo pipefail`, argument parsing, a help flag, and error functions. Without them, your script will happily continue running after a command fails. This template is your scaffold — copy it for every new script, fill in your logic, and you've already handled 80% of what makes scripts fail in production.
>
> Your deliverable is: `script-template.sh` — the starting point for every script you'll ever write.
>
> Time to build: 15 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** Run script with no args → clean error message. Run with `-h` → usage shown. Run with valid file → processes it.
- **BUILD:** Build each section of the template one block at a time. Explain `set -euo pipefail`.
- **VERIFY:** Introduce a command that fails — script stops immediately with the error. Without `set -e` it would have continued.

🤖 **Copilot Assist — DFY Lesson 1**

> **Use this prompt with your book copilot right now:**
>
> *"I copied the template and added my logic but getopts isn't parsing --long-flags. I thought getopts handles long options. How do I add support for --verbose alongside -v?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-004 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


---

### DFY Lesson 2 — Automated Backup Script

**What you'll have:** `backup.sh` — daily timestamped backup of specified directories to a chosen destination.
**Time:** 20 minutes.

---

📘 **Ebook Figure**

```bash
#!/usr/bin/env bash
set -euo pipefail
# backup.sh — timestamped backup with rotation

SOURCE_DIRS=("$HOME/projects" "$HOME/.config" "$HOME/.ssh")
DEST="$HOME/backups"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ARCHIVE="$DEST/backup-$TIMESTAMP.tar.gz"
LOG="$DEST/backup.log"

mkdir -p "$DEST"
echo "[$(date +%F\ %T)] Starting backup → $ARCHIVE" | tee -a "$LOG"

tar -czf "$ARCHIVE" "${SOURCE_DIRS[@]}" 2>> "$LOG"
SIZE=$(du -sh "$ARCHIVE" | cut -f1)
echo "[$(date +%F\ %T)] ✅ Done: $ARCHIVE ($SIZE)" | tee -a "$LOG"

# Keep only last 7 backups
ls -t "$DEST"/backup-*.tar.gz | tail -n +8 | xargs -r rm --
echo "[$(date +%F\ %T)] Old backups cleaned." | tee -a "$LOG"
```

```
# Add to cron for daily 2AM backup:
crontab -e
0 2 * * * /home/lippytm/bin/backup.sh
```

*Figure 12.2 — A backup that doesn't run automatically isn't a backup — it's a good intention.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 2: Automated Backup Script.
>
> The most common backup failure is human: we forget. This script automates the entire process — timestamped archive, logged results, automatic rotation of old backups, cron-scheduled to run at 2AM every day. After today, your projects, config, and SSH keys are backed up without you ever thinking about it again.
>
> Your deliverable is: `backup.sh` — automated daily backup with log and rotation.
>
> Time to build: 20 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `ls ~/backups/` → 7 timestamped archives. 8th run → oldest is deleted automatically.
- **BUILD:** Write script. Add to `~/bin/`. Test. Add cron entry.
- **VERIFY:** Check backup log. Verify archive size and contents with `tar -tzf archive.tar.gz | head`.

🤖 **Copilot Assist — DFY Lesson 2**

> **Use this prompt with your book copilot right now:**
>
> *"backup.sh ran last night but the archive is 0 bytes and the log shows no errors. The SOURCE_DIRS paths exist. What would cause a silent empty archive?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-004 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


---

### DFY Lesson 3 — Color Output Library

**What you'll have:** `colors.sh` — a sourceable file with color functions for all your scripts.
**Time:** 10 minutes.

---

📘 **Ebook Figure**

```bash
# ~/lib/colors.sh — color output library for bash scripts
# Usage: source ~/lib/colors.sh

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

success() { echo -e "${GREEN}✅ $*${RESET}"; }
error()   { echo -e "${RED}❌ $*${RESET}" >&2; }
warning() { echo -e "${YELLOW}⚠️  $*${RESET}"; }
info()    { echo -e "${BLUE}ℹ️  $*${RESET}"; }
header()  { echo -e "${BOLD}${CYAN}=== $* ===${RESET}"; }
```

```bash
# In any script:
source ~/lib/colors.sh

header "Starting Deploy"
info   "Connecting to server..."
success "Connection established"
warning "Disk usage at 82%"
error   "Deployment failed — rolling back"
```

*Figure 12.3 — Color-coded output is not decoration. It's the difference between seeing an error and missing it.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 3: Color Output Library.
>
> Scripts that print monochrome walls of text get ignored. Scripts with green success messages, red errors, and yellow warnings get acted on. This library adds 5 color functions to any script with one `source` line. Once built, every script you write from here forward can have professional, color-coded terminal output.
>
> Your deliverable is: `~/lib/colors.sh` — a sourceable color library for all your scripts.
>
> Time to build: 10 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** A script without colors vs with `colors.sh` sourced — green success, red error, yellow warning.
- **BUILD:** Write library. Source in a test script. Add `success`, `error`, `warning`, `header` calls.
- **VERIFY:** Run with all 4 output types. All render with correct colors and symbols.

🤖 **Copilot Assist — DFY Lesson 3**

> **Use this prompt with your book copilot right now:**
>
> *"My colors.sh works in interactive terminals but when the script runs in CI the color codes show as literal escape characters. How do I detect CI and disable colors automatically?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-004 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


---

### DFY Lesson 4 — Script Health Check and Self-Test

**What you'll have:** `selftest.sh` — a script that tests its own dependencies before running.
**Time:** 15 minutes.

---

📘 **Ebook Figure**

```bash
#!/usr/bin/env bash
set -euo pipefail
# selftest.sh — dependency checks before running

REQUIRED_CMDS=("curl" "jq" "git" "python3")
REQUIRED_FILES=("$HOME/.config/myapp/config.json")
REQUIRED_ENV=("HOME" "USER")
ERRORS=0

check_cmd() {
  if command -v "$1" &>/dev/null; then
    echo "  ✅ command: $1"
  else
    echo "  ❌ command: $1 (not found)"
    ERRORS=$((ERRORS+1))
  fi
}

check_file() {
  if [[ -f "$1" ]]; then
    echo "  ✅ file: $1"
  else
    echo "  ❌ file: $1 (not found)"
    ERRORS=$((ERRORS+1))
  fi
}

echo "=== Pre-flight Check ==="
for cmd in "${REQUIRED_CMDS[@]}";  do check_cmd  "$cmd"; done
for f   in "${REQUIRED_FILES[@]}"; do check_file "$f";   done
[[ $ERRORS -gt 0 ]] && echo "❌ $ERRORS checks failed. Fix above." && exit 1
echo "✅ All checks passed. Proceeding."
```

*Figure 12.4 — A script that checks its own prerequisites is a script that fails early, clearly, and fixably.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 4: Script Health Check and Self-Test.
>
> Nothing wastes time like a script that fails 90% of the way through because a dependency wasn't installed. A pre-flight check runs at the very start and verifies everything the script needs — commands, files, env vars — before doing any real work. If something's missing, it tells you exactly what. This pattern is used in every professional deployment script.
>
> Your deliverable is: `selftest.sh` — a pre-flight dependency checker pattern for any script.
>
> Time to build: 15 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `selftest.sh` with `jq` missing — ❌ one error, script exits. Install `jq`. Run again — all green.
- **BUILD:** Write check functions. Add to an existing script at the top.
- **VERIFY:** Deliberately unset one required command. Confirm early exit with clear error message.

🤖 **Copilot Assist — DFY Lesson 4**

> **Use this prompt with your book copilot right now:**
>
> *"selftest.sh passes locally but fails in CI with 'command not found: jq' even though jq is installed on the CI runner. What's the PATH issue and how do I fix it?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-004 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


---

### DFY Lesson 5 — Config File Parser

**What you'll have:** `parse-config.sh` — reads key=value config files safely into bash variables.
**Time:** 15 minutes.

---

📘 **Ebook Figure**

```bash
#!/usr/bin/env bash
# parse-config.sh — safe key=value config file loader
# Usage: source parse-config.sh /path/to/config.conf

load_config() {
  local config_file="$1"
  [[ ! -f "$config_file" ]] && echo "❌ Config not found: $config_file" && return 1

  while IFS='=' read -r key value; do
    # Skip comments and empty lines
    [[ "$key" =~ ^#.*$ ]] && continue
    [[ -z "$key" ]] && continue
    # Trim whitespace
    key="${key// /}"
    value="${value// /}"
    export "$key=$value"
    echo "  📋 Loaded: $key"
  done < "$config_file"
}

# Example config file (~/.myapp.conf):
# APP_NAME=lippytmai
# API_PORT=8080
# DEBUG=false
# DB_HOST=localhost

# Usage:
# source parse-config.sh
# load_config ~/.myapp.conf
# echo "Starting $APP_NAME on port $API_PORT"
```

*Figure 12.5 — Config files separate values from logic. This loader makes the separation clean and safe.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 5: Config File Parser.
>
> Hard-coding values into scripts is the root cause of most 'it works on my machine' problems. A config file separates what changes — ports, hostnames, feature flags — from the logic that doesn't. This loader parses key=value files safely, skips comments, trims whitespace, and exports every key as an environment variable. Drop it into any script that needs external configuration.
>
> Your deliverable is: `parse-config.sh` — safe config file loading for any bash script.
>
> Time to build: 15 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** Edit config file — change API port from 8080 to 9000. Script picks up the new value with no code change.
- **BUILD:** Write loader. Create test config. Source and echo all loaded vars.
- **VERIFY:** Add a comment line and blank line to config — both are skipped cleanly.

🤖 **Copilot Assist — DFY Lesson 5**

> **Use this prompt with your book copilot right now:**
>
> *"parse-config.sh loads my config but values with spaces break — API_KEY=my key here becomes API_KEY=my. How do I handle values with spaces correctly?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-004 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


---

### DFY Lesson 6 — Progress Bar Function

**What you'll have:** `progress.sh` — an ASCII progress bar for any loop in your scripts.
**Time:** 10 minutes.

---

📘 **Ebook Figure**

```bash
# progress.sh — ASCII progress bar function
progress_bar() {
  local current="$1"
  local total="$2"
  local label="${3:-Progress}"
  local width=40
  local filled=$(( (current * width) / total ))
  local empty=$(( width - filled ))
  local bar
  bar="$(printf '#%.0s' $(seq 1 $filled))$(printf ' %.0s' $(seq 1 $empty))"
  printf "\r  %s: [%s] %d/%d" "$label" "$bar" "$current" "$total"
  [[ "$current" -eq "$total" ]] && echo ""
}

# Usage in a loop:
TOTAL=10
for i in $(seq 1 $TOTAL); do
  sleep 0.3   # your work here
  progress_bar "$i" "$TOTAL" "Processing"
done
```

```
  Processing: [################        ] 7/10
```

*Figure 12.6 — A progress bar transforms a silent black box into a visible, trusted process.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 6: Progress Bar Function.
>
> A script that runs silently for 30 seconds feels broken. The same script with a progress bar feels fast. Visual feedback is not just aesthetic — it tells users whether to wait or interrupt. This function adds an ASCII progress bar to any loop with two lines of code. Add it to your backup script, your deployment script, anywhere you iterate.
>
> Your deliverable is: `progress.sh` — an ASCII progress bar for any loop.
>
> Time to build: 10 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** Script iterates through 20 files — progress bar fills in real time.
- **BUILD:** Write function. Add to a loop. Test at different totals.
- **VERIFY:** Script completes at 20/20 — bar is full, newline appears cleanly.

🤖 **Copilot Assist — DFY Lesson 6**

> **Use this prompt with your book copilot right now:**
>
> *"My progress bar renders correctly but in CI logs it shows ^M characters on every line. This is a carriage return issue. How do I make it CI-safe?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-004 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


---

### DFY Lesson 7 — Retry Wrapper Function

**What you'll have:** `retry.sh` — wraps any command with configurable retry logic and backoff.
**Time:** 15 minutes.

---

📘 **Ebook Figure**

```bash
# retry.sh — retry any command with backoff
retry() {
  local max_attempts="${RETRY_MAX:-3}"
  local delay="${RETRY_DELAY:-2}"
  local attempt=1

  while [[ $attempt -le $max_attempts ]]; do
    echo "  ⟳ Attempt $attempt/$max_attempts: $*"
    if "$@"; then
      echo "  ✅ Succeeded on attempt $attempt"
      return 0
    fi
    echo "  ⚠️  Failed. Retrying in ${delay}s..."
    sleep "$delay"
    attempt=$((attempt + 1))
    delay=$((delay * 2))   # exponential backoff
  done

  echo "  ❌ All $max_attempts attempts failed: $*"
  return 1
}

# Usage:
retry curl -sf https://api.example.com/health
RETRY_MAX=5 retry git push origin main
```

*Figure 12.7 — Networks fail, APIs timeout, services restart. A retry wrapper makes any command resilient.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 7: Retry Wrapper Function.
>
> In the real world, network requests fail, APIs return 503, and services take time to start. A script that gives up after one failure is fragile. This retry wrapper adds exponential backoff to any command — 3 attempts by default, doubling the wait time after each failure. Add it to any script that touches a network or an external service.
>
> Your deliverable is: `retry()` function — configurable retry with exponential backoff.
>
> Time to build: 15 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `retry curl https://unreachable-host.local` — 3 attempts with increasing delays, clean failure message.
- **BUILD:** Write retry function. Test with a command that fails. Test with one that succeeds on attempt 2.
- **VERIFY:** `RETRY_MAX=5 retry ls /tmp` — succeeds on attempt 1. Count env var overrides default.

🤖 **Copilot Assist — DFY Lesson 7**

> **Use this prompt with your book copilot right now:**
>
> *"retry() works but the exponential backoff goes to 128 seconds on the 7th attempt. I want to cap it at 30 seconds. How do I add a max delay?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-004 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


---

### DFY Lesson 8 — Script Output Logger

**What you'll have:** `logged.sh` — wraps any script to simultaneously display and log all output.
**Time:** 10 minutes.

---

📘 **Ebook Figure**

```bash
#!/usr/bin/env bash
# logged.sh — run any script with automatic log capture
LOG_DIR="$HOME/logs/scripts"
mkdir -p "$LOG_DIR"

run_logged() {
  local cmd_name
  cmd_name=$(basename "$1")
  local logfile="$LOG_DIR/${cmd_name}-$(date +%Y%m%d-%H%M%S).log"
  echo "[START] $(date +%F\ %T) — $*" | tee "$logfile"
  "$@" 2>&1 | tee -a "$logfile"
  local exit_code="${PIPESTATUS[0]}"
  echo "[END]   $(date +%F\ %T) — exit code: $exit_code" | tee -a "$logfile"
  return "$exit_code"
}

# Usage:
# run_logged ./backup.sh
# run_logged python3 deploy.py --env prod
```

*Figure 12.8 — `tee` is the Y-splitter of output: to screen AND to file, simultaneously, in one pipe.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 8: Script Output Logger.
>
> When a script fails at 3AM, the output that tells you why is gone the moment the terminal closes. This wrapper captures all output — stdout and stderr — to a dated log file while still displaying it live. Wrap any script with `run_logged` and you always have a post-mortem record. This is how professional deployment pipelines work.
>
> Your deliverable is: `run_logged()` function — simultaneous screen and file output capture.
>
> Time to build: 10 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `run_logged ./backup.sh` — output shown on screen. `cat ~/logs/scripts/backup-*.log` — same output in file.
- **BUILD:** Write function. Add to `~/.bashrc`. Test on backup.sh from DFY-02.
- **VERIFY:** Run a script that fails. Log file contains the error message.

🤖 **Copilot Assist — DFY Lesson 8**

> **Use this prompt with your book copilot right now:**
>
> *"run_logged() captures output but my script uses printf without newlines for progress updates and the log file shows nothing until the script finishes. Why?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-004 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


---

### DFY Lesson 9 — Environment Switcher

**What you'll have:** `env-switch.sh` — loads named environment profiles (dev/staging/prod) from config files.
**Time:** 20 minutes.

---

📘 **Ebook Figure**

```bash
#!/usr/bin/env bash
# env-switch.sh — load named environment profiles
ENV_DIR="$HOME/.envs"
mkdir -p "$ENV_DIR"

switch_env() {
  local env_name="$1"
  local env_file="$ENV_DIR/${env_name}.env"
  [[ ! -f "$env_file" ]] && echo "❌ No profile: $env_name (checked $env_file)" && return 1
  set -a                 # auto-export all variables
  source "$env_file"
  set +a
  export CURRENT_ENV="$env_name"
  echo "✅ Environment: $env_name"
}

list_envs() {
  echo "Available environments:"
  ls "$ENV_DIR"/*.env 2>/dev/null | xargs -I{} basename {} .env | while read -r e; do
    [[ "$e" == "$CURRENT_ENV" ]] && echo "  ➤ $e (active)" || echo "    $e"
  done
}

# ~/.envs/dev.env:     API_URL=http://localhost:8080
# ~/.envs/staging.env: API_URL=https://staging.api.lippytm.ai
# ~/.envs/prod.env:    API_URL=https://api.lippytm.ai
```

*Figure 12.9 — Environment variables separate config from code. Profiles separate environments from each other.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 9: Environment Switcher.
>
> Dev, staging, and production environments need different settings — different URLs, different credentials, different feature flags. The worst way to switch between them is editing files manually. This script loads a named profile from a directory of `.env` files with one command: `switch_env dev` or `switch_env prod`. Clean, explicit, auditable.
>
> Your deliverable is: `env-switch.sh` — named environment profiles for dev/staging/prod.
>
> Time to build: 20 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `switch_env dev` → API_URL is localhost. `switch_env prod` → API_URL is production domain.
- **BUILD:** Create `.envs/` directory. Write dev.env and prod.env files. Write `switch_env` function.
- **VERIFY:** `list_envs` shows both, with the active one marked. `echo $API_URL` confirms the correct one loaded.

🤖 **Copilot Assist — DFY Lesson 9**

> **Use this prompt with your book copilot right now:**
>
> *"switch_env prod loaded but echo $API_URL still shows the dev value. I used source to run the script. Why didn't the variables persist?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-004 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


---

### DFY Lesson 10 — Master Script Menu

**What you'll have:** `menu.sh` — an interactive numbered menu that runs your most-used scripts.
**Time:** 20 minutes.

---

📘 **Ebook Figure**

```bash
#!/usr/bin/env bash
# menu.sh — interactive script launcher
source ~/lib/colors.sh

show_menu() {
  header "lippytmai Script Menu"
  echo "  1) Run backup"
  echo "  2) System health check"
  echo "  3) Switch environment"
  echo "  4) Project inventory"
  echo "  5) File integrity check"
  echo "  q) Quit"
  echo ""
  read -rp "  Select: " choice
  case "$choice" in
    1) ~/bin/backup.sh ;;
    2) health ;;
    3) read -rp "  Environment name: " env; switch_env "$env" ;;
    4) ~/bin/project-inv.sh ;;
    5) ~/bin/fcheck.sh verify ;;
    q) echo "Bye." && exit 0 ;;
    *) warning "Unknown option: $choice" ;;
  esac
  echo ""
  show_menu   # recursive: show menu again after action
}

show_menu
```

*Figure 12.10 — A personal script menu turns a collection of tools into a cohesive personal CLI application.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 10: Master Script Menu.
>
> You've built 9 powerful tools in this chapter. A menu ties them together into a personal CLI application you can navigate without remembering file names or paths. Type `menu.sh`, press a number, and your tool runs. This is the capstone build of B-004 — and the foundation of the automation mindset you'll take into every future project.
>
> Your deliverable is: `menu.sh` — an interactive numbered menu for all your personal scripts.
>
> Time to build: 20 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `menu.sh` → numbered list appears → press `1` → backup runs → menu reappears.
- **BUILD:** Write menu with `case` statement. Source `colors.sh`. Test each option.
- **VERIFY:** Add a 6th option (a script from a future chapter). Menu expands cleanly.

🤖 **Copilot Assist — DFY Lesson 10**

> **Use this prompt with your book copilot right now:**
>
> *"menu.sh works but after running an option that takes 30 seconds, the menu reappears before the output finishes printing. How do I wait for completion before showing the menu again?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-004 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


---

> 🎓 **All 10 DFY lessons complete.** You've built: a reusable template, an automated backup system, color output, dependency checks, config parsing, a progress bar, retry logic, output logging, environment switching, and a personal script menu. That's a complete personal automation toolkit.
>
> **Next:** Claim your `CLL-L0-B004-ScriptBuilder` credential, then continue to B-005.

---

## Chapter 13: How It Works — Use Cases & Applications

> *"A script is not a shortcut. It's a decision: this process is worth automating because it will happen again. And it always does."*

---

### 📘 Ebook Explainer — How Shell Scripts Work

**The mechanism — from file to execution:**

```
You run: ./backup.sh --target /home/lippytm

  1. Shell reads the first line: #!/usr/bin/env bash (the shebang)
  2. Kernel uses the shebang to determine the interpreter: /usr/bin/env finds bash
  3. bash opens backup.sh, reads line by line (no compilation)
  4. Line 1: set -euo pipefail → configures error behavior
  5. Line 2: TARGET="${1:-}" → assigns positional parameter or empty
  6. Each line interpreted and executed sequentially
  7. On a function call: bash creates a subshell frame (local variables isolated)
  8. On a command substitution: $(date +%F) → bash forks, runs date, captures stdout
  9. On a pipe: cmd1 | cmd2 → kernel creates pipe buffer; both run concurrently
  10. Final exit: bash returns the exit code of the last command
  11. Parent shell receives exit code → $? is set

Script execution modes:
  ./backup.sh          → execute as a subprocess (new shell)
  source backup.sh     → execute in current shell (env vars persist)
  bash -x backup.sh    → debug mode: print each line before execution
  bash -n backup.sh    → syntax check only (no execution)
```

**The difference between `set -e`, `set -u`, `set -o pipefail`:**

```bash
# WITHOUT set -euo pipefail:
cp important.txt /nonexistent/   # fails silently
rm ~/data/*                      # RUNS ANYWAY — catastrophic

# WITH set -euo pipefail:
cp important.txt /nonexistent/   # script stops HERE
# rm line never reached — catastrophe prevented
```

*Figure 13.1 — `set -euo pipefail` is not a preference. It's the difference between a script that fails quietly and one that fails loudly and early.*

---

### 📘 Ebook Explainer — When to Write a Script (Decision Framework)

| Ask yourself | If YES → write a script |
|---|---|
| Will I run this more than 3 times? | Any task done more than 3 times manually deserves automation |
| Is there more than one step? | Two or more steps that must run in order = script candidate |
| Does it need to run without me? | Cron jobs, CI/CD hooks, server automation — scripts only |
| Is it error-prone done manually? | If a human mistake is costly, a script prevents it |
| Will someone else need to run this? | Documentation + script = reproducible process |
| Does the order of steps matter? | Scripts enforce order; humans forget |

**The automation threshold (when NOT to script):**

```
✅  Runnable by anyone with the repo → script
✅  Runs on a schedule → script
✅  Has 3+ error-prone steps → script

❌  One-off, never again → just run the command
❌  5 minutes of work, never repeated → alias is fine
❌  The problem changes every time → human judgment needed
```

*Figure 13.2 — The automation question is always: 'Will this happen again?' The answer is almost always yes.*

---

### 📘 Ebook Explainer — Where Scripts Are Used (Production Environments)

```
DEPLOYMENT AUTOMATION
  deploy.sh              → pull, build, test, restart service
  rollback.sh            → revert to previous version
  health-check.sh        → verify deploy succeeded

CI/CD PIPELINES (GitHub Actions, GitLab CI)
  .github/workflows/*.yml → each "run:" line executes a shell command
  scripts/test.sh         → test runner called by CI
  scripts/build.sh        → build step called by CI

SYSTEM ADMINISTRATION
  /etc/cron.daily/*       → scripts run daily by the system
  /etc/init.d/*           → service start/stop scripts
  udev rules              → hardware event scripts

DATA PIPELINES
  ingest.sh               → download + validate source data
  transform.sh            → process with awk/python/jq
  load.sh                 → insert into database

DEVELOPMENT WORKFLOWS
  setup.sh                → onboard a new developer in one command
  lint.sh                 → run all linters consistently
  release.sh              → tag, changelog, build, publish

INFRASTRUCTURE AS CODE
  provision.sh            → create cloud resources via CLI
  terraform.sh            → wrapper for terraform with env handling
  k8s-deploy.sh           → kubectl apply with environment selection

BLOCKCHAIN DEVELOPMENT
  deploy-contract.sh      → forge build + deploy + verify
  fund-testnet.sh         → request testnet ETH from faucet
  run-node.sh             → start a local hardhat/anvil node
```

*Figure 13.3 — Scripts are the connective tissue of every automated system. Everything in DevOps, CI/CD, and infrastructure runs on them.*

---

### 📘 Ebook Explainer — Diversity of Scripting Applications

**The same scripting skills applied across 8 domains:**

| Domain | Script examples | Core skill used |
|---|---|---|
| **Web Dev** | `deploy.sh`, `build.sh`, `reset-db.sh` | Sequencing commands reliably |
| **Data Science** | `download-dataset.sh`, `preprocess.sh` | Chaining python + bash steps |
| **AI/ML** | `train.sh --epochs 50 --lr 0.001` | Parameterized execution |
| **Blockchain** | `deploy-contract.sh mainnet`, `fund-wallets.sh` | Conditional logic + env vars |
| **DevOps** | `provision.sh`, `scale.sh`, `backup.sh` | Error handling + logging |
| **Security** | `audit.sh`, `rotate-keys.sh`, `scan.sh` | Retry logic + validation |
| **Robotics** | `start-ros.sh`, `calibrate-sensors.sh` | Startup sequencing |
| **Education** | `setup-student-env.sh`, `grade.sh` | Idempotency + setup |

**The meta-skill:** Once you know how to write a reliable script in one domain, you can write reliable scripts in any domain. The bash patterns don't change — only the commands inside them do.

*Figure 13.4 — Shell scripting is domain-agnostic automation. The syntax is universal; the application is infinite.*

---

### 🎧 Audiobook Explainer

> *[EXPLAINER TONE — measured, 3 minutes]*
>
> "Chapter 13. How Shell Scripts Work. When to Write One. Where They Run.
>
> A shell script is not a compiled program — it's a recipe the shell reads line by line. When you run a script, bash opens the file, parses each line, and executes it as if you had typed it yourself. The shebang on line one tells the kernel which interpreter to use. `set -euo pipefail` on line two is your safety net — without it, a failing command doesn't stop the script. With it, the script stops at the first sign of trouble.
>
> The decision to write a script has a simple test: will this happen again? If a task is worth doing twice, it's worth automating. If it has more than one step, it's worth scripting. If it needs to run without you, it must be a script.
>
> Scripts run everywhere that bash runs. CI/CD pipelines are lists of scripts. Cron jobs are scripts on timers. Deployment tools call scripts. System startup runs scripts. GitHub Actions, GitLab CI, Kubernetes operators — all of them execute shell commands in controlled environments.
>
> And the diversity of application is the real story. You write a deploy script for a web server and a test script for a data pipeline and a provisioning script for cloud infrastructure — and the underlying pattern is the same. Argument parsing. Error handling. Logging. Retry logic. Idempotency. These patterns transfer completely between domains. Learn them once in bash, apply them everywhere."
>
> *[EXPLAINER TONE OUT]*

---

### 🎬 Video Explainer — Scripts in 5 Real Environments (5 Minutes)

**Minute 1 — CI/CD Pipeline:**
> GitHub Actions YAML file shown. Each `run:` block is a shell command. `bash -x test.sh` in CI output — debug mode shows every line before it runs. "Every CI/CD job is your scripts, running on their machines."

**Minute 2 — Database Backup Cron:**
> `crontab -l` — backup script scheduled at 2AM. Skip to next morning: `ls ~/backups/` — timestamped archive from 2AM exists. "It ran while you slept. That's automation."

**Minute 3 — Onboarding Script:**
> Fresh machine. `./setup.sh` — packages install, dotfiles link, SSH key generates, repo clones. Done in 2 minutes. "One command. New developer is productive. No manual steps, no missed steps."

**Minute 4 — Smart Contract Deployment:**
> `./deploy-contract.sh anvil ERC20` — forge builds, deploys to local Anvil node, prints contract address. "Environment-parameterized deployment. Change `anvil` to `mainnet` and it deploys to production."

**Minute 5 — The Universal Pattern:**
> Open `script-template.sh` from DFY Lesson 1. Show the sections. Voice-over: "This template works for every use case in the four minutes before this one. Same structure. Different commands inside."

---

> 🎯 **Use Cases Summary — B-004**
>
> Shell scripting from this book applies to:
> - ✅ Every CI/CD pipeline you'll ever build (GitHub Actions, GitLab, Jenkins)
> - ✅ Every deployment you'll ever automate
> - ✅ Every scheduled task (cron, systemd timers)
> - ✅ Every new machine or environment setup
> - ✅ Every multi-step workflow that needs to be reproducible
> - ✅ Every production process that must run without human intervention
>
> **A script is the lowest-cost automation that delivers the highest-value reliability.**

---

## Appendix C: AI Copilot — Script Builder

> *"The scripting copilot is your pair programmer for automation. It reviews your logic, catches your edge cases, and tells you when your script is ready for production."*

---

### Section 1 — Copilot Identity & System Prompt

**Copilot ID:** `B-004-COPILOT`
**Domain:** Bash Shell Scripting — Automation, Reliability, Production Patterns
**Level:** Beginner-to-Intermediate
**Credential Gate:** `CLL-L0-B004-ScriptBuilder`
**Prerequisite:** `CLL-L0-B003-FilesystemNavigator`

**Copy this system prompt into any AI assistant:**

```
You are lippytmai — AI Copilot for B-004 "The Script That Did My Job"
Domain: Bash shell scripting — automation, argument handling, error management, 
        deployment, CI/CD integration
Level: Beginner-to-intermediate — user has terminal, command, and filesystem skills
Credential this book unlocks: CLL-L0-B004-ScriptBuilder

WHAT THE USER HAS COVERED:
- Shebang line and script execution: ./script.sh, source, bash -x, bash -n
- set -euo pipefail — why it's mandatory and what each flag does
- Argument handling: $1, $@, getopts, shift
- Functions: local variables, return codes, subshell vs current shell
- Conditionals: [[ ]], case statements, string/number/file tests
- Loops: for, while, until — iterating files, arrays, ranges
- Here-docs and here-strings
- Error handling: trap, ERR signal, cleanup functions
- 10 DFY builds: script-template.sh, backup.sh, colors.sh library,
  selftest.sh pre-flight check, parse-config.sh, progress bar function,
  retry() wrapper, run_logged() output logger, env-switch.sh, menu.sh

CORE BEHAVIOR:
- Always start with script-template.sh as the scaffold — never from scratch
- When reviewing a script: check for set -euo pipefail first
- When debugging: ask for the exact error output AND run with bash -x if unclear
- For every script: ask "What happens when the input is empty? When the file doesn't exist?"
- Always show the failure mode before the happy path
- End responses with code with: "What did you get when you ran this?"

TEACHING MODES:
  TEACH:  Explain bash internals — subshells, process substitution, trap, IFS
  BUILD:  Pair-program any script from template through working implementation
  DEBUG:  Diagnose script failures — trace with bash -x, interpret error output
  DEPLOY: Package scripts for cron, systemd, CI/CD, Docker, remote servers
  EXTEND: Show how bash scripts become the foundation of deployment pipelines

GUARDRAILS:
- Always include set -euo pipefail in every script you write
- Never generate a script that could delete data without explicit confirmation
- If the user needs Python instead of bash → identify when complexity warrants it
- Always show the cleanup trap pattern for scripts that create temp files
```

---

### Section 2 — Prompt Library (30 Curated Prompts)

**🔵 Stage 1 — UNDERSTAND**

```
1. Explain set -euo pipefail line by line. What does each flag actually prevent?

2. What's the difference between running a script with ./ vs source vs bash? 
   When does each matter?

3. Why do local variables in functions matter? What happens without them?

4. What's the trap command for? Show me the cleanup pattern for temp files.

5. When should I write a bash script vs a Python script? 
   What's the decision boundary?

6. What does $@ vs $* vs $# mean? When do I use each?
```

**🟢 Stage 2 — BUILD**

```
7. Help me build a deployment script for my project that: pulls latest git, 
   installs dependencies, runs tests, and restarts the service only if tests pass.

8. Build backup.sh from DFY Lesson 2 — timestamped backup with log and 
   7-backup rotation. Walk me through each section.

9. I need a script that processes every .csv file in a directory, 
   extracts column 3, and writes a summary report. Build it step by step.

10. Help me build the env-switch.sh from DFY Lesson 9 — load named environment 
    profiles from ~/.envs/ directory.

11. Build me a pre-flight check script that verifies my production server has 
    all required tools, ports, and permissions before deploying.

12. I want a script that monitors a log file and sends a message if it sees 
    "ERROR" more than 5 times in 60 seconds. Build it.
```

**🔴 Stage 3 — DEBUG**

```
13. My script exits with no error message but doesn't do what it should. 
    How do I debug it? It starts with: [paste first 20 lines]

14. I get "unbound variable" error in my script. Here's the line: [paste]
    I thought I set it. What's happening?

15. My trap isn't cleaning up my temp files. Here's my trap setup: [paste]
    What did I miss?

16. My script works when I run it but fails in cron. Same script, same user. 
    What are the usual causes?

17. getopts isn't parsing my flags correctly. Here's my usage: [paste]
    The flags work individually but not combined.

18. My script ran but deleted files I didn't want deleted. 
    Here's the relevant section: [paste]. Help me add safeguards.
```

**🟡 Stage 4 — DEPLOY**

```
19. My backup.sh works locally. How do I deploy it to run at 2AM daily 
    on a remote server — including the cron setup and log rotation?

20. How do I package my script as a systemd service so it restarts 
    automatically if it crashes?

21. How do I add my deploy.sh to GitHub Actions so it runs automatically 
    on every push to main?

22. I want to run my script inside Docker — with access to the host filesystem 
    but isolated from everything else. How?

23. How do I make my script accept environment variables from a .env file 
    without hard-coding credentials?

24. How do I create a bash script that works on both Arch Linux (pacman) 
    and Ubuntu (apt) without separate scripts?
```

**🟣 Stage 5 — EXTEND**

```
25. What makes a bash script production-quality? Give me the checklist.

26. How do real DevOps engineers structure their script repositories? 
    What does a mature scripts/ directory look like?

27. When does a bash script need to become a Python program? 
    Show me where the line is.

28. How do CI/CD pipelines like GitHub Actions use shell scripts? 
    What patterns do they rely on?

29. How do blockchain deployment scripts work? What does a hardhat deploy 
    script look like and how does bash orchestrate it?

30. What's the gap between my scripts now and infrastructure-as-code tools 
    like Ansible and Terraform? How do I think about the progression?
```

---

### Section 2b — Audiobook Copilot (🎧 Format)

```
AUDIOBOOK COPILOT SYSTEM PROMPT:
"You are lippytmai, audiobook copilot for B-004. The listener is learning
bash scripting via audio while following along in their editor. Keep all
responses speakable. Narrate code logic verbally — what each section 
intends, not the syntax characters."
```

**15 Audiobook Prompts:**

```
WHILE LISTENING:

A1. "The audiobook mentioned 'set -euo pipefail'. Explain what would 
    go wrong without it using a real disaster scenario."

A2. "Explain getopts in plain English — what problem does it solve 
    and what's the alternative?"

A3. "I heard 'trap' mentioned. What is it and what analogy helps 
    me remember when to use it?"

A4. "Explain the difference between running a script and sourcing it 
    using a door vs walking into a room analogy."

A5. "What is idempotency? Give me a real-world analogy I'll remember."

PAUSE AND BUILD:

A6. "Walk me through backup.sh verbally — each section's purpose 
    before I type a single character."

A7. "Narrate the retry() function logic — attempt, failure, backoff, 
    retry — like a persistence story."

A8. "Walk me through the selftest.sh pre-flight pattern — why each 
    check exists and what happens without it."

A9. "Narrate the env-switch.sh concept — what a named environment 
    profile is and why I'd want multiple."

A10. "Read the colors.sh library purpose — what 5 output states does 
     it handle and why each matters."

RESUME CHECK:

A11. "Quiz me: I'll describe a script failure, you tell me which 
     set flag would have caught it. Three scenarios."

A12. "What makes a script 'production-quality'? Give me the list 
     in spoken sentences I can recite."

A13. "Before I resume: explain the difference between $@ and $* — 
     when does it matter which one I use?"

A14. "Summarize the automation decision framework — when to write a 
     script — in 30 spoken seconds."

A15. "Narrate my CLL-L0-B004-ScriptBuilder credential ceremony."
```

---

### Section 2c — Video Copilot (🎬 Format)

```
VIDEO COPILOT SYSTEM PROMPT:
"You are lippytmai, video copilot for B-004. The learner is watching
bash scripts being written and run on screen. Prioritize: what each
code block does visually, how to use bash -x to trace execution,
and SHOW→BUILD→VERIFY for every script build."
```

**15 Video Prompts:**

```
BEFORE PLAYING:

V1. "I'm about to watch the backup.sh video. What directories 
    should I create first so I can test safely?"

V2. "The video builds the retry() function. What behavior should 
    I create to test it — a command that fails a predictable way?"

V3. "I'm following the env-switch video. Set up my ~/.envs/ directory 
    with a dev and prod profile before I press play."

PAUSED:

V4. "The video shows bash -x output. Walk me through reading the 
    trace — what does + mean? What does ++ mean?"

V5. "Paused: the script is failing silently. The video uses bash -x 
    to find it. What am I looking for in the trace output?"

V6. "The colors.sh library is being sourced. What should I see 
    on screen after running `source ~/lib/colors.sh`?"

V7. "The video shows the trap ERR pattern. Pause — explain what 
    happens on screen when the trap fires."

V8. "The menu.sh is running. The selection isn't working. 
    What does the read -rp line look like when it's broken vs correct?"

VERIFY:

V9. "I built backup.sh. What are the 4 verification commands 
    that prove it works correctly — before I add it to cron?"

V10. "The retry() function is installed. Build me a test scenario 
     that exercises the exponential backoff."

V11. "setup-machine.sh ran on my machine. What does a successful 
     second run look like — all steps should be idempotent."

V12. "I ran run_logged() on a script. What does the log file look 
     like for a successful run vs a failed run?"

EXTEND:

V13. "The scripting videos covered bash. When does a bash script 
     need to become a Python script? Show me the tipping point."

V14. "I've completed all B-004 videos. What shell feature would 
     make my scripts 10x more powerful that we didn't cover?"

V15. "Show me what a production deploy.sh from a real open-source 
     project looks like — what patterns does it use?"
```

---

### Section 3 — Deployment Companion

| Artifact | Local | Remote server | Docker | GitHub | CI/CD |
|---|---|---|---|---|---|
| `backup.sh` | cron `0 2 * * *` | scp + remote cron | `cron.d/` + volume mount | scripts/ repo | Scheduled GH Actions workflow |
| `run_logged()` | Source in `.bashrc` | dotfiles deploy | Add to base image | dotfiles | Wrap CI commands |
| `retry()` | Source in `.bashrc` | dotfiles deploy | Source in build scripts | dotfiles | Use in CI steps for flaky commands |
| `env-switch.sh` | `switch_env dev` | Deploy `~/.envs/` via scp | `--env-file .env.prod` flag | `.envs/` in private repo | GitHub Actions secrets → .env |
| `menu.sh` | `chmod +x ~/bin/menu.sh` | SSH interactive use | N/A | scripts/ | N/A (interactive) |
| `selftest.sh` | Run before each deploy | Run on server via SSH | Add to HEALTHCHECK in Dockerfile | scripts/check.sh | CI: first step before build |

**Complete CI/CD pipeline from one script:**
```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Pre-flight check
        run: bash scripts/selftest.sh
        
      - name: Run tests
        run: bash scripts/test.sh
        
      - name: Deploy (with retry)
        run: |
          source scripts/retry.sh
          retry bash scripts/deploy.sh
          
      - name: Verify deployment
        run: bash scripts/health-check.sh
```

---

### Section 4 — ACSS Integration

```
B-004-COPILOT
    ├── Prerequisite: CLL-L0-B003-FilesystemNavigator
    ├── Hermes topic: b004.copilot
    ├── Fabric node prefix: B004
    │   → script patterns → reusable snippet library
    │   → deployment patterns → CI/CD pattern database
    │   → script errors → pre-flight check improvement loop
    └── Unlocks: B-005-COPILOT on credential earn
```

**Credential ceremony prompt:**
```
I've completed B-004. My DFY builds:
- script-template.sh (production-ready bash scaffold)
- backup.sh (timestamped + rotation + cron)
- ~/lib/colors.sh (color output library)
- selftest.sh (pre-flight dependency checker)
- parse-config.sh (key=value config loader)
- progress_bar() function
- retry() with exponential backoff
- run_logged() output logger
- env-switch.sh (named environment profiles)
- menu.sh (interactive script launcher)

Ready to claim CLL-L0-B004-ScriptBuilder.
```

---

## Further Reading

- 📄 [`docs/B-003-the-file-that-remembered-everything.md`](B-003-the-file-that-remembered-everything.md) — Permissions used in this script
- 📄 [`docs/linux-blockchain-educational-ecosystem.md`](linux-blockchain-educational-ecosystem.md) — Full Linux curriculum
- 📄 [`docs/autonomous-continuous-development.md`](autonomous-continuous-development.md) — How scripts become CI/CD pipelines
- 🏠 [`README.md`](../README.md) — Encyclopedia home

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

## Further Reading

- 📄 [`docs/B-003-the-file-that-remembered-everything.md`](B-003-the-file-that-remembered-everything.md) — Permissions used in this script
- 📄 [`docs/linux-blockchain-educational-ecosystem.md`](linux-blockchain-educational-ecosystem.md) — Full Linux curriculum
- 📄 [`docs/autonomous-continuous-development.md`](autonomous-continuous-development.md) — How scripts become CI/CD pipelines
- 🏠 [`README.md`](../README.md) — Encyclopedia home

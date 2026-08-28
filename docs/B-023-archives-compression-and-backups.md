# B-023: Archives, Compression, and Backups

### The Art of Preserving What Matters — tar, gzip, rsync, and Automated Snapshots

> *"Every piece of work you never backed up is a single disk failure away from being lost forever. Every piece of work you did back up is immortal. Learn tar and rsync once. Use them forever."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Create and extract archives with `tar`, `gzip`, `bzip2`, `xz`, and `zip`
2. Understand the difference between archiving and compression
3. Use `rsync` to create efficient incremental backups
4. Build an automated backup system using cron (B-014)
5. Restore from backups confidently and systematically

**Prerequisite:** B-001 through B-022

**Build Artifact:** `~/scripts/backup-system.sh` — automated incremental backup with retention policy

**Credential:** `CLL-L1-B023-BackupEngineer` — on-chain on Base

---

## Chapter 1: Archiving vs. Compression

These are two different operations often combined:

| Concept | What It Does | Tool |
|---|---|---|
| **Archiving** | Combines multiple files/dirs into one file | `tar` |
| **Compression** | Reduces file size by encoding redundancy | `gzip`, `bzip2`, `xz`, `zstd` |
| **Both at once** | Create a compressed archive | `tar -czf`, `tar -cjf`, `tar -cJf` |

```bash
# Archive only (no compression) — .tar
tar -cf archive.tar directory/

# Archive + gzip compression — .tar.gz or .tgz (fastest)
tar -czf archive.tar.gz directory/

# Archive + bzip2 compression — .tar.bz2 (smaller, slower)
tar -cjf archive.tar.bz2 directory/

# Archive + xz compression — .tar.xz (smallest, slowest)
tar -cJf archive.tar.xz directory/
```

---

## Chapter 2: tar — The Universal Archiver

```bash
# tar flag memory aid:
# c = create, x = extract, t = list (table), f = filename
# z = gzip, j = bzip2, J = xz, v = verbose

# CREATE archives:
tar -czf backup.tar.gz ~/developer-workspace/
tar -czf logs-2026-08.tar.gz /var/log/ --exclude="*.gz"

# EXTRACT archives:
tar -xzf backup.tar.gz                    # extract here
tar -xzf backup.tar.gz -C /tmp/restore/   # extract to specific dir
tar -xzf backup.tar.gz --strip-components=1  # skip top directory

# LIST contents without extracting:
tar -tzf backup.tar.gz
tar -tzf backup.tar.gz | grep ".sh"

# APPEND to an existing (uncompressed) archive:
tar -rf archive.tar newfile.txt

# Extract a single file:
tar -xzf backup.tar.gz developer-workspace/scripts/filesystem-navigator.sh
```

---

## Chapter 3: gzip, bzip2, xz — Standalone Compression

```bash
# gzip — compress single files (replaces original by default)
gzip logfile.txt          # creates logfile.txt.gz, removes logfile.txt
gzip -k logfile.txt       # keep original with -k
gunzip logfile.txt.gz     # decompress

# Check compression ratio
gzip -l archive.tar.gz

# bzip2 — better compression than gzip, slower
bzip2 bigfile.tar         # creates bigfile.tar.bz2
bunzip2 bigfile.tar.bz2

# xz — best compression, slowest
xz -z database-dump.sql   # compress
xz -d database-dump.sql.xz # decompress

# zstd — modern: fast AND good compression (install: apt install zstd)
zstd logfile.txt          # creates logfile.txt.zst
zstd -d logfile.txt.zst

# Compression comparison:
# Speed: gzip > zstd > bzip2 > xz
# Size:  xz < bzip2 < zstd < gzip
```

---

## Chapter 4: zip and unzip

```bash
# zip is cross-platform (Windows-friendly)
zip -r project.zip ~/developer-workspace/projects/my-app/
zip -r project.zip ~/projects/ -x "*/node_modules/*"  # exclude node_modules

# Unzip
unzip project.zip
unzip project.zip -d /tmp/project-restore/  # to specific dir
unzip -l project.zip                         # list without extracting
unzip -p project.zip README.md              # extract to stdout
```

---

## Chapter 5: rsync — The Incremental Backup Powerhouse

`rsync` only transfers changed files — making it ideal for backups:

```bash
# rsync flag memory aid:
# -a = archive mode (preserves permissions, timestamps, symlinks, etc.)
# -v = verbose
# -z = compress during transfer
# -P = show progress + allow partial transfers
# --delete = delete files in destination that don't exist in source

# Local backup
rsync -av ~/developer-workspace/ ~/backups/developer-workspace/

# Backup to external drive
rsync -av --progress ~/developer-workspace/ /media/backup-drive/workspace/

# Backup to remote server via SSH
rsync -avz -e ssh ~/developer-workspace/ charles@backup-server:~/backups/workspace/

# Mirror (exact copy — deletes removed files in destination)
rsync -av --delete ~/developer-workspace/ ~/backups/developer-workspace/

# Dry run (see what WOULD happen without doing it)
rsync -av --dry-run ~/developer-workspace/ ~/backups/developer-workspace/

# Exclude patterns
rsync -av \
  --exclude='.git' \
  --exclude='node_modules' \
  --exclude='*.log' \
  ~/developer-workspace/ ~/backups/workspace/
```

---

## Chapter 6: The Build — Automated Backup System

```bash
#!/bin/bash
# backup-system.sh — B-023 Build Artifact
# Automated backup with timestamped snapshots and retention policy
set -euo pipefail

# === Configuration ===
BACKUP_SOURCE="$HOME/developer-workspace"
BACKUP_DEST="$HOME/backups"
RETENTION_DAYS=30
LOG_FILE="$HOME/developer-workspace/logs/backup.log"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
SNAPSHOT_NAME="workspace-${TIMESTAMP}"

# === Create backup directory ===
mkdir -p "$BACKUP_DEST/snapshots" "$BACKUP_DEST/latest"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log "=== Backup Started ==="
log "Source: $BACKUP_SOURCE"
log "Destination: $BACKUP_DEST"

# === Step 1: rsync to latest/ (incremental mirror) ===
log "Running rsync to latest/..."
rsync -av --delete \
    --exclude='.git' \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='node_modules' \
    "$BACKUP_SOURCE/" "$BACKUP_DEST/latest/" \
    >> "$LOG_FILE" 2>&1

log "rsync complete."

# === Step 2: Create timestamped snapshot archive ===
log "Creating snapshot: $SNAPSHOT_NAME.tar.gz"
tar -czf "$BACKUP_DEST/snapshots/${SNAPSHOT_NAME}.tar.gz" \
    -C "$BACKUP_DEST" latest/ \
    >> "$LOG_FILE" 2>&1

log "Snapshot created: $(du -sh "$BACKUP_DEST/snapshots/${SNAPSHOT_NAME}.tar.gz" | cut -f1)"

# === Step 3: Retention — remove snapshots older than N days ===
log "Cleaning snapshots older than ${RETENTION_DAYS} days..."
find "$BACKUP_DEST/snapshots/" -name "workspace-*.tar.gz" \
    -mtime +"$RETENTION_DAYS" -delete \
    >> "$LOG_FILE" 2>&1

SNAPSHOT_COUNT=$(ls "$BACKUP_DEST/snapshots/" | wc -l)
log "Snapshots retained: $SNAPSHOT_COUNT"

# === Step 4: Summary ===
TOTAL_SIZE=$(du -sh "$BACKUP_DEST" 2>/dev/null | cut -f1)
log "Total backup size: $TOTAL_SIZE"
log "=== Backup Complete ==="

echo ""
echo "✅ Backup complete! Snapshot: $SNAPSHOT_NAME"
echo "   Size: $TOTAL_SIZE | Log: $LOG_FILE"
```

```bash
chmod +x ~/scripts/backup-system.sh

# Test it
~/scripts/backup-system.sh

# Schedule with cron (B-014) — run at 2 AM daily
crontab -e
# Add: 0 2 * * * /home/charles/scripts/backup-system.sh >> /home/charles/developer-workspace/logs/cron-backup.log 2>&1
```

---

## Chapter 7: Restoring from Backup

```bash
# List available snapshots
ls -lh ~/backups/snapshots/

# Preview contents of a snapshot
tar -tzf ~/backups/snapshots/workspace-20260828-020000.tar.gz | head -20

# Restore to a test directory
mkdir -p /tmp/restore-test
tar -xzf ~/backups/snapshots/workspace-20260828-020000.tar.gz -C /tmp/restore-test/

# Compare restored vs current
diff -r ~/developer-workspace/ /tmp/restore-test/latest/ 2>/dev/null | head -20

# Restore specific file
tar -xzf ~/backups/snapshots/workspace-20260828-020000.tar.gz \
    -C /tmp/ \
    latest/scripts/filesystem-navigator.sh
```

---

## Chapter 8: Proof of Work

```bash
echo "=== B-023 Verification ==="
echo "Creating test archive..."
tar -czf /tmp/test-b023.tar.gz ~/scripts/ 2>/dev/null
echo "Archive size: $(du -sh /tmp/test-b023.tar.gz | cut -f1)"

echo ""
echo "Listing archive contents:"
tar -tzf /tmp/test-b023.tar.gz | head -5

echo ""
echo "Running backup system:"
~/scripts/backup-system.sh | tail -5

echo ""
echo "Backup snapshots:"
ls ~/backups/snapshots/ | tail -3
```

---

## Further Reading

- 📄 [`docs/B-014-the-scheduler-that-never-forgets.md`](B-014-the-scheduler-that-never-forgets.md) — Scheduling backups with cron
- 📄 [`docs/B-018-the-log-that-tells-the-truth.md`](B-018-the-log-that-tells-the-truth.md) — Backing up log files
- 📄 [`docs/B-021-the-linux-filesystem-explained.md`](B-021-the-linux-filesystem-explained.md) — Understanding /var and where data lives
- 🏠 [`README.md`](../README.md) — Encyclopedia home

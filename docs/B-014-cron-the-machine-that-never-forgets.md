# B-014: Cron — The Machine That Never Forgets

### Automated, Scheduled Tasks in Linux

> *"A cron job is a loyal machine that wakes up at exactly the same time every day, every hour, every minute — and does exactly what you told it. It doesn't forget, it doesn't get lazy, it doesn't call in sick. Automating the repetitive frees you to build the important."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Explain what cron is and how the cron daemon works
2. Read and write crontab syntax for any scheduling pattern
3. Create and manage cron jobs with `crontab -e`
4. Handle cron output and logging correctly
5. Choose between cron and systemd timers for scheduled tasks

**Prerequisite:** B-001 through B-013

**Build Artifact:** A crontab with three scheduled jobs: daily database backup, hourly health check, weekly cleanup — all with logging

**Credential:** `CLL-L1-B014-CronOperator` — on-chain on Base

---

## Chapter 1: How Cron Works

Cron is a **daemon** (`crond`) that wakes up every minute and checks a set of scheduling tables (crontabs). For each job whose schedule matches the current time, cron launches the command.

```
System boot
    └── crond starts (systemd: crond.service)
            └── Every minute:
                    ├── Read /etc/crontab (system-wide jobs)
                    ├── Read /etc/cron.d/ (drop-in files)
                    ├── Read /var/spool/cron/crontabs/ (per-user)
                    └── Run matching jobs
```

*[Reality — cron has been part of Unix since the 1970s and remains the most widely-used job scheduler on Linux servers]*

---

## Chapter 2: Crontab Syntax

Every cron job is one line: **schedule** + **command**.

```
# ┌───────── minute (0-59)
# │ ┌─────── hour (0-23)
# │ │ ┌───── day of month (1-31)
# │ │ │ ┌─── month (1-12)
# │ │ │ │ ┌─ day of week (0-7, both 0 and 7 = Sunday)
# │ │ │ │ │
# * * * * *  command to run
```

### Common Patterns

| Schedule | Crontab | Plain English |
|---|---|---|
| Every minute | `* * * * *` | Every single minute |
| Every 5 minutes | `*/5 * * * *` | Every 5 minutes |
| Every hour | `0 * * * *` | Top of every hour |
| Every day at midnight | `0 0 * * *` | Daily at 00:00 |
| Every day at 3 AM | `0 3 * * *` | Daily at 03:00 |
| Every Monday at 9 AM | `0 9 * * 1` | Weekly Monday morning |
| First of each month | `0 0 1 * *` | Monthly at midnight |
| Every 30 min, 8–18 | `*/30 8-18 * * *` | Working hours only |

```bash
# Quick reference
@reboot   # once after reboot
@daily    # equivalent to "0 0 * * *"
@weekly   # equivalent to "0 0 * * 0"
@monthly  # equivalent to "0 0 1 * *"
@hourly   # equivalent to "0 * * * *"
```

---

## Chapter 3: Managing Crontabs

```bash
# Open your personal crontab in $EDITOR
crontab -e

# List your current crontab
crontab -l

# Remove your crontab (WARNING: irreversible)
crontab -r

# View system crontab
cat /etc/crontab

# View system cron.d drop-ins
ls /etc/cron.d/

# Check if cron is running
systemctl status cron         # Ubuntu/Debian
systemctl status cronie       # Arch/RHEL

# View cron logs
grep CRON /var/log/syslog     # Ubuntu
journalctl -u cron            # systemd
```

---

## Chapter 4: Output and Logging

Cron runs commands in a minimal environment — it emails output to your local user by default. Redirect output properly:

```bash
# In your crontab:

# Discard all output (bad — you'll miss errors)
0 3 * * * /home/charles/backup.sh > /dev/null 2>&1

# Append stdout and stderr to a log file (recommended)
0 3 * * * /home/charles/backup.sh >> /home/charles/logs/backup.log 2>&1

# Log with timestamp
0 3 * * * date "+%Y-%m-%d %H:%M:%S" >> /home/charles/logs/backup.log && \
         /home/charles/backup.sh >> /home/charles/logs/backup.log 2>&1

# Disable email output for all jobs (first line of crontab)
MAILTO=""
```

---

## Chapter 5: Cron Environment Gotchas

Cron runs in a stripped-down environment. Common pitfalls:

```bash
# In your crontab — always set these:
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin:/home/charles/.local/bin
MAILTO=""

# BAD: uses 'python3' but cron's PATH doesn't include it
0 3 * * * python3 /home/charles/backup.py

# GOOD: use full path
0 3 * * * /usr/bin/python3 /home/charles/backup.py

# GOOD: source venv then run
0 3 * * * source /home/charles/venv/bin/activate && python3 backup.py

# GOOD: use absolute path for the script itself
0 3 * * * /home/charles/scripts/backup.sh

# GOOD: run with full environment from profile
0 3 * * * bash -l -c '/home/charles/scripts/backup.sh'
```

---

## Chapter 6: The Build — Three Scheduled Jobs

```bash
# --- Three scripts to create ---

# 1. Daily database backup at 3 AM
cat > ~/scripts/cron-db-backup.sh << 'SCRIPT'
#!/bin/bash
set -euo pipefail
LOG="/home/charles/logs/cron-db-backup.log"
DATE=$(date '+%Y-%m-%d')
BACKUP_DIR="/home/charles/backups/db"
mkdir -p "$BACKUP_DIR"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting DB backup" >> "$LOG"
docker exec project-alpha-db pg_dump -U postgres devdb | \
    gzip > "$BACKUP_DIR/devdb-${DATE}.sql.gz"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] DB backup complete: devdb-${DATE}.sql.gz" >> "$LOG"
# Keep only last 30 days
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +30 -delete
SCRIPT

# 2. Hourly health check
cat > ~/scripts/cron-health-check.sh << 'SCRIPT'
#!/bin/bash
LOG="/home/charles/logs/cron-health.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
STATUS="OK"
docker ps | grep -q "project-alpha-app" || STATUS="APP_DOWN"
docker ps | grep -q "project-alpha-db" || STATUS="DB_DOWN"
echo "[$TIMESTAMP] status=$STATUS" >> "$LOG"
SCRIPT

# 3. Weekly cleanup on Sunday at 1 AM
cat > ~/scripts/cron-weekly-cleanup.sh << 'SCRIPT'
#!/bin/bash
LOG="/home/charles/logs/cron-cleanup.log"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Weekly cleanup starting" >> "$LOG"
find /home/charles/logs -name "*.log" -mtime +90 -delete
find /tmp -name "*.tmp" -mtime +7 -delete 2>/dev/null || true
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Weekly cleanup complete" >> "$LOG"
SCRIPT

chmod +x ~/scripts/cron-db-backup.sh ~/scripts/cron-health-check.sh ~/scripts/cron-weekly-cleanup.sh
mkdir -p ~/logs ~/backups/db

# Add all three to crontab
(crontab -l 2>/dev/null; cat << 'CRONTAB'
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
MAILTO=""

# Daily DB backup at 3 AM
0 3 * * * /home/charles/scripts/cron-db-backup.sh >> /home/charles/logs/cron-db-backup.log 2>&1

# Hourly health check
0 * * * * /home/charles/scripts/cron-health-check.sh >> /home/charles/logs/cron-health.log 2>&1

# Weekly cleanup Sunday 1 AM
0 1 * * 0 /home/charles/scripts/cron-weekly-cleanup.sh >> /home/charles/logs/cron-cleanup.log 2>&1
CRONTAB
) | crontab -

# Verify
crontab -l
```

---

## Chapter 7: Cron vs. systemd Timers

| Feature | Cron | systemd Timer |
|---|---|---|
| **Setup** | Simple one-liner | Service + Timer unit files |
| **Logging** | Manual (redirect to file) | Automatic (journald) |
| **Missed jobs** | Skipped silently | `Persistent=true` catches up |
| **Dependencies** | None | Full systemd dependency graph |
| **Environment** | Minimal (need to set PATH) | Full unit env support |
| **Best for** | Simple personal tasks | Production services |

Use cron for: personal scripts, simple automation, developer workstation tasks.  
Use systemd timers (B-010) for: production services, jobs that must not be missed, jobs with dependencies.

---

## Further Reading

- 📄 [`docs/B-010-the-service-that-started-itself.md`](B-010-the-service-that-started-itself.md) — systemd timer alternative
- 📄 [`docs/B-004-the-script-that-did-my-job.md`](B-004-the-script-that-did-my-job.md) — Bash scripts that cron runs
- 📄 [`docs/B-012-the-container-that-held-everything.md`](B-012-the-container-that-held-everything.md) — Docker containers cron backs up
- 🏠 [`README.md`](../README.md) — Encyclopedia home

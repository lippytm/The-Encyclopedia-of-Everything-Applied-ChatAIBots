# B-018: Log Files Tell the Truth

### Reading, Searching, and Analyzing System Logs

> *"Logs are the black box flight recorder of your system. When something goes wrong — a service crashes, a security incident happens, a database connection fails at 3 AM — logs are the only witness. Learning to read them is the difference between a developer who fixes bugs and one who guesses at them."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Locate and read the key Linux log files
2. Use `journalctl` to query systemd logs with filters
3. Search logs efficiently with `grep`, `tail -f`, and `less`
4. Set up `logrotate` to prevent logs from filling your disk
5. Write a log analysis script that extracts error patterns and sends an alert

**Prerequisite:** B-001 through B-017

**Build Artifact:** A `log-monitor.sh` script that tails multiple log files, filters for errors, counts occurrences by hour, and outputs a daily summary

**Credential:** `CLL-L1-B018-LogAnalyst` — on-chain on Base

---

## Chapter 1: Where Linux Keeps Its Logs

```
/var/log/
├── syslog          # General system messages (Ubuntu/Debian)
├── messages        # Same, on RHEL/Arch
├── auth.log        # Authentication events (logins, sudo, SSH)
├── kern.log        # Kernel messages
├── dmesg           # Boot-time hardware messages
├── apt/            # Package manager history
├── nginx/
│   ├── access.log  # Every HTTP request
│   └── error.log   # Nginx errors
├── postgresql/     # Database logs
└── journal/        # systemd journal (binary)
```

*[Reality — on systemd-based systems (Arch, Ubuntu 20.04+), most logs go through the journal daemon and can be read with `journalctl`]*

---

## Chapter 2: journalctl — systemd Log Query

```bash
# View all logs (newest last)
journalctl

# Show most recent logs first
journalctl -r

# Follow live (like tail -f)
journalctl -f

# Logs for a specific service
journalctl -u nginx
journalctl -u docker
journalctl -u sshd

# Logs since a specific time
journalctl --since "2026-08-28 00:00:00"
journalctl --since "1 hour ago"
journalctl --since today

# Logs for current boot only
journalctl -b

# Previous boot (useful after crashes)
journalctl -b -1

# Priority filtering
journalctl -p err          # errors and above
journalctl -p warning      # warnings and above

# Combine filters
journalctl -u nginx -p err --since today

# Show kernel messages
journalctl -k

# Export to file
journalctl --since today > today-logs.txt

# Disk usage
journalctl --disk-usage

# Vacuum (keep only last 100MB)
sudo journalctl --vacuum-size=100M
```

---

## Chapter 3: tail, less, and grep on Log Files

```bash
# Follow a log file in real time
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Show last 100 lines
tail -n 100 /var/log/syslog

# Follow multiple files simultaneously
tail -f /var/log/nginx/access.log /var/log/nginx/error.log

# Search with grep
grep "ERROR" /var/log/app.log
grep -i "error\|warning\|critical" /var/log/app.log
grep "2026-08-28" /var/log/app.log | grep "ERROR"

# Count error lines
grep -c "ERROR" /var/log/app.log

# Show context around matches (-A after, -B before, -C both)
grep -C 3 "FATAL" /var/log/app.log

# Navigate large files with less
less /var/log/syslog
# In less: / to search, n for next match, G for end, q to quit
```

---

## Chapter 4: logrotate — Preventing Disk Full

Log files grow forever if nothing rotates them. `logrotate` compresses and removes old logs automatically:

```bash
# View logrotate config
cat /etc/logrotate.conf
ls /etc/logrotate.d/

# Create a custom logrotate config
cat > /etc/logrotate.d/developer-workspace << 'EOF'
/home/charles/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 charles charles
    sharedscripts
    postrotate
        echo "$(date): Logs rotated" >> /home/charles/logs/rotation.log
    endscript
}
EOF

# Test logrotate (dry run)
sudo logrotate --debug /etc/logrotate.d/developer-workspace

# Force rotation now
sudo logrotate --force /etc/logrotate.d/developer-workspace
```

---

## Chapter 5: The Build — Log Monitor Script

```bash
#!/bin/bash
# log-monitor.sh — B-018 Build Artifact
# Monitors log files for error patterns and produces a daily summary
set -euo pipefail

LOG_SOURCES=(
    "/home/charles/logs/cron-db-backup.log"
    "/home/charles/logs/cron-health.log"
    "/tmp/b016-pipeline.log"
)
SUMMARY_FILE="/home/charles/logs/daily-summary-$(date +%Y%m%d).txt"
ERROR_PATTERNS="ERROR|FATAL|CRITICAL|FAILED|Exception|Traceback"

{
    echo "=============================="
    echo "  Daily Log Summary"
    echo "  $(date '+%Y-%m-%d %H:%M:%S')"
    echo "=============================="
    echo ""

    for log in "${LOG_SOURCES[@]}"; do
        if [ ! -f "$log" ]; then
            echo "[SKIP] $log — not found"
            continue
        fi

        echo "--- $(basename "$log") ---"
        echo "Total lines: $(wc -l < "$log")"

        error_count=$(grep -cEi "$ERROR_PATTERNS" "$log" 2>/dev/null || echo "0")
        echo "Error lines: $error_count"

        if [ "$error_count" -gt 0 ]; then
            echo "Recent errors:"
            grep -Ei "$ERROR_PATTERNS" "$log" | tail -5 | sed 's/^/  /'
        fi
        echo ""
    done

    echo "=============================="
    echo "  Journal: Last 10 system errors"
    echo "=============================="
    journalctl -p err --since "24 hours ago" --no-pager | tail -10
} > "$SUMMARY_FILE" 2>&1

cat "$SUMMARY_FILE"
echo ""
echo "Summary saved: $SUMMARY_FILE"
```

```bash
chmod +x ~/scripts/log-monitor.sh
~/scripts/log-monitor.sh
```

---

## Chapter 6: Proof of Work

```bash
echo "=== B-018 Verification ==="

echo "journalctl disk usage:"
journalctl --disk-usage

echo ""
echo "Today's system errors:"
journalctl -p err --since today --no-pager | wc -l

echo ""
echo "Log monitor run:"
~/scripts/log-monitor.sh
```

---

## Further Reading

- 📄 [`docs/B-010-the-service-that-started-itself.md`](B-010-the-service-that-started-itself.md) — systemd services generate the logs you'll monitor
- 📄 [`docs/B-016-pipes-redirects-and-composition.md`](B-016-pipes-redirects-and-composition.md) — Pipe log output through analysis tools
- 📄 [`docs/B-019-securing-your-linux-machine.md`](B-019-securing-your-linux-machine.md) — auth.log is your security audit trail
- 🏠 [`README.md`](../README.md) — Encyclopedia home

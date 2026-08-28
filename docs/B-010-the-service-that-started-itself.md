# B-010: The Service That Started Itself

### systemd — Linux Service Management, Autostart, and System Boot

> *"The difference between a script that runs once and a service that runs forever is systemd. Every production application — web servers, databases, blockchain nodes, AI inference servers — runs as a systemd service. This is the book where your code learns to start itself."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Understand what systemd is and how it manages Linux services
2. Start, stop, restart, enable, and disable services with `systemctl`
3. Read service logs with `journalctl`
4. Write a custom `.service` unit file to run your own script as a service
5. Create a service that runs your `backup.sh` automatically on a schedule

**Prerequisite:** B-001 through B-009

**Build Artifact:** A custom systemd service unit that runs `backup.sh` automatically and a systemd timer that schedules it nightly

**Credential:** `CLL-L1-B010-SystemdOperator` — on-chain on Base

---

## Chapter 1: What Is systemd?

When Linux boots, the kernel starts exactly one process: **PID 1**. On modern Linux systems, that's `systemd`. Everything else — every service, every daemon, every scheduled task — is managed by systemd.

```
Linux Kernel
    └── systemd (PID 1)
        ├── network.service
        ├── sshd.service
        ├── postgresql.service
        ├── docker.service
        └── your-app.service  ← you'll build this
```

systemd manages services using **unit files** — text configuration files that describe a service: what binary to run, when to start it, what to do if it crashes, and how it relates to other services.

*[Reality — systemd is the init system on Ubuntu, Debian, Arch, Fedora, RHEL, and most other major Linux distributions as of 2026]*

---

## Chapter 2: systemctl — The Control Interface

```bash
# Check the status of a service
systemctl status nginx
systemctl status sshd
systemctl status postgresql

# Start a service (runs it now, until next reboot)
sudo systemctl start nginx

# Stop a service
sudo systemctl stop nginx

# Restart a service (stop + start)
sudo systemctl restart nginx

# Reload config without stopping (if service supports it)
sudo systemctl reload nginx

# Enable a service (start automatically at boot)
sudo systemctl enable nginx

# Disable a service (don't start at boot)
sudo systemctl disable nginx

# Enable AND start immediately
sudo systemctl enable --now nginx

# Is it running?
systemctl is-active nginx

# Does it start at boot?
systemctl is-enabled nginx

# List all active services
systemctl list-units --type=service --state=active

# List all failed services
systemctl list-units --type=service --state=failed
```

*[Reality — the `status` command is the first thing to run when a service isn't working. Always check it before anything else.]*

---

## Chapter 3: journalctl — Reading Logs

systemd collects logs from all services in a central journal. `journalctl` is how you read it.

```bash
# Show all logs (most recent last)
journalctl

# Follow logs in real time (like tail -f)
journalctl -f

# Show logs for a specific service
journalctl -u nginx
journalctl -u sshd

# Follow a specific service's logs
journalctl -u nginx -f

# Show logs since a specific time
journalctl --since "2026-08-28 00:00:00"
journalctl --since "1 hour ago"
journalctl --since yesterday

# Show only errors and above
journalctl -p err

# Show the last 50 lines
journalctl -n 50

# Show logs for the current boot only
journalctl -b

# Show logs for the previous boot
journalctl -b -1
```

---

## Chapter 4: Writing a Service Unit File

A unit file is an INI-style configuration file with three sections:

```ini
[Unit]
Description=Human-readable name of the service
After=network.target    # start after network is up

[Service]
Type=simple             # or forking, oneshot, notify
User=charles            # run as this user
WorkingDirectory=/home/charles
ExecStart=/home/charles/backup.sh
Restart=on-failure      # restart if it crashes
RestartSec=10           # wait 10 seconds before restarting

[Install]
WantedBy=multi-user.target  # target that activates this service
```

### Service Types

| Type | When to Use |
|---|---|
| `simple` | Process stays in foreground (most scripts) |
| `forking` | Process forks itself to background (traditional daemons) |
| `oneshot` | Runs once and exits (scripts, one-time tasks) |
| `notify` | Process sends systemd a ready notification |

---

## Chapter 5: The Build — backup.service and backup.timer

### Part 1: The Service Unit

```bash
# Create the service file
sudo nano /etc/systemd/system/backup.service
```

```ini
[Unit]
Description=Developer Workspace Backup Service
Documentation=https://github.com/lippytm/The-Encyclopedia-of-Everything-Applied-ChatAIBots
After=local-fs.target

[Service]
Type=oneshot
User=charles
Group=charles
WorkingDirectory=/home/charles
ExecStart=/home/charles/backup.sh
StandardOutput=journal
StandardError=journal
SyslogIdentifier=backup

# Environment variables
Environment="LOG_FILE=/home/charles/developer-workspace/logs/backup.log"

[Install]
WantedBy=multi-user.target
```

```bash
# Test it immediately
sudo systemctl daemon-reload
sudo systemctl start backup.service
sudo systemctl status backup.service

# Check the logs
journalctl -u backup.service -n 20
```

### Part 2: The Timer Unit (Nightly at 2:00 AM)

```bash
sudo nano /etc/systemd/system/backup.timer
```

```ini
[Unit]
Description=Run Developer Workspace Backup nightly at 2:00 AM
Requires=backup.service

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true    # catch up on missed runs after system was off
Unit=backup.service

[Install]
WantedBy=timers.target
```

```bash
# Enable and start the timer
sudo systemctl daemon-reload
sudo systemctl enable --now backup.timer

# Verify the timer is scheduled
systemctl list-timers
# backup.timer should appear with next run time

# List all timers
systemctl list-timers --all
```

*[Reality — `Persistent=true` means if the machine was off at 2:00 AM, the backup will run the next time it boots up — important for laptops]*

---

## Chapter 6: User Services (No sudo Required)

For personal scripts that don't need system-level access, use user-level systemd services:

```bash
# User services live here (create if needed)
mkdir -p ~/.config/systemd/user/

# Create a user service
cat > ~/.config/systemd/user/process-monitor.service << 'EOF'
[Unit]
Description=Process CPU Monitor (User Level)
After=default.target

[Service]
Type=oneshot
ExecStart=%h/process-monitor.sh
Environment="CPU_THRESHOLD=80"

[Install]
WantedBy=default.target
EOF

# Create a user timer
cat > ~/.config/systemd/user/process-monitor.timer << 'EOF'
[Unit]
Description=Run process monitor every 15 minutes

[Timer]
OnBootSec=5min
OnUnitActiveSec=15min
Unit=process-monitor.service

[Install]
WantedBy=timers.target
EOF

# Enable user timer (no sudo)
systemctl --user daemon-reload
systemctl --user enable --now process-monitor.timer
systemctl --user list-timers
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-010 Build Verification ==="

echo "backup.service status:"
sudo systemctl status backup.service --no-pager

echo ""
echo "backup.timer status:"
sudo systemctl status backup.timer --no-pager

echo ""
echo "Timer schedule:"
systemctl list-timers backup.timer

echo ""
echo "Service logs:"
journalctl -u backup.service -n 10 --no-pager
```

---

## Chapter 8: The Production Pattern

Now you have the complete pattern for running any program as a Linux service:

1. Write the script (`backup.sh`, `server.py`, `node-app.js`)
2. Create `/etc/systemd/system/<name>.service`
3. Create `/etc/systemd/system/<name>.timer` (if scheduled)
4. `sudo systemctl daemon-reload`
5. `sudo systemctl enable --now <name>.timer`
6. `journalctl -u <name> -f` to watch it run

This exact pattern runs PostgreSQL, Nginx, Docker, Ethereum nodes, and every production application on Linux. *[Reality — all listed services use systemd unit files on Linux production servers]*

---

## Chapter 9: Mutation

```bash
# MUTATION 1: View the actual unit file for an installed service
systemctl cat nginx
systemctl cat sshd

# MUTATION 2: See what services depend on each other
systemctl list-dependencies backup.service

# MUTATION 3: Override a service without editing the original unit file
sudo systemctl edit backup.service
# This creates /etc/systemd/system/backup.service.d/override.conf
# Add only the directives you want to change
```

---

## Further Reading

- 📄 [`docs/B-006-the-process-that-wouldnt-stop.md`](B-006-the-process-that-wouldnt-stop.md) — Process management (systemd manages processes)
- 📄 [`docs/autonomous-continuous-development.md`](autonomous-continuous-development.md) — ACD uses systemd-style service concepts
- 📄 [`docs/linux-blockchain-educational-ecosystem.md`](linux-blockchain-educational-ecosystem.md) — Blockchain nodes run as systemd services
- 🏠 [`README.md`](../README.md) — Encyclopedia home

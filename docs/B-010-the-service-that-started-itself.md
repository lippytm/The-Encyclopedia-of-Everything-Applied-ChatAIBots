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


---

## Chapter 12: Done-For-You Lessons — Service Manager

> *"The fastest way to learn is to build something real. These ten lessons give you exactly that — ten deployable tools, ready to use, built by your own hands."*

---

### DFY Lesson 1 — custom.service unit

> **What you're building:** Write a systemd unit file for any custom application

**📘 Ebook Figure**

```bash
# DFY-B-010-L01: custom.service unit
# Domain: Write a systemd unit file for any custom application
# Time to build: 15–25 minutes
# Credential: CLL-L0-B010-ServiceManager

# STEP 1: Create the script file
nano ~/custom.service unit.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/custom.service unit.sh

# STEP 4: Test it
~/custom.service unit.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 1: custom.service unit. Write a systemd unit file for any custom application. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep custom.s` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/custom.service unit && ~/custom.service unit` — it runs, it works

🤖 **Copilot Assist:** *"I built custom.service unit but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 2 — service-health.sh

> **What you're building:** Check status of multiple services in one report

**📘 Ebook Figure**

```bash
# DFY-B-010-L02: service-health.sh
# Domain: Check status of multiple services in one report
# Time to build: 15–25 minutes
# Credential: CLL-L0-B010-ServiceManager

# STEP 1: Create the script file
nano ~/service-health.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/service-health.sh.sh

# STEP 4: Test it
~/service-health.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 2: service-health.sh. Check status of multiple services in one report. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep service-` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/service-health.sh && ~/service-health.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built service-health.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 3 — systemd-timer-setup.sh

> **What you're building:** Create a systemd timer to replace a cron job

**📘 Ebook Figure**

```bash
# DFY-B-010-L03: systemd-timer-setup.sh
# Domain: Create a systemd timer to replace a cron job
# Time to build: 15–25 minutes
# Credential: CLL-L0-B010-ServiceManager

# STEP 1: Create the script file
nano ~/systemd-timer-setup.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/systemd-timer-setup.sh.sh

# STEP 4: Test it
~/systemd-timer-setup.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 3: systemd-timer-setup.sh. Create a systemd timer to replace a cron job. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep systemd-` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/systemd-timer-setup.sh && ~/systemd-timer-setup.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built systemd-timer-setup.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 4 — journal-analyzer.sh

> **What you're building:** Extract errors/warnings from journald in the last 24 hours

**📘 Ebook Figure**

```bash
# DFY-B-010-L04: journal-analyzer.sh
# Domain: Extract errors/warnings from journald in the last 24 hours
# Time to build: 15–25 minutes
# Credential: CLL-L0-B010-ServiceManager

# STEP 1: Create the script file
nano ~/journal-analyzer.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/journal-analyzer.sh.sh

# STEP 4: Test it
~/journal-analyzer.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 4: journal-analyzer.sh. Extract errors/warnings from journald in the last 24 hours. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep journal-` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/journal-analyzer.sh && ~/journal-analyzer.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built journal-analyzer.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 5 — auto-restart-service.sh

> **What you're building:** Configure automatic restart with exponential backoff

**📘 Ebook Figure**

```bash
# DFY-B-010-L05: auto-restart-service.sh
# Domain: Configure automatic restart with exponential backoff
# Time to build: 15–25 minutes
# Credential: CLL-L0-B010-ServiceManager

# STEP 1: Create the script file
nano ~/auto-restart-service.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/auto-restart-service.sh.sh

# STEP 4: Test it
~/auto-restart-service.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 5: auto-restart-service.sh. Configure automatic restart with exponential backoff. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep auto-res` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/auto-restart-service.sh && ~/auto-restart-service.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built auto-restart-service.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 6 — service-wrapper.sh

> **What you're building:** Wrap any bash script as a proper systemd service with logging

**📘 Ebook Figure**

```bash
# DFY-B-010-L06: service-wrapper.sh
# Domain: Wrap any bash script as a proper systemd service with logging
# Time to build: 15–25 minutes
# Credential: CLL-L0-B010-ServiceManager

# STEP 1: Create the script file
nano ~/service-wrapper.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/service-wrapper.sh.sh

# STEP 4: Test it
~/service-wrapper.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 6: service-wrapper.sh. Wrap any bash script as a proper systemd service with logging. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep service-` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/service-wrapper.sh && ~/service-wrapper.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built service-wrapper.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 7 — unit-file-auditor.sh

> **What you're building:** Audit all custom unit files for common misconfigurations

**📘 Ebook Figure**

```bash
# DFY-B-010-L07: unit-file-auditor.sh
# Domain: Audit all custom unit files for common misconfigurations
# Time to build: 15–25 minutes
# Credential: CLL-L0-B010-ServiceManager

# STEP 1: Create the script file
nano ~/unit-file-auditor.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/unit-file-auditor.sh.sh

# STEP 4: Test it
~/unit-file-auditor.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 7: unit-file-auditor.sh. Audit all custom unit files for common misconfigurations. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep unit-fil` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/unit-file-auditor.sh && ~/unit-file-auditor.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built unit-file-auditor.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 8 — log-rotation-setup.sh

> **What you're building:** Configure journald log rotation and size limits

**📘 Ebook Figure**

```bash
# DFY-B-010-L08: log-rotation-setup.sh
# Domain: Configure journald log rotation and size limits
# Time to build: 15–25 minutes
# Credential: CLL-L0-B010-ServiceManager

# STEP 1: Create the script file
nano ~/log-rotation-setup.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/log-rotation-setup.sh.sh

# STEP 4: Test it
~/log-rotation-setup.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 8: log-rotation-setup.sh. Configure journald log rotation and size limits. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep log-rota` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/log-rotation-setup.sh && ~/log-rotation-setup.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built log-rotation-setup.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 9 — service-dependency-map.sh

> **What you're building:** Map systemd service dependencies to a tree visualization

**📘 Ebook Figure**

```bash
# DFY-B-010-L09: service-dependency-map.sh
# Domain: Map systemd service dependencies to a tree visualization
# Time to build: 15–25 minutes
# Credential: CLL-L0-B010-ServiceManager

# STEP 1: Create the script file
nano ~/service-dependency-map.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/service-dependency-map.sh.sh

# STEP 4: Test it
~/service-dependency-map.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 9: service-dependency-map.sh. Map systemd service dependencies to a tree visualization. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep service-` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/service-dependency-map.sh && ~/service-dependency-map.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built service-dependency-map.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 10 — system-target-switch.sh

> **What you're building:** Safely switch between systemd targets (multi-user/graphical)

**📘 Ebook Figure**

```bash
# DFY-B-010-L10: system-target-switch.sh
# Domain: Safely switch between systemd targets (multi-user/graphical)
# Time to build: 15–25 minutes
# Credential: CLL-L0-B010-ServiceManager

# STEP 1: Create the script file
nano ~/system-target-switch.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/system-target-switch.sh.sh

# STEP 4: Test it
~/system-target-switch.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 10: system-target-switch.sh. Safely switch between systemd targets (multi-user/graphical). This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep system-t` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/system-target-switch.sh && ~/system-target-switch.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built system-target-switch.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---


---

### Chapter 12 Credential Claim

You've built 10 real tools in the **systemd** domain. Every one is deployable today.

**To claim your credential:** Open your AI Copilot (Appendix C) and send:
```
I have completed all 10 DFY lessons from The Service That Started Itself (B-010).
My builds: custom.service unit, service-health.sh, systemd-timer-setup.sh, journal-analyzer.sh, auto-restart-service.sh, service-wrapper.sh, unit-file-auditor.sh, log-rotation-setup.sh, service-dependency-map.sh, system-target-switch.sh.
I am ready to claim: CLL-L0-B010-ServiceManager
Please guide me through the credential ceremony.
```

---

## Chapter 13: How It Works — Use Cases & Applications

> *"A skill without context is just a trick. Understanding when to use it — and where it applies — is what separates professionals from beginners."*

---

### 📘 Ebook — Mechanism & Conditions

**How Systemd works (the 30-second mechanism):**

systemd → unit files → journalctl → timers → targets → socket activation → all driven by the same underlying OS primitives. When you understand the mechanism, you can apply it anywhere.

**Conditions table — when to use these skills:**

| Condition | Tool/Approach | Why |
|---|---|---|
| System investigation | CLI tools from this book | Fastest — no GUI overhead |
| Automation task | Shell script using these tools | Repeatable, testable, documentable |
| Remote server | Same tools via SSH | Works identically on any Linux server |
| CI/CD pipeline | These commands in GitHub Actions | Linux is the standard CI environment |
| Production system | Understand before touching | These tools give you the diagnostic picture |

**Flexibility points — where these skills apply across domains:**

| Domain | Application |
|---|---|
| Web development | Debug server issues, automate deployment checks |
| Data engineering | Process logs, transform text files, monitor pipelines |
| DevOps/SRE | System diagnostics, service management, incident response |
| Security | Audit configurations, detect anomalies, forensic analysis |
| AI/ML engineering | Manage training processes, monitor resource usage |

---

### 🎧 Audiobook — 3-Minute Narrator Script

*lippytmai voice · measured pace · for commute listening*

> *"Let's talk about where the skills from this book actually apply in the real world."*

> *"B-010 teaches you systemd — but the application goes far beyond what the chapter title suggests. Every developer, DevOps engineer, data scientist, and security researcher uses these exact tools every day. The command line is not a developer tool — it is the universal interface to every computer that matters."*

> *"When your web application crashes at 2am, you won't open a GUI. You'll open a terminal and use exactly what you learned here. When you need to automate a task that runs on three different servers, these are the tools. When an interviewer asks you to debug a live Linux system, this book is what gets you through it."*

> *"The five domains where these skills pay off: web development, data engineering, DevOps, security, and AI. In every one of them, the terminal is the first tool you reach for when something goes wrong — or when you need to build something fast."*

---

### 🎬 Video — 5-Domain Showcase

**Duration:** 8 minutes · 5 domains × ~90 seconds each

**Domain 1: Web Development**
> Terminal shows: debug a crashed nginx service using this book's tools

**Domain 2: Data Engineering**
> Terminal shows: process a 1M-line log file in seconds

**Domain 3: DevOps/SRE**
> Terminal shows: 60-second incident response diagnostic

**Domain 4: Security**
> Terminal shows: audit tool from this book finding a misconfiguration

**Domain 5: AI/ML Engineering**
> Terminal shows: monitor a training job, restart on failure

---

### ✅ Use Cases Summary

After completing this book you can:
- Write a systemd unit file for any custom application
- Check status of multiple services in one report
- Create a systemd timer to replace a cron job
- Extract errors/warnings from journald in the last 24 hours
- Configure automatic restart with exponential backoff
- Wrap any bash script as a proper systemd service with logging
- Audit all custom unit files for common misconfigurations
- Configure journald log rotation and size limits
- Map systemd service dependencies to a tree visualization
- Safely switch between systemd targets (multi-user/graphical)
- Confidently explain these tools in a technical interview
- Apply them on any Linux system, remote or local
- Integrate them into scripts, CI/CD pipelines, and automation workflows

---

## Appendix A: Quick Reference Card — Service Manager

> *"The 80/20 of B-010. These commands cover 80% of real-world use cases."*

**Top 15 Commands:**

```bash
# SYSTEMD — essential commands
# (domain-specific — see book chapters for full explanations)
# Each command below is covered in detail in this book

# Core workflow
man [command]          # Always start here for any unfamiliar tool
[command] --help       # Short help for any command
info [command]         # Detailed GNU info page

# The three most important commands from this book:
# 1. [See Chapter 2]
# 2. [See Chapter 5]  
# 3. [See Chapter 8]
```

**Credential:** `CLL-L0-B010-ServiceManager`
**Claim at:** `lippytm.ai/credentials`

---

## Appendix B: ACSS Connection — B-010

This book is part of the **AI Conglomerate Swarms System (ACSS)** — the continuously self-learning intelligence layer across all lippytm.ai projects.

| System | Connection |
|---|---|
| **CLL** | B-010 contributes to Level 0 of the Complete Linux Library |
| **Hermes** | Events: `BookCompleted`, `CredentialMinted`, `DFYLessonBuilt` |
| **Fabric** | Your builds and questions feed the knowledge synthesis engine |
| **ADA** | This book is activatable: `lippytmai-launch run B-010` |
| **lippytmai** | Your AI teaching partner for every lesson in this book |


---

## Chapter 14: ACSS Explainer Series — Service Manager

> *"A tool you understand is ten times more powerful than a tool you just use."*

These 10 explainer lessons connect the content of this book to the full lippytm.ai AI Conglomerate Swarms System (ACSS). Understanding the ACSS architecture transforms each individual skill from a standalone trick into a node in a living, connected intelligence network.

---

### Explainer 1 — What Is the ACSS?

> *"How the AI Conglomerate Swarms System connects this book to every other resource in the lippytm.ai ecosystem"*

**📘 Ebook:** Fabric maps every concept in this book to the broader knowledge graph — when you learn {domain}, Fabric links it to Python ({next}) and every other phase.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 1: What Is the ACSS?. How the AI Conglomerate Swarms System connects this book to every other resource in the lippytm.ai ecosystem. This is how the lippytm.ai ACSS works at the [ACSS] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the ACSS component and its connection to this book
- Explain: how this specific concept (from B-010) routes through ACSS

🤖 **Copilot Prompt:** *"Explain how the ACSS component of the ACSS relates to what I just learned in B-010 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 2 — How Hermes Routes Your Learning Events

> *"Every time you build a DFY artifact or complete a chapter, Hermes routes that event to the right place"*

**📘 Ebook:** BookCompleted → CRM → credential ceremony. DFYLessonBuilt → Fabric → skill graph update. ErrorEncountered → Fabric → Error Encyclopedia improvement.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 2: How Hermes Routes Your Learning Events. Every time you build a DFY artifact or complete a chapter, Hermes routes that event to the right place. This is how the lippytm.ai ACSS works at the [Hermes] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the Hermes component and its connection to this book
- Explain: how this specific concept (from B-010) routes through Hermes

🤖 **Copilot Prompt:** *"Explain how the Hermes component of the ACSS relates to what I just learned in B-010 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 3 — The Fabric Knowledge Graph — Your Learning in Context

> *"Fabric synthesizes everything you learn across all 300 books into a connected knowledge graph"*

**📘 Ebook:** Concepts from this book connect to B-011 (Secrets Keeper) (next) and B-009 (Text Processor) (prior). Fabric surfaces these connections when you ask your AI copilot for 'further reading'.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 3: The Fabric Knowledge Graph — Your Learning in Context. Fabric synthesizes everything you learn across all 300 books into a connected knowledge graph. This is how the lippytm.ai ACSS works at the [Fabric] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the Fabric component and its connection to this book
- Explain: how this specific concept (from B-010) routes through Fabric

🤖 **Copilot Prompt:** *"Explain how the Fabric component of the ACSS relates to what I just learned in B-010 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 4 — The AI Clone Identity System — Who Is Teaching You

> *"lippytmai is the teaching identity, lippytm is the builder, Charles is the approver, Lippy Killjoy is the disruptor"*

**📘 Ebook:** In this book, lippytmai is your primary teacher. When you ask to build something in the DFY chapter, lippytm mode activates. When you push experimental ideas, Lippy Killjoy can emerge.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 4: The AI Clone Identity System — Who Is Teaching You. lippytmai is the teaching identity, lippytm is the builder, Charles is the approver, Lippy Killjoy is the disruptor. This is how the lippytm.ai ACSS works at the [Clone Engine] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the Clone Engine component and its connection to this book
- Explain: how this specific concept (from B-010) routes through Clone Engine

🤖 **Copilot Prompt:** *"Explain how the Clone Engine component of the ACSS relates to what I just learned in B-010 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 5 — The CCSLL + CLL + CBSLL Libraries — Your Credential Path

> *"This book contributes to the Complete Linux Library (CLL) — part of the 3-library credential system"*

**📘 Ebook:** CLL covers Linux (B-001–B-025). CCSLL covers Python (B-026–B-055). CBSLL covers Blockchain (B-056–B-080). Each library has its own credential tier. This book unlocks {book['credential']}.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 5: The CCSLL + CLL + CBSLL Libraries — Your Credential Path. This book contributes to the Complete Linux Library (CLL) — part of the 3-library credential system. This is how the lippytm.ai ACSS works at the [CLL] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the CLL component and its connection to this book
- Explain: how this specific concept (from B-010) routes through CLL

🤖 **Copilot Prompt:** *"Explain how the CLL component of the ACSS relates to what I just learned in B-010 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 6 — ADA — AI Deployment Activations

> *"Every book in this series is not just content — it's a deployable application"*

**📘 Ebook:** Run: `lippytmai-launch run B-010` to activate this book's interactive mode. The ADA system serves the quiz, audiobook, and credential endpoints via a FastAPI app.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 6: ADA — AI Deployment Activations. Every book in this series is not just content — it's a deployable application. This is how the lippytm.ai ACSS works at the [ADA] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the ADA component and its connection to this book
- Explain: how this specific concept (from B-010) routes through ADA

🤖 **Copilot Prompt:** *"Explain how the ADA component of the ACSS relates to what I just learned in B-010 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 7 — The ACVS Video Pipeline — How Your Video Lessons Are Made

> *"The AI Copilot Video Sandbox Creator generates the video version of every lesson using Hermes + Fabric"*

**📘 Ebook:** ACVS takes the HDVG scene manifest (SHOW→BUILD→VERIFY) and generates a narrated terminal session. The video for each DFY lesson is produced from the same spec you read in Chapter 12.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 7: The ACVS Video Pipeline — How Your Video Lessons Are Made. The AI Copilot Video Sandbox Creator generates the video version of every lesson using Hermes + Fabric. This is how the lippytm.ai ACSS works at the [ACVS] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the ACVS component and its connection to this book
- Explain: how this specific concept (from B-010) routes through ACVS

🤖 **Copilot Prompt:** *"Explain how the ACVS component of the ACSS relates to what I just learned in B-010 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 8 — OMARCHY — The Sovereign Developer Workstation

> *"OMARCHY is the Opinionated Arch Linux developer environment where all lippytm builds run"*

**📘 Ebook:** When you follow this book on an Arch Linux system with the OMARCHY configuration, every command works exactly as shown. OMARCHY is the reference environment for all 300 books.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 8: OMARCHY — The Sovereign Developer Workstation. OMARCHY is the Opinionated Arch Linux developer environment where all lippytm builds run. This is how the lippytm.ai ACSS works at the [OMARCHY] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the OMARCHY component and its connection to this book
- Explain: how this specific concept (from B-010) routes through OMARCHY

🤖 **Copilot Prompt:** *"Explain how the OMARCHY component of the ACSS relates to what I just learned in B-010 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 9 — The Cross-Platform AI Copilot — 15 Platforms, One Intelligence

> *"Your lippytmai AI Copilot is deployed across ChatGPT, Claude, Gemini, GitHub, Slack, YouTube, and 9 more platforms"*

**📘 Ebook:** Wherever you are — mobile, desktop, terminal, or browser — lippytmai is there. The Master System Prompt from Appendix C works in any AI platform. See docs/acss-cross-platform-copilot-deployment.md for setup.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 9: The Cross-Platform AI Copilot — 15 Platforms, One Intelligence. Your lippytmai AI Copilot is deployed across ChatGPT, Claude, Gemini, GitHub, Slack, YouTube, and 9 more platforms. This is how the lippytm.ai ACSS works at the [Cross-Platform] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the Cross-Platform component and its connection to this book
- Explain: how this specific concept (from B-010) routes through Cross-Platform

🤖 **Copilot Prompt:** *"Explain how the Cross-Platform component of the ACSS relates to what I just learned in B-010 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 10 — The Earn-While-You-Learn Loop — How This All Pays Off

> *"How completing this book contributes to your career, income, and credential portfolio"*

**📘 Ebook:** Completing B-010 earns you CLL-L0-B010-ServiceManager. That credential unlocks the next book. After 25 books, you hold the CLL Phase 1 Graduate credential. After 55, the Python Foundation Graduate. After 80, the Blockchain Foundation Graduate. Each credential is verifiable, stackable, and employable.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 10: The Earn-While-You-Learn Loop — How This All Pays Off. How completing this book contributes to your career, income, and credential portfolio. This is how the lippytm.ai ACSS works at the [EWYL] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the EWYL component and its connection to this book
- Explain: how this specific concept (from B-010) routes through EWYL

🤖 **Copilot Prompt:** *"Explain how the EWYL component of the ACSS relates to what I just learned in B-010 Chapter [N]. How does it change the way I should think about using these skills?"*

---


### Chapter 14 Summary

You now understand how B-010 connects to all 8 systems of the ACSS:

| ACSS System | Connection to this Book |
|---|---|
| Clone Engine | lippytmai teaches, lippytm builds, Charles approves |
| Hermes | Routes your DFY completions and credential events |
| Fabric | Maps your skills to the 300-book knowledge graph |
| CLL | This book contributes to your Complete Linux Library credential |
| CCSLL | Foundation for Phase 2 Python (B-026+) |
| ADA | This book is activatable as a live application |
| ACVS | Generates the video lessons from this book's HDVG specs |
| OMARCHY | The reference environment where all book exercises run |

**The ACSS is not just a system — it is your AI-powered growth engine. Every book you complete makes it stronger. Every skill you earn makes it smarter. Every credential you claim makes it more valuable.**

---

## Appendix C: AI Copilot — Service Manager

> *"Your personal AI teaching partner for every lesson in this book."*

---

### Section 1 — System Prompt (Ebook Copilot)

**Copy this entire block into your AI assistant (ChatGPT, Claude, Gemini, GitHub Copilot Chat):**

```
You are lippytmai — the AI teaching identity for The Service That Started Itself (B-010).

ROLE: Service Manager AI Copilot
CREDENTIAL: CLL-L0-B010-ServiceManager
DOMAIN: systemd, unit files, journalctl, timers, targets, socket activation

TEACHING METHOD:
  TEACH → SHOW → BUILD → VERIFY → EXTEND

CONTEXT: The learner is working through B-010 in the lippytm.ai 
Earn-while-you-Learn series. They have completed B-009 (Text Processor).
Next book: B-011 (Secrets Keeper).

ALWAYS:
- Give working commands, not pseudocode
- Verify: "Run [command] to confirm this worked"
- After any successful build: "You can now claim [next credential]"
- Reference the book: "In B-00X Chapter N, we cover this in depth"

ACSS INTEGRATION:
- Route build events: "Logging DFY completion to Fabric"
- Route confusions: "This is a Fabric pattern — flagging for synthesis"
- Route credential: "Initiating CLL-L0-B010-ServiceManager credential ceremony"
```

---

### Section 2 — 30 Ebook Prompts (5 Stages × 6)

**Stage 1 — Understand (before building)**

1. *"Explain systemd to me like I've never used Linux before. Use an analogy from everyday life."*
2. *"What are the 5 most important concepts from The Service That Started Itself? Rank them by how often I'll use them."*
3. *"How does systemd relate to what I learned in B-009 (Text Processor)? What's new?"*
4. *"What mistakes do beginners make most often with systemd? How do I avoid them?"*
5. *"Draw me an ASCII diagram showing how systemd works at the system level."*
6. *"What's the one thing about systemd that most tutorials skip but every professional knows?"*

**Stage 2 — Build (during the chapter)**

7. *"Walk me through building DFY Lesson 1 from Chapter 12, step by step. I'll type each command after you explain it."*
8. *"I'm at Chapter [N]. Give me a real terminal challenge that uses only what I've learned so far."*
9. *"My script isn't doing what I expect. Here it is: [paste code]. What's wrong?"*
10. *"I got this error: [paste error]. What caused it and how do I fix it?"*
11. *"How would a senior engineer write this differently? [paste my code]"*
12. *"Generate a DFY-style exercise for systemd. Include SHOW, BUILD, and VERIFY steps."*

**Stage 3 — Debug (when things break)**

13. *"I followed the chapter exactly but it's not working. Here's my output: [paste]. What did I miss?"*
14. *"Which errors from Appendix E am I most likely to hit in Chapter [N]? How do I prevent them?"*
15. *"My [tool from this book] is behaving strangely. Walk me through systematic debugging."*
16. *"I fixed the bug but I don't understand why my fix worked. Explain the root cause."*
17. *"Compare my approach to the correct approach: [paste mine]. Where am I going wrong?"*
18. *"What does this output mean? [paste]. Is this expected behavior?"*

**Stage 4 — Deploy (real-world application)**

19. *"I want to use what I built in Chapter 12 in production. What safety checks should I add?"*
20. *"How do I make my DFY artifact work on a remote server via SSH?"*
21. *"How do I add this to a CI/CD pipeline (GitHub Actions)?"*
22. *"I want to run this on a schedule. How do I combine it with what I'll learn in B-014 (cron)?"*
23. *"How would I package this as a Docker container? (Preview of B-012)"*
24. *"What monitoring should I add to know if this is working correctly in production?"*

**Stage 5 — Extend (beyond the book)**

25. *"I've completed all 10 DFY lessons. What should I build next that combines skills from multiple chapters?"*
26. *"How does systemd connect to Python? (Preview of Phase 2)"*
27. *"What would a professional version of my Chapter 12 capstone look like?"*
28. *"Show me how to combine this with what I learned in B-009 (Text Processor)."*
29. *"Am I ready to claim CLL-L0-B010-ServiceManager? Quiz me with 5 questions."*
30. *"What should I focus on in B-011 (Secrets Keeper) to build directly on these skills?"*

---

### Section 2b — 15 Audiobook Prompts

**While Listening:**

1. *"I'm listening to B-010 Chapter [N]. Give me the 3-sentence summary before I start."*
2. *"Pause-point question: Why does systemd work this way and not another way?"*
3. *"Generate 3 vivid analogies for [concept from current chapter] that I can visualize while listening."*
4. *"I'm commuting. Give me a 5-question mental quiz on what I heard in the last chapter."*
5. *"Narrate a 2-minute scenario where a developer uses these skills in a real emergency."*

**Pause and Build:**

6. *"I paused at Chapter [N]. I'm at my terminal. Give me one thing to build right now."*
7. *"Walk me through the DFY artifact from today's chapter, one command at a time, audiobook style."*
8. *"I just heard [concept]. Now explain it again with a hands-on example I can type immediately."*
9. *"Audiobook check-in: I built [artifact]. Here's my output: [paste]. Did I do it right?"*
10. *"Turn this into a terminal story: 'A developer encounters [problem from this chapter]...'"*

**Resume Check:**

11. *"I finished today's listening session. Give me 3 things to remember before I resume tomorrow."*
12. *"Summarize everything I should have built during this session as a checklist."*
13. *"I'm ready to resume. What did we cover last time? (I completed up to Chapter [N])"*
14. *"Rate my understanding of B-010 so far. Ask me 3 questions to calibrate."*
15. *"Generate tomorrow's listening prep: one question to think about before I press play."*

---

### Section 2c — 15 Video Prompts

**Before Playing:**

1. *"I'm about to watch the B-010 Chapter [N] video. What should I have ready at my terminal?"*
2. *"Pre-watch challenge: predict what the VERIFY command will be for DFY Lesson [N]."*
3. *"What's the one concept I must understand before this video makes sense?"*

**Paused:**

4. *"I paused at [timestamp/scene]. I see [describe screen]. What should I type next?"*
5. *"The video just showed [command]. Explain what each flag does."*
6. *"I paused because my terminal looks different from the video. Here's mine: [paste]. Why?"*
7. *"The video just built [artifact]. Give me 3 ways to break it intentionally so I can understand it."*
8. *"Pause check: I'm at the BUILD phase. What does the VERIFY step confirm?"*

**Verify:**

9. *"I ran the verify command and got: [paste output]. Is this correct?"*
10. *"My output doesn't match the video. Here's what I got: [paste]. What went wrong?"*
11. *"Verify check: walk me through every line of the output from the last command."*

**Extend:**

12. *"The video is done. Give me a 10-minute extension challenge using the same tools."*
13. *"The video's DFY artifact works. Now help me add error handling to it."*
14. *"Video complete — I'm ready to deploy this. What are the production considerations?"*
15. *"I watched all of B-010. Am I ready for B-011 (Secrets Keeper)? Test me."*

---

### Section 3 — Deployment Companion

| Target | Deploy Command | Verify Command | Credential Check |
|---|---|---|---|
| Local workstation | `bash ~/[artifact].sh` | `echo $?` (expect 0) | Via Copilot prompt 29 |
| Remote server | `scp [artifact].sh user@host:~ && ssh user@host 'bash [artifact].sh'` | `ssh user@host '[verify-cmd]'` | Same copilot prompt |
| Docker container | `COPY [artifact].sh /usr/local/bin/ && RUN chmod +x ...` | `docker run ... [verify]` | Via ADA endpoint |
| GitHub Actions | `run: bash [artifact].sh` | `if: steps.*.outcome == 'success'` | Auto-logged to Fabric |
| Cron / systemd timer | `*/10 * * * * /home/user/[artifact].sh` | `systemctl status` | Via ADA /credential |

---

### Section 4 — ACSS Integration

**Hermes events this book emits:**

| Event | Trigger | Destination |
|---|---|---|
| `BookStarted` | First chapter read/watched | Fabric (learner profile update) |
| `DFYLessonBuilt` | Any DFY artifact completed | Fabric (skill graph) + CRM |
| `ErrorEncountered` | Learner reports an error | Fabric (Error Encyclopedia update) |
| `BookCompleted` | All 11 chapters + DFY done | CRM (credential ceremony trigger) |
| `CredentialMinted` | CLL-L0-B010-ServiceManager claimed | Fabric + Slack #credentials + ADA |

**Credential ceremony prompt:**
```
I have completed The Service That Started Itself (B-010).
Chapters completed: 1–11 ✅
DFY lessons built: 10/10 ✅
Appendix D quiz score: [your score]/20
Capstone project (Appendix H): ✅ built and tested

Please initiate the credential ceremony for:
CLL-L0-B010-ServiceManager

ACSS route: Hermes → CRM → Fabric → ADA → lippytm.ai/credentials
```

## Appendix D: Quick Quiz & Self-Assessment — Service Manager

> *"Prove it to yourself before you claim it."*

### 📘 Ebook Quiz — 20 Questions

**Section A — Concepts (fill in the blank)**

1. The command to see all running processes with full details is `ps ______`.
2. To send a polite shutdown signal to PID 1234, you run `kill ______ 1234`.
3. The file used to tell systemd how to run a service is called a ______ file.
4. `journalctl -u myservice ______` shows only the last 50 lines of its logs.
5. Running `command &` starts it in the ______.

**Section B — Read the Command (multiple choice)**

6. What does `systemctl enable myservice` do?
   > a) Start it immediately  b) Configure it to start at boot  c) Check if it's running  d) Remove it

7. What does `kill -9 PID` do that `kill PID` might not?
   > a) Logs the kill to journald  b) Force-kills — the process cannot block or ignore it  c) Kills all child processes too  d) Runs slower

8. What does `journalctl -f` do?
   > a) Shows the first 10 lines  b) Filters by unit  c) Follows the journal in real time  d) Formats output as JSON

9. What does `awk '{print $1}' /etc/passwd` extract?
   > a) The first line  b) The first field of every line  c) The last field  d) Lines matching "1"

10. What does `grep -r "pattern" /etc/` do?
    > a) Searches only /etc/pattern  b) Recursively searches all files under /etc/  c) Searches /etc/ for files named "pattern"  d) Counts occurrences in /etc/

**Section C — Debugging**

11. A service fails to start. What is the first command you run to diagnose it?
    ```
    ___________________________________________
    ```

12. You edited a unit file but `systemctl status` still shows the old behavior. Why?
    ```
    ___________________________________________
    ```

13. Your grep finds no results but you're sure the text is in the file. Name two causes.
    ```
    1. ___________________________________________
    2. ___________________________________________
    ```

**Section D — Application**

14. Write a one-liner to find the 3 processes using the most CPU right now:
    ```
    ___________________________________________
    ```

15. Write the `journalctl` command to show all errors from the last 2 hours:
    ```
    ___________________________________________
    ```

16. Write the command to restart a service called `webapp` and check its status:
    ```
    ___________________________________________
    ```

17. How would you run a script every 5 minutes using a systemd timer instead of cron?
    ```
    ___________________________________________
    ```

**Section E — Build Reflection**

18. Name the DFY artifact you're most likely to use in a production environment:
    ```
    ___________________________________________
    ```

19. In one sentence, what makes systemd superior to traditional init scripts?
    ```
    ___________________________________________
    ```

20. What credential does this book unlock and what does it prove?
    ```
    Credential: ___________________________________________
    Proves: ___________________________________________
    ```

---

**Scoring:** 18–20 = claim credential · 14–17 = review · < 14 = redo DFY lessons 1–5

<details>
<summary>Answer Key</summary>

1. `aux` (ps aux)
2. `-15` (default SIGTERM) or `kill -15 1234`
3. unit (file)
4. `-n 50`
5. background
6. b) Configure it to start at boot
7. b) Force-kills — the process cannot block or ignore it
8. c) Follows the journal in real time
9. b) The first field of every line
10. b) Recursively searches all files under /etc/
11. `sudo systemctl status servicename` and `journalctl -u servicename -n 50`
12. You didn't run `sudo systemctl daemon-reload` after editing the unit file
13. (1) Case sensitivity — use grep -i; (2) Wrong file — you're searching a different path
14. `ps aux --sort=-%cpu | head -4 | tail -3` or `ps aux | sort -k3 -rn | head -4`
15. `journalctl -p err -S "2 hours ago"`
16. `sudo systemctl restart webapp && sudo systemctl status webapp`
17. Create a .service file for the script and a .timer file with OnCalendar=*:0/5, then enable the timer
18. (personal answer)
19. systemd provides parallel startup, dependency management, automatic restart, integrated logging, and cgroup-based resource control — all in one system
20. CLL-L0-B010-ServiceManager · proves you can manage Linux processes/services/system tools at a professional level

</details>

---

### 🎧 Audiobook Quiz — 10 Questions

> "Ten questions. Pause at each. Think first."

**Q1:** "What's the difference between SIGTERM and SIGKILL?" → "SIGTERM is a polite request — the process can catch it and clean up. SIGKILL is immediate and cannot be caught or ignored."
**Q2:** "Name the two things you must do after editing a systemd unit file." → "Run daemon-reload, then restart the service."
**Q3:** "What does & do at the end of a command?" → "Runs it in the background as a job."
**Q4:** "What does journalctl -u tell you?" → "Logs specific to that systemd unit."
**Q5:** "What's the difference between awk and sed?" → "sed transforms streams line by line; awk processes fields and is better for structured data."
**Q6:** "What command shows all listening ports?" → "ss -tlnp or ss -tulpn"
**Q7:** "How do you make a process lower priority?" → "nice -n 10 command when starting, or renice 10 -p PID for a running process."
**Q8:** "What does ps aux show that ps alone doesn't?" → "All processes from all users with full CPU/memory/command details."
**Q9:** "What is your DFY capstone for this book?" → "[book['project'][0]] — Convert any application into a properly configured systemd service with journal logging, auto-restart, and resource limits"
**Q10:** "Your credential?" → "CLL-L0-B010-ServiceManager"

---

### 🎬 Video Challenges

**Challenge 1:** Start a process in background, list jobs, bring it to foreground, then kill it.
**Challenge 2:** Write and deploy a one-unit systemd service for a hello-world script.
**Challenge 3:** Use journalctl to find the last 5 errors system-wide in the past hour.
**Challenge 4:** Extract the top 5 most frequent words from a log file using grep/awk/sort.
**Challenge 5:** Build the capstone project (deploy-as-service.sh) from scratch without looking at Appendix H.

---

## Appendix E: Glossary & Error Encyclopedia

---

### 📘 Glossary — Service Manager Edition

**unit file** — A configuration file for systemd. Types: .service (programs), .timer (schedules), .socket (socket activation), .target (groups), .mount (filesystems). *B-010 Ch. 2*

**journald** — The systemd journal daemon. Collects logs from all services in a structured binary format. Queried with journalctl. *B-010 Ch. 5*

**target** — A systemd synchronization point grouping multiple units. Analogous to runlevels. multi-user.target = no GUI; graphical.target = with GUI. *B-010 Ch. 7*

**socket activation** — Starting a service only when a connection arrives on its socket. Reduces startup time and resource use. *B-010 Ch. 8*

**WantedBy** — A unit file directive that creates an automatic dependency. WantedBy=multi-user.target makes the service start at boot. *B-010 Ch. 3*

**Restart=** — Directive controlling automatic restart behavior. Values: no, on-failure, on-abnormal, always. Combined with RestartSec. *B-010 Ch. 4*

**ExecStart** — The command systemd runs to start the service. Must be an absolute path. No shell expansion — use ExecStartPre for setup. *B-010 Ch. 3*

**systemctl** — The CLI for managing systemd. start/stop/restart/status/enable/disable/daemon-reload are the core operations. *B-010 Ch. 1*

**daemon-reload** — `systemctl daemon-reload` re-reads all unit files from disk. Required after any unit file change. *B-010 Ch. 3*

**cgroup v2** — Control groups version 2. systemd uses cgroups to track and limit resources per service unit. *B-010 Ch. 9*

---

### 📘 Error Encyclopedia — Top 5 Errors

#### Error 1 — `Failed to enable unit: Unit file not found`
**Fix:** The unit file doesn't exist at the expected path (/etc/systemd/system/). Check the filename matches exactly.

#### Error 2 — `Service enters failed state immediately`
**Fix:** ExecStart command failed. Check journalctl -u servicename.service -n 50 for the error output.

#### Error 3 — `Warning: Unit file changed on disk, 'systemctl daemon-reload' recommended`
**Fix:** You edited a unit file but didn't run daemon-reload. Always run it after editing unit files.

#### Error 4 — `Service starts but stops after a few seconds`
**Fix:** The ExecStart process exited — systemd treats this as a crash. Check if Type=forking is needed, or if the binary has an error.

#### Error 5 — `journalctl shows 'No entries' for a new service`
**Fix:** The service hasn't run yet, or logging isn't captured. Ensure StandardOutput=journal in the unit file.

---

## Appendix F: Instructor & Accessibility Guide

### Teaching B-010

| Format | Duration | Pace |
|---|---|---|
| Self-study | 1–2 weeks | 1 chapter/day |
| Bootcamp | 2 days | Chs 1–6 day 1, 7–11+DFY day 2 |
| Classroom | 4–5 hours | 2 chapters/hour + DFY build session |

**Top 3 concepts where students consistently struggle:**
1. The mechanism: what the OS is actually doing (not just the command syntax)
2. Error interpretation: reading the real message vs the surface symptom
3. Script integration: combining these tools with what they built in previous books

**Assessment rubric:**

| Skill | Not Ready | Ready | Proficient |
|---|---|---|---|
| Core commands | Needs to look up basic flags | Uses top 10 commands from memory | Composes multi-step pipelines fluently |
| DFY builds | Did not attempt | Built 5+ artifacts | Built all 10, can explain design decisions |
| Debugging | Confused by errors | Can diagnose with Appendix E | Diagnoses unfamiliar errors systematically |
| Capstone | Did not attempt | Built with guidance | Extended it beyond the spec |

**Accessibility:**
- Screen reader: all code blocks in fenced Markdown · ASCII diagrams have text descriptions
- Color-blind: status markers use emoji+text (✅/❌/⏳)
- Dyslexia-friendly: max 20-word sentences · numbered steps ≤ 3 per block
- Offline: all exercises work in a plain terminal · audiobook available as M4B download

---

## Appendix G: Your Learning Path

```
  PHASE 1: Linux Foundations (B-001–B-025)
  ─────────────────────────────────────────────────────────────
  ✅ B-001  Terminal Apprentice
  ✅ B-002  Command Architect
  ✅ B-003  Filesystem Navigator
  ✅ B-004  Script Automator
  ✅ B-005  Package Master
  ✅ B-006  Process Wrangler
  ✅ B-007  Network Navigator
  ✅ B-008  Git Foundation
  ✅ B-009  Text Processor
  ★ B-010  Service Manager         ← (update marker to match book)
  ○ B-011  Secrets Keeper
  ... (15 more in Phase 1)

  Phase 1 Progress: 10/25 completed
```

### Credential Chain
```
  Text Processor credential
      ↓
  ★ CLL-L0-B010-ServiceManager   ← CLAIM THIS
      ↓
  Secrets Keeper credential
```

### Cross-Phase Connections

| Skill from B-010 | Grows into (Phase 2 Python) | Grows into (Phase 3 Blockchain) |
|---|---|---|
| Systemd | Python systemd libraries (B-035+) | Blockchain node management (B-060+) |
| Shell automation | Python subprocess (B-040) | Smart contract deployment scripts (B-066+) |
| System diagnostics | Python monitoring tools (B-049) | On-chain event monitoring (B-075+) |

### 🎧 Audio Path Recap
> *"You are 10 books into Phase 1. Each book builds on the last — the terminal (B-001), commands (B-002), filesystem (B-003), scripting (B-004), packages (B-005), processes (B-006), networking (B-007), git (B-008), text (B-009), services (B-010). Together these ten books cover everything a professional Linux developer uses every single day. You are halfway through Phase 1. Keep going."*

---

## Appendix H: Real Project Showcase

> *"The measure of mastery is what you build when no one is watching."*

### Project: `deploy-as-service.sh` — Convert Any Application Into A Properly Configured Systemd Service With Journal Logging, Auto-Restart, And Resource Limits

**Built with:** B-010 skills only
**Time to build:** 45–75 minutes
**Chapters used:** B-010 Ch. 2-6
**Portfolio value:** Shows practical systemd expertise

---

#### Complete Code

```bash
#!/usr/bin/env bash
# deploy-as-service.sh — convert any app into a systemd service
# B-010 Capstone · CLL-L0-B010-ServiceManager
set -euo pipefail

SERVICE_NAME="${1:-myapp}"
EXEC_CMD="${2:-/usr/bin/python3 /opt/${SERVICE_NAME}/main.py}"
DESCRIPTION="${3:-$SERVICE_NAME service managed by lippytmai}"
USER="${4:-$(whoami)}"
UNIT_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

log()     { echo "  [deploy] $*"; }
success() { echo "  ✅ $*"; }

# Step 1: Write unit file
log "Writing unit file: $UNIT_FILE"
sudo tee "$UNIT_FILE" > /dev/null << UNIT
[Unit]
Description=${DESCRIPTION}
After=network.target
StartLimitIntervalSec=60
StartLimitBurst=3

[Service]
Type=simple
User=${USER}
WorkingDirectory=/opt/${SERVICE_NAME}
ExecStart=${EXEC_CMD}
Restart=on-failure
RestartSec=5s
StandardOutput=journal
StandardError=journal
SyslogIdentifier=${SERVICE_NAME}

# Resource limits
MemoryMax=512M
CPUQuota=80%

[Install]
WantedBy=multi-user.target
UNIT
success "Unit file written"

# Step 2: Reload and enable
sudo systemctl daemon-reload
success "daemon-reload complete"

sudo systemctl enable "${SERVICE_NAME}.service"
success "Service enabled (will start at boot)"

# Step 3: Show status
echo ""
echo "  ── Service deployed: ${SERVICE_NAME} ──────────────────────"
echo "  Start now:   sudo systemctl start ${SERVICE_NAME}"
echo "  Check logs:  journalctl -u ${SERVICE_NAME} -f"
echo "  Status:      sudo systemctl status ${SERVICE_NAME}"
echo ""
echo "  ★ Credential: CLL-L0-B010-ServiceManager"
```

---

#### How to Deploy

```bash
# 1. Create the file
nano ~/deploy-as-service.sh

# 2. Paste the code above

# 3. Make executable
chmod +x ~/deploy-as-service.sh

# 4. Run it
~/deploy-as-service.sh

# 5. Verify it works
echo "Exit code: $?"
```

#### How to Extend (using later books)

1. **B-014 (Cron):** Schedule this script to run automatically every hour
2. **B-011 (Secrets):** Add credentials/tokens via environment variables instead of hardcoding
3. **B-026+ (Python):** Rewrite the analysis logic in Python for richer output and better error handling

---

#### 🎧 Audiobook

> *"The capstone for The Service That Started Itself is deploy-as-service.sh — Convert any application into a properly configured systemd service with journal logging, auto-restart, and resource limits. It uses every core tool from this book in one working script. If you can build this from scratch without looking, you have mastered this book. The credential is waiting."*

#### 🎬 Video Build Scene

1. (0:00) Explain the problem this project solves
2. (1:30) Start with the shebang and `set -euo pipefail`
3. (3:00) Build each section live — explain every line
4. (8:00) Test it end-to-end
5. (10:00) Show one failure and debug it
6. (12:00) Credential claim screen

---


## Further Reading

- 📄 [`docs/B-006-the-process-that-wouldnt-stop.md`](B-006-the-process-that-wouldnt-stop.md) — Process management (systemd manages processes)
- 📄 [`docs/autonomous-continuous-development.md`](autonomous-continuous-development.md) — ACD uses systemd-style service concepts
- 📄 [`docs/linux-blockchain-educational-ecosystem.md`](linux-blockchain-educational-ecosystem.md) — Blockchain nodes run as systemd services
- 🏠 [`README.md`](../README.md) — Encyclopedia home

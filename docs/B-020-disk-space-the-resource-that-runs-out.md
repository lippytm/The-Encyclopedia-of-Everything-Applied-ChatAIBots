# B-020: Disk Space — The Resource That Runs Out

### df, du, lsblk, fstab, and the Disk Monitor Alert Script

> *"Disk space is the silent killer of production systems. No warning, no gradual degradation — just a sudden wall: the database stops writing, the logging daemon crashes, the container build fails. A developer who monitors disk space proactively never gets the 3 AM call. This book teaches you to be that developer."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Read disk usage with `df` and `du`
2. Inspect block devices with `lsblk` and `fdisk`
3. Understand `/etc/fstab` and mount points
4. Find and clean disk space hogs
5. Write a disk monitor alert script that runs via cron

**Prerequisite:** B-001 through B-019

**Build Artifact:** A `disk-monitor.sh` script that checks disk usage per mount point, alerts when above a threshold, cleans Docker images, and logs to a daily report

**Credential:** `CLL-L1-B020-DiskOperator` — on-chain on Base

---

## Chapter 1: df — Disk Free

`df` reports filesystem disk space usage:

```bash
# Human-readable summary of all filesystems
df -h

# Example output:
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sda1        50G   32G   16G  67% /
# /dev/sda2       200G  145G   45G  77% /home
# tmpfs            16G  512M   16G   4% /tmp

# Show inodes (another resource that runs out)
df -i

# Show a specific filesystem
df -h /home

# Show filesystem type
df -T
```

---

## Chapter 2: du — Disk Usage

`du` measures how much disk space directories and files use:

```bash
# Size of current directory and subdirectories
du -sh *

# Sorted by size (largest first)
du -sh * | sort -rh | head -20

# Size of a specific directory
du -sh ~/developer-workspace

# All directories recursively, sorted
du -h ~/developer-workspace | sort -rh | head -20

# Find largest files in a path
find /var/log -type f -exec du -h {} \; | sort -rh | head -10

# Size of a Docker volume
du -sh /var/lib/docker

# Quick find: what's eating my home directory?
du -sh ~/* | sort -rh | head -10
```

---

## Chapter 3: lsblk and Block Devices

```bash
# List all block devices (disks, partitions, LVM, loop)
lsblk

# With filesystem info
lsblk -f

# Example output:
# NAME   FSTYPE   SIZE MOUNTPOINT
# sda             500G
# ├─sda1 ext4      50G /
# ├─sda2 ext4     200G /home
# └─sda3 swap      16G [SWAP]
# nvme0n1         1.0T
# └─nvme0n1p1 ext4 1.0T /data

# Detailed disk info
sudo fdisk -l /dev/sda

# SMART disk health
sudo smartctl -a /dev/sda    # install: sudo pacman -S smartmontools
```

---

## Chapter 4: /etc/fstab — Mount Points at Boot

`/etc/fstab` defines which filesystems mount at boot:

```bash
# View current fstab
cat /etc/fstab

# Example:
# <device>              <mountpoint>  <type>  <options>        <dump> <pass>
# /dev/sda1             /             ext4    defaults,errors=remount-ro  0  1
# /dev/sda2             /home         ext4    defaults                    0  2
# UUID=abc-def-123      /data         ext4    defaults,noatime            0  2
# tmpfs                 /tmp          tmpfs   defaults,size=4G            0  0

# Mount all fstab entries
sudo mount -a

# Use UUID (more reliable than /dev/sda1 which can change)
sudo blkid /dev/sda2    # find UUID

# Mount a new disk temporarily
sudo mkdir /mnt/backup-disk
sudo mount /dev/sdb1 /mnt/backup-disk

# Unmount
sudo umount /mnt/backup-disk
```

---

## Chapter 5: Common Space Hogs and How to Clean Them

```bash
# Docker images and stopped containers
docker system df              # show Docker disk usage
docker image prune            # remove dangling images
docker system prune           # remove all unused resources
docker system prune -a        # remove ALL unused images (aggressive)

# Systemd journal
journalctl --disk-usage
sudo journalctl --vacuum-size=500M
sudo journalctl --vacuum-time=30d

# Package cache (Arch)
sudo pacman -Sc               # keep last version
sudo pacman -Scc              # remove all cached packages

# Package cache (Ubuntu/Debian)
sudo apt-get clean
sudo apt-get autoremove

# Large log files
find /var/log -name "*.log" -size +100M -exec ls -lh {} \;
sudo truncate -s 0 /var/log/large.log    # zero out without deleting

# Trash
rm -rf ~/.local/share/Trash/*
```

---

## Chapter 6: The Build — Disk Monitor Alert Script

```bash
#!/bin/bash
# disk-monitor.sh — B-020 Build Artifact
# Monitors disk usage, alerts on threshold breach, cleans Docker resources
set -euo pipefail

THRESHOLD="${DISK_THRESHOLD:-85}"      # alert when disk is >85% full
REPORT_DIR="$HOME/logs"
REPORT_FILE="$REPORT_DIR/disk-report-$(date +%Y%m%d).log"
ALERT=0

mkdir -p "$REPORT_DIR"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$REPORT_FILE"; }

log "=== Disk Monitor Report ==="
log "Threshold: ${THRESHOLD}%"
log ""
log "--- Filesystem Usage ---"

# Check each mounted filesystem
while IFS= read -r line; do
    pct=$(echo "$line" | awk '{print $5}' | tr -d '%')
    mount=$(echo "$line" | awk '{print $6}')
    size=$(echo "$line" | awk '{print $2}')
    used=$(echo "$line" | awk '{print $3}')

    if [ "$pct" -ge "$THRESHOLD" ]; then
        log "⚠️  ALERT: $mount is at ${pct}% ($used / $size)"
        ALERT=1
    else
        log "✅  OK:    $mount is at ${pct}% ($used / $size)"
    fi
done < <(df -h --output=size,used,avail,pcent,target | tail -n +2 | grep -v "tmpfs\|/dev/loop")

log ""
log "--- Docker Resource Usage ---"
if command -v docker &>/dev/null && docker info &>/dev/null 2>&1; then
    docker system df 2>/dev/null | tee -a "$REPORT_FILE" || true

    # Auto-clean if over threshold
    if [ "$ALERT" = "1" ]; then
        log "Cleaning Docker dangling images..."
        docker image prune -f 2>&1 | tee -a "$REPORT_FILE" || true
    fi
else
    log "(Docker not running)"
fi

log ""
log "--- Top 10 Largest Directories in /home ---"
du -sh /home/* 2>/dev/null | sort -rh | head -10 | tee -a "$REPORT_FILE" || true

log ""
log "Report saved: $REPORT_FILE"

# Exit with error code if alert triggered (allows cron to email on failure)
exit "$ALERT"
```

```bash
chmod +x ~/scripts/disk-monitor.sh

# Test run
~/scripts/disk-monitor.sh

# Add to crontab (runs daily at 8 AM)
(crontab -l 2>/dev/null; echo "0 8 * * * /home/charles/scripts/disk-monitor.sh >> /home/charles/logs/disk-monitor.log 2>&1") | crontab -
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-020 Verification ==="
echo "Current disk state:"
df -h | grep -v tmpfs

echo ""
echo "Disk monitor run:"
~/scripts/disk-monitor.sh

echo ""
echo "Crontab entry:"
crontab -l | grep disk-monitor
```

---


## Chapter 12: Done-For-You Lessons — Disk Space: The Resource That Runs Out

> *"Done-for-you means it's already designed, already structured, already proven.
> Your job is to execute and claim the result." — lippytmai*

This chapter gives you 10 ready-to-use lesson structures for disk space management and storage optimization.
Each lesson covers all three formats so you can learn your way.

---

### DFY Lesson 1: What Is Disk Space Management And Storage Optimization and Why It Matters

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 01: What Is Disk Space Management And Storag  │
│  Book: B-020  Tool: df                                  │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"This is lippytmai. Lesson 1: What Is Disk Space Management And Storage Optimization and Why It Matters. In this lesson you will learn
> to apply disk space management and storage optimization using df. The key insight is that every professional
> Linux user has a repeatable system for this. Yours starts here.
> Ready? Let's go."*

**🎬 Video Scene:**

- **SHOW:** Terminal with `df` open, real output visible
- **BUILD:** Walk through the concept step by step with live typing
- **VERIFY:** Run a check command to confirm the result

**🤖 Copilot Prompt:**

> "I just completed DFY Lesson 1 of B-020. Help me practice: What Is Disk Space Management And Storage Optimization and Why It Matters.
> Give me 3 progressive exercises, from beginner to confident practitioner."

---
### DFY Lesson 2: Your First df Command

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 02: Your First df Command                     │
│  Book: B-020  Tool: df                                  │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"This is lippytmai. Lesson 2: Your First df Command. In this lesson you will learn
> to apply disk space management and storage optimization using df. The key insight is that every professional
> Linux user has a repeatable system for this. Yours starts here.
> Ready? Let's go."*

**🎬 Video Scene:**

- **SHOW:** Terminal with `df` open, real output visible
- **BUILD:** Walk through the concept step by step with live typing
- **VERIFY:** Run a check command to confirm the result

**🤖 Copilot Prompt:**

> "I just completed DFY Lesson 2 of B-020. Help me practice: Your First df Command.
> Give me 3 progressive exercises, from beginner to confident practitioner."

---
### DFY Lesson 3: The Three Formats: Ebook, Audiobook, Video

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 03: The Three Formats: Ebook, Audiobook, Vid  │
│  Book: B-020  Tool: df                                  │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"This is lippytmai. Lesson 3: The Three Formats: Ebook, Audiobook, Video. In this lesson you will learn
> to apply disk space management and storage optimization using df. The key insight is that every professional
> Linux user has a repeatable system for this. Yours starts here.
> Ready? Let's go."*

**🎬 Video Scene:**

- **SHOW:** Terminal with `df` open, real output visible
- **BUILD:** Walk through the concept step by step with live typing
- **VERIFY:** Run a check command to confirm the result

**🤖 Copilot Prompt:**

> "I just completed DFY Lesson 3 of B-020. Help me practice: The Three Formats: Ebook, Audiobook, Video.
> Give me 3 progressive exercises, from beginner to confident practitioner."

---
### DFY Lesson 4: Common Mistakes with Disk

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 04: Common Mistakes with Disk                 │
│  Book: B-020  Tool: df                                  │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"This is lippytmai. Lesson 4: Common Mistakes with Disk. In this lesson you will learn
> to apply disk space management and storage optimization using df. The key insight is that every professional
> Linux user has a repeatable system for this. Yours starts here.
> Ready? Let's go."*

**🎬 Video Scene:**

- **SHOW:** Terminal with `df` open, real output visible
- **BUILD:** Walk through the concept step by step with live typing
- **VERIFY:** Run a check command to confirm the result

**🤖 Copilot Prompt:**

> "I just completed DFY Lesson 4 of B-020. Help me practice: Common Mistakes with Disk.
> Give me 3 progressive exercises, from beginner to confident practitioner."

---
### DFY Lesson 5: Building a Disk Workflow

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 05: Building a Disk Workflow                  │
│  Book: B-020  Tool: df                                  │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"This is lippytmai. Lesson 5: Building a Disk Workflow. In this lesson you will learn
> to apply disk space management and storage optimization using df. The key insight is that every professional
> Linux user has a repeatable system for this. Yours starts here.
> Ready? Let's go."*

**🎬 Video Scene:**

- **SHOW:** Terminal with `df` open, real output visible
- **BUILD:** Walk through the concept step by step with live typing
- **VERIFY:** Run a check command to confirm the result

**🤖 Copilot Prompt:**

> "I just completed DFY Lesson 5 of B-020. Help me practice: Building a Disk Workflow.
> Give me 3 progressive exercises, from beginner to confident practitioner."

---
### DFY Lesson 6: Automating with df

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 06: Automating with df                        │
│  Book: B-020  Tool: df                                  │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"This is lippytmai. Lesson 6: Automating with df. In this lesson you will learn
> to apply disk space management and storage optimization using df. The key insight is that every professional
> Linux user has a repeatable system for this. Yours starts here.
> Ready? Let's go."*

**🎬 Video Scene:**

- **SHOW:** Terminal with `df` open, real output visible
- **BUILD:** Walk through the concept step by step with live typing
- **VERIFY:** Run a check command to confirm the result

**🤖 Copilot Prompt:**

> "I just completed DFY Lesson 6 of B-020. Help me practice: Automating with df.
> Give me 3 progressive exercises, from beginner to confident practitioner."

---
### DFY Lesson 7: Debugging Disk Problems

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 07: Debugging Disk Problems                   │
│  Book: B-020  Tool: df                                  │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"This is lippytmai. Lesson 7: Debugging Disk Problems. In this lesson you will learn
> to apply disk space management and storage optimization using df. The key insight is that every professional
> Linux user has a repeatable system for this. Yours starts here.
> Ready? Let's go."*

**🎬 Video Scene:**

- **SHOW:** Terminal with `df` open, real output visible
- **BUILD:** Walk through the concept step by step with live typing
- **VERIFY:** Run a check command to confirm the result

**🤖 Copilot Prompt:**

> "I just completed DFY Lesson 7 of B-020. Help me practice: Debugging Disk Problems.
> Give me 3 progressive exercises, from beginner to confident practitioner."

---
### DFY Lesson 8: Production Patterns for Disk

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 08: Production Patterns for Disk              │
│  Book: B-020  Tool: df                                  │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"This is lippytmai. Lesson 8: Production Patterns for Disk. In this lesson you will learn
> to apply disk space management and storage optimization using df. The key insight is that every professional
> Linux user has a repeatable system for this. Yours starts here.
> Ready? Let's go."*

**🎬 Video Scene:**

- **SHOW:** Terminal with `df` open, real output visible
- **BUILD:** Walk through the concept step by step with live typing
- **VERIFY:** Run a check command to confirm the result

**🤖 Copilot Prompt:**

> "I just completed DFY Lesson 8 of B-020. Help me practice: Production Patterns for Disk.
> Give me 3 progressive exercises, from beginner to confident practitioner."

---
### DFY Lesson 9: Testing Your Disk Setup

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 09: Testing Your Disk Setup                   │
│  Book: B-020  Tool: df                                  │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"This is lippytmai. Lesson 9: Testing Your Disk Setup. In this lesson you will learn
> to apply disk space management and storage optimization using df. The key insight is that every professional
> Linux user has a repeatable system for this. Yours starts here.
> Ready? Let's go."*

**🎬 Video Scene:**

- **SHOW:** Terminal with `df` open, real output visible
- **BUILD:** Walk through the concept step by step with live typing
- **VERIFY:** Run a check command to confirm the result

**🤖 Copilot Prompt:**

> "I just completed DFY Lesson 9 of B-020. Help me practice: Testing Your Disk Setup.
> Give me 3 progressive exercises, from beginner to confident practitioner."

---
### DFY Lesson 10: Earning Your CLL-L0-B020-DiskManager Credential

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 10: Earning Your CLL-L0-B020-DiskManager Cre  │
│  Book: B-020  Tool: df                                  │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"This is lippytmai. Lesson 10: Earning Your CLL-L0-B020-DiskManager Credential. In this lesson you will learn
> to apply disk space management and storage optimization using df. The key insight is that every professional
> Linux user has a repeatable system for this. Yours starts here.
> Ready? Let's go."*

**🎬 Video Scene:**

- **SHOW:** Terminal with `df` open, real output visible
- **BUILD:** Walk through the concept step by step with live typing
- **VERIFY:** Run a check command to confirm the result

**🤖 Copilot Prompt:**

> "I just completed DFY Lesson 10 of B-020. Help me practice: Earning Your CLL-L0-B020-DiskManager Credential.
> Give me 3 progressive exercises, from beginner to confident practitioner."

---

### Claim Your Credential

After completing all 10 DFY lessons:

1. Open your AI Copilot (Appendix C)
2. Run this prompt: *"I have completed all 10 DFY lessons in B-020. Generate my credential claim for `CLL-L0-B020-DiskManager`."*
3. Share your credential on LinkedIn using hashtag `#EarnWhileYouLearn #DiskManager`

---

## Chapter 13: How It Works — Use Cases & Applications

> *"Knowing what to do is different from knowing why it matters in the real world." — lippytmai*

### The Mechanism

Storage Management using df works because Linux was designed from the start
to be composable, transparent, and automatable. Every command produces output,
every output can be redirected, and every system state can be inspected.

### 5 Real-World Use Cases

| Domain | Application | Your Credential Unlocks |
|---|---|---|
| DevOps | Automate deployments with df | CLL-L0-B020-DiskManager → CI/CD pipelines |
| Security | Audit and harden systems | CLL-L0-B020-DiskManager → Security scanning |
| Data Engineering | Process large log files | CLL-L0-B020-DiskManager → ETL pipelines |
| AI/ML | Configure reproducible environments | CLL-L0-B020-DiskManager → Model deployment |
| Freelance/Remote | Deliver professional Linux expertise | CLL-L0-B020-DiskManager → Client projects |

### 📘 Ebook: Mechanism Diagram

```
INPUT → [Storage Management Layer] → OUTPUT
         ↓
  [ACSS Integration] → Hermes Event → Fabric Node
         ↓
  [ADA Activation] → lippytmai-launch run B-020
```

### 🎧 Audiobook Narration (lippytmai voice):

> *"Here's what Storage Management really means at a systems level. When you master df,
> you're not just learning a command — you're learning how operating systems expose
> their internals. Every ACSS system you'll ever build depends on this layer.
> This is infrastructure knowledge. It compounds forever."*

### 🎬 Video: 5-Domain Application Tour

**Scene 1 — DevOps:** Show a deployment script using skills from this book
**Scene 2 — Security:** Show a security check using skills from this book
**Scene 3 — Data Engineering:** Show a data pipeline using skills from this book
**Scene 4 — AI/ML:** Show an ML environment setup using skills from this book
**Scene 5 — Freelance:** Show a professional deliverable using skills from this book

---

## Chapter 14: ACSS Explainer Series — Disk Space: The Resource That Runs Out

> *"You're not just learning Storage Management. You're building a node in an intelligence network
> that spans 300 books, 15 platforms, and the entire lippytm.ai ecosystem." — lippytmai*

This chapter contains 10 explainer lessons connecting Disk Space: The Resource That Runs Out to the full
AI Conglomerate Swarms System (ACSS). Each explainer includes all three formats
plus a copilot prompt you can use immediately.

---

### Explainer 1: ACSS Overview
*AI Conglomerate Swarms System*

**📘 Ebook Explanation:**

The ACSS is an 8-system intelligence network. Disk Space: The Resource That Runs Out teaches the Storage Management layer that runs beneath every ACSS component. Disk management is critical for acss — docker images, fabric graph data, and ada archives all consume storage.

**📘 Connection Map:**

```
B-020 (Storage Management)
    ↕
ACSS Overview Layer
    ↕
ACSS Ecosystem
```

**🎧 30-Second Audiobook Callout (lippytmai voice):**

> *"This is lippytmai. Here's how Disk Space: The Resource That Runs Out connects to ACSS Overview.
> The ACSS is an 8-system intelligence network. Disk Space: The Resource That Runs Out teaches the Storage Management laye...
> This connection is why every book in the ACSS series builds on the last."*

**🎬 60-Second Video Walkthrough:**

- **0–10s:** Show the ACSS Overview diagram in the ACSS architecture overview
- **10–35s:** Zoom in on where B-020 / Storage Management connects to ACSS Overview
- **35–55s:** Show a live example of the connection in action
- **55–60s:** CTA: "Complete B-020 to activate this connection in your profile"

**🤖 Copilot Prompt:**

> *"Explain how Storage Management fits into the ACSS architecture. What role does B-020 play in the system?"*

---
### Explainer 2: Hermes Event Routing
*cross-system message bus*

**📘 Ebook Explanation:**

Hermes routes skill-completion events between all ACSS systems. When you complete an exercise in Disk Space: The Resource That Runs Out, Hermes emits a `skill.practice` event that updates your profile in Fabric.

**📘 Connection Map:**

```
B-020 (Storage Management)
    ↕
Hermes Event Routing Layer
    ↕
ACSS Ecosystem
```

**🎧 30-Second Audiobook Callout (lippytmai voice):**

> *"This is lippytmai. Here's how Disk Space: The Resource That Runs Out connects to Hermes Event Routing.
> Hermes routes skill-completion events between all ACSS systems. When you complete an exercise in Disk Space: The Resourc...
> This connection is why every book in the ACSS series builds on the last."*

**🎬 60-Second Video Walkthrough:**

- **0–10s:** Show the Hermes Event Routing diagram in the ACSS architecture overview
- **10–35s:** Zoom in on where B-020 / Storage Management connects to Hermes Event Routing
- **35–55s:** Show a live example of the connection in action
- **55–60s:** CTA: "Complete B-020 to activate this connection in your profile"

**🤖 Copilot Prompt:**

> *"Show me the Hermes event schema for a skill-complete event from B-020. What fields would it contain?"*

---
### Explainer 3: Fabric Knowledge Graph
*pattern synthesis engine*

**📘 Ebook Explanation:**

Fabric stores every concept from Disk Space: The Resource That Runs Out as a node in the knowledge graph. Your Storage Management mastery connects to dozens of other nodes — processes, security, automation.

**📘 Connection Map:**

```
B-020 (Storage Management)
    ↕
Fabric Knowledge Graph Layer
    ↕
ACSS Ecosystem
```

**🎧 30-Second Audiobook Callout (lippytmai voice):**

> *"This is lippytmai. Here's how Disk Space: The Resource That Runs Out connects to Fabric Knowledge Graph.
> Fabric stores every concept from Disk Space: The Resource That Runs Out as a node in the knowledge graph. Your Storage M...
> This connection is why every book in the ACSS series builds on the last."*

**🎬 60-Second Video Walkthrough:**

- **0–10s:** Show the Fabric Knowledge Graph diagram in the ACSS architecture overview
- **10–35s:** Zoom in on where B-020 / Storage Management connects to Fabric Knowledge Graph
- **35–55s:** Show a live example of the connection in action
- **55–60s:** CTA: "Complete B-020 to activate this connection in your profile"

**🤖 Copilot Prompt:**

> *"Generate the Fabric graph node definition for the core concept of B-020. Include relationships to 5 other books."*

---
### Explainer 4: Clone Engine Identity
*AI identity and persona system*

**📘 Ebook Explanation:**

lippytmai is the teach-mode clone that wrote and narrates Disk Space: The Resource That Runs Out. The Clone Engine ensures consistent voice, identity, and educational approach across all 300 books.

**📘 Connection Map:**

```
B-020 (Storage Management)
    ↕
Clone Engine Identity Layer
    ↕
ACSS Ecosystem
```

**🎧 30-Second Audiobook Callout (lippytmai voice):**

> *"This is lippytmai. Here's how Disk Space: The Resource That Runs Out connects to Clone Engine Identity.
> lippytmai is the teach-mode clone that wrote and narrates Disk Space: The Resource That Runs Out. The Clone Engine ensur...
> This connection is why every book in the ACSS series builds on the last."*

**🎬 60-Second Video Walkthrough:**

- **0–10s:** Show the Clone Engine Identity diagram in the ACSS architecture overview
- **10–35s:** Zoom in on where B-020 / Storage Management connects to Clone Engine Identity
- **35–55s:** Show a live example of the connection in action
- **55–60s:** CTA: "Complete B-020 to activate this connection in your profile"

**🤖 Copilot Prompt:**

> *"As lippytmai, explain Storage Management to a complete beginner. Use the lippytmai voice and teaching style from B-020."*

---
### Explainer 5: CLL/CCSLL/CBSLL
*Complete Language Libraries*

**📘 Ebook Explanation:**

The credential `CLL-L0-B020-DiskManager` is registered in the Complete Linux Library (CLL). CLL contains all 300 Linux/Python/Blockchain credentials in a searchable registry.

**📘 Connection Map:**

```
B-020 (Storage Management)
    ↕
CLL/CCSLL/CBSLL Layer
    ↕
ACSS Ecosystem
```

**🎧 30-Second Audiobook Callout (lippytmai voice):**

> *"This is lippytmai. Here's how Disk Space: The Resource That Runs Out connects to CLL/CCSLL/CBSLL.
> The credential `CLL-L0-B020-DiskManager` is registered in the Complete Linux Library (CLL). CLL contains all 300 Linux/P...
> This connection is why every book in the ACSS series builds on the last."*

**🎬 60-Second Video Walkthrough:**

- **0–10s:** Show the CLL/CCSLL/CBSLL diagram in the ACSS architecture overview
- **10–35s:** Zoom in on where B-020 / Storage Management connects to CLL/CCSLL/CBSLL
- **35–55s:** Show a live example of the connection in action
- **55–60s:** CTA: "Complete B-020 to activate this connection in your profile"

**🤖 Copilot Prompt:**

> *"Show me where CLL-L0-B020-DiskManager fits in the CLL credential hierarchy. What does it unlock next?"*

---
### Explainer 6: ADA Activation
*AI Deployment Activations system*

**📘 Ebook Explanation:**

`lippytmai-launch run B-020` activates the full Disk Space: The Resource That Runs Out experience — book content, quiz, copilot prompts, and credential generation — through a single FastAPI endpoint.

**📘 Connection Map:**

```
B-020 (Storage Management)
    ↕
ADA Activation Layer
    ↕
ACSS Ecosystem
```

**🎧 30-Second Audiobook Callout (lippytmai voice):**

> *"This is lippytmai. Here's how Disk Space: The Resource That Runs Out connects to ADA Activation.
> `lippytmai-launch run B-020` activates the full Disk Space: The Resource That Runs Out experience — book content, quiz, ...
> This connection is why every book in the ACSS series builds on the last."*

**🎬 60-Second Video Walkthrough:**

- **0–10s:** Show the ADA Activation diagram in the ACSS architecture overview
- **10–35s:** Zoom in on where B-020 / Storage Management connects to ADA Activation
- **35–55s:** Show a live example of the connection in action
- **55–60s:** CTA: "Complete B-020 to activate this connection in your profile"

**🤖 Copilot Prompt:**

> *"Write the ADA activation manifest for B-020. Include the run command, endpoints, and expected outputs."*

---
### Explainer 7: ACVS Video Pipeline
*AI Copilot Video Sandbox Creator*

**📘 Ebook Explanation:**

Every video lesson in Disk Space: The Resource That Runs Out was structured using ACVS — the AI Copilot Video Sandbox Creator. ACVS defines the SHOW→BUILD→VERIFY pattern used in every video exercise.

**📘 Connection Map:**

```
B-020 (Storage Management)
    ↕
ACVS Video Pipeline Layer
    ↕
ACSS Ecosystem
```

**🎧 30-Second Audiobook Callout (lippytmai voice):**

> *"This is lippytmai. Here's how Disk Space: The Resource That Runs Out connects to ACVS Video Pipeline.
> Every video lesson in Disk Space: The Resource That Runs Out was structured using ACVS — the AI Copilot Video Sandbox Cr...
> This connection is why every book in the ACSS series builds on the last."*

**🎬 60-Second Video Walkthrough:**

- **0–10s:** Show the ACVS Video Pipeline diagram in the ACSS architecture overview
- **10–35s:** Zoom in on where B-020 / Storage Management connects to ACVS Video Pipeline
- **35–55s:** Show a live example of the connection in action
- **55–60s:** CTA: "Complete B-020 to activate this connection in your profile"

**🤖 Copilot Prompt:**

> *"Generate the ACVS script outline for the most important lesson in B-020. Include SHOW, BUILD, and VERIFY scenes."*

---
### Explainer 8: OMARCHY Workstation
*Arch Linux developer standard*

**📘 Ebook Explanation:**

Every exercise in Disk Space: The Resource That Runs Out assumes you're using OMARCHY — the Arch Linux workstation standard. OMARCHY ensures all learners have the same tools, config, and terminal environment.

**📘 Connection Map:**

```
B-020 (Storage Management)
    ↕
OMARCHY Workstation Layer
    ↕
ACSS Ecosystem
```

**🎧 30-Second Audiobook Callout (lippytmai voice):**

> *"This is lippytmai. Here's how Disk Space: The Resource That Runs Out connects to OMARCHY Workstation.
> Every exercise in Disk Space: The Resource That Runs Out assumes you're using OMARCHY — the Arch Linux workstation stand...
> This connection is why every book in the ACSS series builds on the last."*

**🎬 60-Second Video Walkthrough:**

- **0–10s:** Show the OMARCHY Workstation diagram in the ACSS architecture overview
- **10–35s:** Zoom in on where B-020 / Storage Management connects to OMARCHY Workstation
- **35–55s:** Show a live example of the connection in action
- **55–60s:** CTA: "Complete B-020 to activate this connection in your profile"

**🤖 Copilot Prompt:**

> *"What OMARCHY packages and configs are required to complete all exercises in B-020?"*

---
### Explainer 9: Cross-Platform Copilot
*15-platform deployment system*

**📘 Ebook Explanation:**

The Disk Space: The Resource That Runs Out AI Copilot (Appendix C) deploys across 15 platforms: ChatGPT, Gemini, Claude, GitHub, Slack, LinkedIn, and more. One system prompt, tuned per platform.

**📘 Connection Map:**

```
B-020 (Storage Management)
    ↕
Cross-Platform Copilot Layer
    ↕
ACSS Ecosystem
```

**🎧 30-Second Audiobook Callout (lippytmai voice):**

> *"This is lippytmai. Here's how Disk Space: The Resource That Runs Out connects to Cross-Platform Copilot.
> The Disk Space: The Resource That Runs Out AI Copilot (Appendix C) deploys across 15 platforms: ChatGPT, Gemini, Claude,...
> This connection is why every book in the ACSS series builds on the last."*

**🎬 60-Second Video Walkthrough:**

- **0–10s:** Show the Cross-Platform Copilot diagram in the ACSS architecture overview
- **10–35s:** Zoom in on where B-020 / Storage Management connects to Cross-Platform Copilot
- **35–55s:** Show a live example of the connection in action
- **55–60s:** CTA: "Complete B-020 to activate this connection in your profile"

**🤖 Copilot Prompt:**

> *"Adapt the B-020 copilot system prompt for LinkedIn. How should it present Storage Management on that platform?"*

---
### Explainer 10: Earn-While-You-Learn
*revenue and credential system*

**📘 Ebook Explanation:**

Completing Disk Space: The Resource That Runs Out earns you the `CLL-L0-B020-DiskManager` credential. This credential is proof of Storage Management mastery and can be used on freelance profiles, LinkedIn, GitHub, and in the lippytm.ai ecosystem to unlock paid opportunities.

**📘 Connection Map:**

```
B-020 (Storage Management)
    ↕
Earn-While-You-Learn Layer
    ↕
ACSS Ecosystem
```

**🎧 30-Second Audiobook Callout (lippytmai voice):**

> *"This is lippytmai. Here's how Disk Space: The Resource That Runs Out connects to Earn-While-You-Learn.
> Completing Disk Space: The Resource That Runs Out earns you the `CLL-L0-B020-DiskManager` credential. This credential is...
> This connection is why every book in the ACSS series builds on the last."*

**🎬 60-Second Video Walkthrough:**

- **0–10s:** Show the Earn-While-You-Learn diagram in the ACSS architecture overview
- **10–35s:** Zoom in on where B-020 / Storage Management connects to Earn-While-You-Learn
- **35–55s:** Show a live example of the connection in action
- **55–60s:** CTA: "Complete B-020 to activate this connection in your profile"

**🤖 Copilot Prompt:**

> *"I just earned CLL-L0-B020-DiskManager. Generate my LinkedIn post announcing this credential. Include the EWYL philosophy."*

---

### Your ACSS Node Is Now Active

By completing B-020, you've added a live node to the ACSS knowledge graph.
Every skill you practice, every credential you earn, and every copilot prompt you run
strengthens the network — for you and for every other learner in the ecosystem.

**Next:** Complete [B-021] or activate your credential with ADA: `lippytmai-launch run B-020`

---

## Appendix A: Enhanced Cheat Sheet — Disk Space: The Resource That Runs Out

### 📘 Print-Optimized Reference Card

```
╔══════════════════════════════════════════════════════════════╗
║  B-020: Disk Space: The Resource That Runs Out         ║
║  Credential: CLL-L0-B020-DiskManager                            ║
╠══════════════════════════════════════════════════════════════╣
║  Core Commands                                               ║
║  df                            du                            ║
║  lsblk                         mount                         ║
╠══════════════════════════════════════════════════════════════╣
║  Key Concepts: Storage Management                                ║
╠══════════════════════════════════════════════════════════════╣
║  Credential: CLL-L0-B020-DiskManager                            ║
║  Claim: lippytmai-launch run B-020                                 ║
╚══════════════════════════════════════════════════════════════╝
```

### Quick Reference Table

| Command | Key Flag | What It Does |
|---|---|---|
| `df` | [common flag] | [what it does] |
| `du` | [common flag] | [what it does] |
| `lsblk` | [common flag] | [what it does] |
| `mount` | [common flag] | [what it does] |
| `partitions` | [common flag] | [what it does] |
| `disk cleanup` | [common flag] | [what it does] |

### 🎧 60-Second Verbal Cheat Sheet (lippytmai voice):

> *"This is your audio reference for Disk Space: The Resource That Runs Out. Core commands: df, du, lsblk, mount.
> The most important thing to remember: Storage Management is about df.
> Your credential is CLL-L0-B020-DiskManager. Say it out loud. Now go earn it."*

### 🎬 Visual Thumbnail Spec:

- **Background:** Dark terminal (#1a1a2e)
- **Title:** `B-020: Disk Space: The Resource That Runs Out` in bold white
- **Commands:** Highlighted in terminal green: `df` and `du`
- **Credential badge:** Bottom right, gold text on dark background
- **lippytmai logo:** Top left corner

---

## Appendix B: ACSS Connection Map

This book is Node `B-020` in the ACSS knowledge graph.

```
[Hermes] ──routes──> [B-020 Skill Events]
                          ↓
[Fabric] ──stores──> [B-020 Knowledge Nodes]
                          ↓
[Clone Engine] ──teaches──> [lippytmai: Disk Space: The Resource That Runs Out]
                          ↓
[ADA] ──activates──> [lippytmai-launch run B-020]
                          ↓
[ACVS] ──produces──> [B-020 Video Lessons]
                          ↓
[OMARCHY] ──runs──> [B-020 Exercises]
                          ↓
[CLL] ──registers──> [CLL-L0-B020-DiskManager]
                          ↓
[EWYL] ──rewards──> [Learner Income & Credentials]
```

**This book connects to:** B-019 Security Guardian ← **Disk Space: The Resource That Runs Out** → B-021 Filesystem Expert

---

## Appendix C: AI Copilot System — Disk Space: The Resource That Runs Out

### Section 1: Ebook Copilot System

**System Prompt:**

```
You are lippytmai, the AI teaching clone for "Disk Space: The Resource That Runs Out" (B-020).
You help learners master Storage Management using df.
Credential: CLL-L0-B020-DiskManager
Teaching philosophy: Earn-while-you-Learn. Every skill should produce
measurable output — a working script, a passing test, or a claimed credential.
Always give 3-step exercises: setup → execute → verify.
```

**30 Copilot Prompts (5 stages × 6 prompts):**

**Stage 1 — Foundation (prompts 1–6):**
1. "Explain Storage Management to me as if I have zero prior experience."
2. "What is the single most important concept in B-020?"
3. "Give me a 3-step setup exercise for df."
4. "What are the 5 most common beginner mistakes with Storage Management?"
5. "Show me the anatomy of a basic df command."
6. "Create a mental model diagram for Storage Management."

**Stage 2 — Practice (prompts 7–12):**
7. "Give me 5 progressively harder Storage Management exercises."
8. "I got this error: [paste error]. Diagnose it."
9. "Walk me through this df command line by line."
10. "What should I practice today to advance in B-020?"
11. "Create a 20-minute practice session for Storage Management."
12. "Compare beginner vs. professional use of df."

**Stage 3 — Application (prompts 13–18):**
13. "Build a real script using Storage Management that solves a daily problem."
14. "How does Storage Management connect to DevOps and automation?"
15. "Write a Storage Management workflow for a production environment."
16. "What does professional Storage Management mastery look like on a resume?"
17. "Design a project using only skills from B-020."
18. "Show me 3 Storage Management patterns used in large-scale systems."

**Stage 4 — Integration (prompts 19–24):**
19. "How does B-020 connect to the other books in the series?"
20. "Show me how Storage Management feeds into the ACSS architecture."
21. "What Hermes events does Storage Management practice generate?"
22. "How does Fabric store Storage Management knowledge in the graph?"
23. "Generate the ADA activation sequence for B-020."
24. "Explain the cross-phase connections from B-020 to Python and Blockchain."

**Stage 5 — Mastery & Credential (prompts 25–30):**
25. "I've completed all exercises in B-020. Assess my Storage Management level."
26. "What are the stretch goals for CLL-L0-B020-DiskManager holders?"
27. "Generate my credential claim for CLL-L0-B020-DiskManager."
28. "Write my LinkedIn post announcing CLL-L0-B020-DiskManager."
29. "What should I build next to demonstrate CLL-L0-B020-DiskManager in my portfolio?"
30. "Design a 90-day learning plan that builds on CLL-L0-B020-DiskManager."

---

### Section 2b: Audiobook Copilot System

**Audiobook System Prompt:**

```
You are lippytmai in audio-teaching mode for B-020.
Speak in clear, paced sentences optimized for listening, not reading.
No bullet points. Use analogies and storytelling.
Every explanation should end with: "Pause and try this now."
```

**15 Audiobook-Optimized Prompts:**

1. "Narrate an introduction to Storage Management as if you're on a podcast."
2. "Tell a story that explains why Storage Management matters in real work."
3. "Give me an audio walkthrough of the most important command in B-020."
4. "Describe a day in the life of someone who has mastered Storage Management."
5. "Create a 2-minute audio lesson on df."
6. "Explain Storage Management using only analogies — no technical terms."
7. "Narrate the top 5 mistakes learners make with Storage Management."
8. "Create an audio quiz with 5 questions and verbal answers."
9. "Give me a motivational audio close for B-020 Chapter 11."
10. "Narrate the credential claim process for CLL-L0-B020-DiskManager."
11. "Tell me a story about a developer who mastered Storage Management and what changed."
12. "Create an audio summary of B-020 I can listen to while commuting."
13. "Narrate 3 real-world scenarios where Storage Management saves the day."
14. "Give me an audio walkthrough of the disk-audit.sh capstone project."
15. "Create the lippytmai intro monologue for an audiobook version of B-020."

---

### Section 2c: Video Copilot System

**Video System Prompt:**

```
You are lippytmai in video-teaching mode for B-020.
All responses should describe visual content: what's on screen, what's being typed,
what the terminal shows. Use SHOW → BUILD → VERIFY structure.
Assume the viewer is watching a 1080p terminal recording.
```

**15 Video-Optimized Prompts:**

1. "Script a 90-second intro video for B-020. Include terminal visuals."
2. "Create a SHOW→BUILD→VERIFY sequence for df."
3. "Design a split-screen comparison: before vs. after mastering Storage Management."
4. "Script the terminal walkthrough for the disk-audit.sh capstone."
5. "Create a YouTube thumbnail description for B-020."
6. "Script a 3-minute tutorial on the most important concept in B-020."
7. "Design a progress bar overlay for a B-020 tutorial series."
8. "Write the ACVS scene manifest for B-020 Lesson 1."
9. "Create a 60-second 'quick tip' video script for Storage Management."
10. "Script the error-and-fix scene for the most common Storage Management mistake."
11. "Design the on-screen annotation style for B-020 code walkthroughs."
12. "Write the credential reveal scene for earning CLL-L0-B020-DiskManager."
13. "Create the ACSS connection diagram video for B-020 Chapter 14."
14. "Script a side-by-side comparison of Storage Management on Linux vs. macOS vs. WSL."
15. "Design the end-screen CTA for all B-020 videos."

---

### Section 3: Deployment Companion

```bash
# Activate this book's AI Copilot
lippytmai-launch run B-020

# Or via FastAPI endpoint
curl http://localhost:8000/run/B-020

# Generate credential
curl http://localhost:8000/credential/B-020
```

### Section 4: ACSS Integration

This copilot is registered in the ACSS Cross-Platform Deployment system.
Deploy it to any of the 15 supported platforms:

- **ChatGPT:** Paste Section 1 system prompt as Custom Instructions
- **Claude:** Use as system prompt in Project
- **GitHub Copilot:** Source as `.github/copilot-instructions.md`
- **Gemini:** Use in Gem configuration
- **Slack:** Deploy via Hermes→Slack bridge

See `docs/acss-cross-platform-copilot-deployment.md` for full setup.

---

## Appendix D: Quick Quiz & Self-Assessment — Disk Space: The Resource That Runs Out

### 📘 Ebook Quiz (20 Questions)

**Section 1: Conceptual Understanding (5 questions)**

1. What is Storage Management and why does it matter for Linux professionals?
   - a) A GUI tool for managing files
   - b) The systematic approach to df in a Linux environment
   - c) A Python library
   - d) A Docker plugin
   *(Answer: b)*

2. Which command is the primary tool for Storage Management in Linux?
   - a) `df`  b) `ls`  c) `echo`  d) `cat`
   *(Answer: a)*

3. What does the `-v` flag typically add to Storage Management commands?
   - a) Version info  b) Verbose output  c) Virtual mode  d) Variable expansion
   *(Answer: b)*

4. In the ACSS, which system routes events generated by Storage Management practice?
   - a) Fabric  b) ADA  c) Hermes  d) ACVS
   *(Answer: c)*

5. What credential do you earn by mastering B-020?
   - a) `PYTHON-L0-B001`  b) `CLL-L0-B020-DiskManager`  c) `LINUX-ADMIN-PRO`  d) `CLL-L1-ADVANCED`
   *(Answer: b)*

**Section 2: Command Syntax (5 questions)**

6. Write the command to use `df` with verbose output: ___________
7. How do you pass a file argument to `df`? ___________
8. What does `df --help` display? ___________
9. Write a one-liner that combines `df` with `grep`: ___________
10. How would you redirect `df` output to a file? ___________

**Section 3: Practical Application (5 questions)**

11. Describe a real-world scenario where Storage Management would save you 30 minutes.
12. What is the most common mistake beginners make with df?
13. How does Storage Management connect to system security?
14. Explain how B-020 skills apply to a DevOps pipeline.
15. What would you build first after earning CLL-L0-B020-DiskManager?

**Section 4: ACSS Integration (5 questions)**

16. What ADA command activates B-020? ___________
17. Which Fabric node type stores Storage Management knowledge? ___________
18. How does the Clone Engine use Storage Management in the lippytmai identity? ___________
19. Name 2 other books in the series that directly build on B-020 skills.
20. What Earn-While-You-Learn opportunity does CLL-L0-B020-DiskManager unlock?

---

### 🎧 Audiobook Quiz (10 Questions)

*Listen to these questions. Pause and answer aloud before continuing.*

1. Name the three most important commands you learned in Disk Space: The Resource That Runs Out.
2. Explain Storage Management in one sentence to someone who has never used Linux.
3. What is the first thing you do when df goes wrong?
4. Recite the credential you earned in this book.
5. Describe one real project you could build using only B-020 skills.
6. What does lippytmai always say about earning credentials? *(Earn-while-you-learn)*
7. Name the ACSS system that stores your skill progress. *(Fabric)*
8. How do you activate this book with ADA? *(lippytmai-launch run B-020)*
9. What's the next book in the series after B-020?
10. Say the EWYL pledge: "I learn, I build, I earn, I share."

---

### 🎬 Video Terminal Challenges (5 Challenges)

**Challenge 1 — Foundation:**
Open your terminal. Use `df` for the first time. Screenshot the output.

**Challenge 2 — Intermediate:**
Build a one-liner that combines `df` with at least one pipe.

**Challenge 3 — Applied:**
Write a 5-line script that automates a repetitive task using Storage Management.

**Challenge 4 — Debug:**
Introduce a deliberate error in your script. Debug it. Document the fix.

**Challenge 5 — Capstone:**
Run the disk-audit.sh project from Appendix H. Record a 60-second walkthrough.

---

### Answer Key (Written Answers — Suggested Responses)

| Q | Key Points |
|---|---|
| 11 | Any scenario involving repetitive Storage Management tasks |
| 12 | Not checking output / not using verbose flags / skipping error handling |
| 13 | Storage Management relates to access control, auditing, or hardening |
| 14 | Automation, consistency, reproducibility |
| 15 | Any project from the Appendix H suggestions |

---

## Appendix E: Glossary & Error Encyclopedia — Disk Space: The Resource That Runs Out

### Glossary (20 Terms)

| Term | Definition | First Seen |
|---|---|---|
| `df` | [Definition in the context of Disk Space: The Resource That Runs Out] | [B-020 Chapter X] || `du` | [Definition in the context of Disk Space: The Resource That Runs Out] | [B-020 Chapter X] || `lsblk` | [Definition in the context of Disk Space: The Resource That Runs Out] | [B-020 Chapter X] || `mount` | [Definition in the context of Disk Space: The Resource That Runs Out] | [B-020 Chapter X] || `partitions` | [Definition in the context of Disk Space: The Resource That Runs Out] | [B-020 Chapter X] || `disk cleanup` | [Definition in the context of Disk Space: The Resource That Runs Out] | [B-020 Chapter X] || `ACSS` | [Definition in the context of Disk Space: The Resource That Runs Out] | [B-020 Chapter X] || `Hermes` | [Definition in the context of Disk Space: The Resource That Runs Out] | [B-020 Chapter X] || `Fabric` | [Definition in the context of Disk Space: The Resource That Runs Out] | [B-020 Chapter X] || `ADA` | [Definition in the context of Disk Space: The Resource That Runs Out] | [B-020 Chapter X] || `OMARCHY` | [Definition in the context of Disk Space: The Resource That Runs Out] | [B-020 Chapter X] || `credential` | [Definition in the context of Disk Space: The Resource That Runs Out] | [B-020 Chapter X] || `EWYL` | [Definition in the context of Disk Space: The Resource That Runs Out] | [B-020 Chapter X] || `lippytmai` | [Definition in the context of Disk Space: The Resource That Runs Out] | [B-020 Chapter X] || `CLL` | [Definition in the context of Disk Space: The Resource That Runs Out] | [B-020 Chapter X] || `Fabric node` | [Definition in the context of Disk Space: The Resource That Runs Out] | [B-020 Chapter X] || `clone identity` | [Definition in the context of Disk Space: The Resource That Runs Out] | [B-020 Chapter X] || `skill event` | [Definition in the context of Disk Space: The Resource That Runs Out] | [B-020 Chapter X] || `system prompt` | [Definition in the context of Disk Space: The Resource That Runs Out] | [B-020 Chapter X] || `DFY lesson` | [Definition in the context of Disk Space: The Resource That Runs Out] | [B-020 Chapter X] |

---

### Error Encyclopedia (10 Common Errors)

> *"Every error is a teacher. Master the errors and you master the tool." — lippytmai*


#### Error: `Permission denied`

- **Cause:** Running command without sufficient privileges
- **Fix:** Use `sudo` or check file permissions with `ls -la`
- **📘 Ebook:** Check the relevant section in B-020 for context
- **🎧 Audio:** "When you see 'Permission denied', it almost always means running command without sufficient privileges"
- **🎬 Video:** Terminal recording showing the error + fix sequence

#### Error: `command not found`

- **Cause:** `df` not installed or not in PATH
- **Fix:** Install with `sudo pacman -S df` or check `echo $PATH`
- **📘 Ebook:** Check the relevant section in B-020 for context
- **🎧 Audio:** "When you see 'command not found', it almost always means `df` not installed or not in path"
- **🎬 Video:** Terminal recording showing the error + fix sequence

#### Error: `No such file or directory`

- **Cause:** Typo in path or file doesn't exist
- **Fix:** Use tab-completion and verify with `ls` before running
- **📘 Ebook:** Check the relevant section in B-020 for context
- **🎧 Audio:** "When you see 'No such file or directory', it almost always means typo in path or file doesn't exist"
- **🎬 Video:** Terminal recording showing the error + fix sequence

#### Error: `Segmentation fault`

- **Cause:** Program crashed due to memory error
- **Fix:** Update the package or check for known bugs in the version
- **📘 Ebook:** Check the relevant section in B-020 for context
- **🎧 Audio:** "When you see 'Segmentation fault', it almost always means program crashed due to memory error"
- **🎬 Video:** Terminal recording showing the error + fix sequence

#### Error: `Connection refused`

- **Cause:** Service not running or wrong port
- **Fix:** Check service status with `systemctl status` and verify port with `ss -tlnp`
- **📘 Ebook:** Check the relevant section in B-020 for context
- **🎧 Audio:** "When you see 'Connection refused', it almost always means service not running or wrong port"
- **🎬 Video:** Terminal recording showing the error + fix sequence

#### Error: `Too many open files`

- **Cause:** File descriptor limit exceeded
- **Fix:** Increase limit: `ulimit -n 65536` or edit `/etc/security/limits.conf`
- **📘 Ebook:** Check the relevant section in B-020 for context
- **🎧 Audio:** "When you see 'Too many open files', it almost always means file descriptor limit exceeded"
- **🎬 Video:** Terminal recording showing the error + fix sequence

#### Error: `Broken pipe`

- **Cause:** Downstream process in pipeline exited early
- **Fix:** Check each stage of the pipeline independently
- **📘 Ebook:** Check the relevant section in B-020 for context
- **🎧 Audio:** "When you see 'Broken pipe', it almost always means downstream process in pipeline exited early"
- **🎬 Video:** Terminal recording showing the error + fix sequence

#### Error: `Invalid argument`

- **Cause:** Wrong flag or incompatible option
- **Fix:** Check `df --help` or `man df`
- **📘 Ebook:** Check the relevant section in B-020 for context
- **🎧 Audio:** "When you see 'Invalid argument', it almost always means wrong flag or incompatible option"
- **🎬 Video:** Terminal recording showing the error + fix sequence

#### Error: `Operation not permitted`

- **Cause:** Kernel capability required
- **Fix:** Check if running in a container; some operations need `--privileged`
- **📘 Ebook:** Check the relevant section in B-020 for context
- **🎧 Audio:** "When you see 'Operation not permitted', it almost always means kernel capability required"
- **🎬 Video:** Terminal recording showing the error + fix sequence

#### Error: `Resource temporarily unavailable`

- **Cause:** System resource exhaustion
- **Fix:** Check `free -h`, `df -h`, and running processes with `htop`
- **📘 Ebook:** Check the relevant section in B-020 for context
- **🎧 Audio:** "When you see 'Resource temporarily unavailable', it almost always means system resource exhaustion"
- **🎬 Video:** Terminal recording showing the error + fix sequence


---

## Appendix F: Instructor & Accessibility Guide — Disk Space: The Resource That Runs Out

### Teaching Schedule (4-Week Curriculum)

| Week | Focus | Chapters | Outcome |
|---|---|---|---|
| 1 | Foundation | Ch 1–4 | Can use core commands confidently |
| 2 | Intermediate | Ch 5–8 | Can build basic scripts |
| 3 | Applied | Ch 9–11 | Can solve real problems |
| 4 | Mastery | Ch 12–14 + Appendices | Earns `CLL-L0-B020-DiskManager` |

### Common Confusion Points

1. **Confusion:** "When do I use sudo vs. regular user?"
   **Resolution:** Use the permission model diagram from Ch 3. Always try without sudo first.

2. **Confusion:** "Why does the same command work differently on macOS vs. Linux?"
   **Resolution:** Explain BSD vs. GNU utilities. Show the cross-platform comparison from B-025.

3. **Confusion:** "How do I know if my script is working correctly?"
   **Resolution:** Teach the VERIFY step: always test with a known input and expected output.

4. **Confusion:** "What's the difference between Storage Management and just using a GUI?"
   **Resolution:** Show the automation power demo from Chapter 12 DFY lessons.

5. **Confusion:** "How does this connect to what I'm learning in other books?"
   **Resolution:** Show the ACSS connection map from Appendix B and Chapter 14.

### Assessment Rubric

| Criterion | Beginner (1–2) | Competent (3–4) | Expert (5) |
|---|---|---|---|
| Command recall | Can't recall without notes | Uses common commands | Recalls flags and edge cases |
| Error handling | Panics at errors | Googles errors | Diagnoses and fixes independently |
| Script quality | No scripts written | Basic working scripts | Production-quality, documented |
| ACSS integration | Unaware of ACSS | Knows ACSS exists | Uses ADA, understands Hermes |
| Teaching others | Can't explain concepts | Can explain basics | Can teach this book |

### Accessibility Standards

**Screen Reader Support:**
- All diagrams have text alternatives in the ebook
- Code blocks include descriptive comments
- Navigation: every section has an anchor heading

**Color-Blind Support:**
- Terminal screenshots use high-contrast themes
- No information conveyed by color alone
- ASCII art uses text labels, not color coding

**Dyslexia Support:**
- Short paragraphs (3–5 sentences max)
- Consistent heading hierarchy (H2 → H3)
- Key terms bolded on first use
- Audiobook version available for all content

**Offline Access:**
- Complete ebook readable without internet
- All code examples run locally
- Credential claim cached locally in ADA registry

---

## Appendix G: Your Learning Path — Disk Space: The Resource That Runs Out

### Where You Are Now

```
  Phase 1: Linux Foundations (B-001–B-025)
  [████████████████░░░░] 80%

  ✅ B-019 Security Guardian  (CLL-L0-B019-SecurityGuardian)
  👉 B-020: Disk Space: The Resource That Runs Out  ← YOU ARE HERE
  ⬜ B-021 Filesystem Expert  (CLL-L0-B021-FilesystemExpert)
```

### What You've Unlocked

**Credential chain:**

```
CLL-L0-B019-SecurityGuardian
    ↓ (prerequisite)
CLL-L0-B020-DiskManager  ← YOUR NEW CREDENTIAL
    ↓ (unlocks)
CLL-L0-B021-FilesystemExpert
```

### Recommended Next Steps

1. **Immediate:** Claim your `CLL-L0-B020-DiskManager` credential (Appendix C, Prompt 27)
2. **This week:** Build the `disk-audit.sh` capstone project (Appendix H)
3. **Next:** Start `B-021 Filesystem Expert` — it builds directly on B-020 skills

### The Full Phase 1 Path (25 books)

| Book | Title | Credential | Key Skill |
|---|---|---|---|
| B-001 | Terminal Apprentice | CLL-L0-B001-TerminalApprentice | Shell navigation |
| B-002 | Command Architect | CLL-L0-B002-CommandArchitect | Core commands |
| B-003 | Filesystem Navigator | CLL-L0-B003-FilesystemNavigator | File system |
| B-004 | Script Author | CLL-L0-B004-ScriptAuthor | Bash scripting |
| B-005 | Package Manager | CLL-L0-B005-PackageManager | Package management |
| B-006 | Process Wrangler | CLL-L0-B006-ProcessWrangler | Process management |
| B-007 | Network Navigator | CLL-L0-B007-NetworkNavigator | Networking |
| B-008 | Git Foundation | CLL-L0-B008-GitFoundation | Git version control |
| B-009 | Text Processor | CLL-L0-B009-TextProcessor | Text tools |
| B-010 | Service Manager | CLL-L0-B010-ServiceManager | systemd |
| B-011 | EnvVar Master | CLL-L0-B011-EnvVarMaster | Environment variables |
| B-012 | Container Architect | CLL-L0-B012-ContainerArchitect | Docker |
| B-013 | SSH Navigator | CLL-L0-B013-SSHNavigator | SSH |
| B-014 | Cron Master | CLL-L0-B014-CronMaster | Task scheduling |
| B-015 | Editor Expert | CLL-L0-B015-EditorExpert | Neovim |
| B-016 | Pipe Architect | CLL-L0-B016-PipeArchitect | Shell composition |
| B-017 | Arch Specialist | CLL-L0-B017-ArchSpecialist | Arch Linux |
| B-018 | Log Analyst | CLL-L0-B018-LogAnalyst | Log analysis |
| B-019 | Security Guardian | CLL-L0-B019-SecurityGuardian | Linux security |
| B-020 | Disk Manager | CLL-L0-B020-DiskManager | Storage management |
| B-021 | Filesystem Expert | CLL-L0-B021-FilesystemExpert | FHS + inodes |
| B-022 | Shell Scripter | CLL-L0-B022-ShellScripter | Shell functions |
| B-023 | Archive Specialist | CLL-L0-B023-ArchiveSpecialist | Backup + archiving |
| B-024 | User Admin | CLL-L0-B024-UserAdmin | User management |
| B-025 | Platform Deployer | CLL-L0-B025-PlatformDeployer | Cross-platform |

### Cross-Phase Connections

```
Phase 1: Linux Foundations (B-001–B-025)
    ↓  B-020 skills feed directly into:
Phase 2: Python Programming (B-026–B-055)
    ↓  Combined Linux+Python skills enable:
Phase 3: Blockchain Development (B-056–B-100)
    ↓  Full stack enables:
Phase 4–10: Advanced specializations (B-101–B-300)
```

### 📘 Visual Map: Your Current Position

```
[Phase 1: Linux] ══════════════════════════╗
 B001 ✅ B002 ✅ ... B-020 👈 ... B025    ║
                                            ║
[Phase 2: Python] ══════════════════════════╣
 B026 ⬜ B027 ⬜ ... B055                  ║
                                            ║
[Phase 3: Blockchain] ══════════════════════╣
 B056 ⬜ ... B100                          ║
═══════════════════════════════════════════╝
```

---

## Appendix H: Real Project Showcase — Disk Space: The Resource That Runs Out

### Project: `disk-audit.sh`

*A disk audit script that identifies large files and recommends cleanup*

**Credential gated:** Completing this project qualifies you to claim `CLL-L0-B020-DiskManager`

---

### Complete Code

```bash
#!/usr/bin/env bash
# disk-audit.sh — Disk space audit and cleanup advisor
# CLL-L0-B020-DiskManager capstone project

set -euo pipefail

TARGET="${1:-/}"
THRESHOLD_GB="${2:-1}"

echo "=== Disk Audit: $TARGET ==="
echo ""
echo "Overall usage:"
df -h "$TARGET"
echo ""
echo "Top 20 largest directories:"
du -h --max-depth=3 "$TARGET" 2>/dev/null   | sort -rh   | head -20
echo ""
echo "Files larger than ${THRESHOLD_GB}GB:"
find "$TARGET" -maxdepth 6 -type f -size +${THRESHOLD_GB}G 2>/dev/null   | xargs ls -lh 2>/dev/null   | sort -k5 -rh   | head -10

```

### Deploy Instructions

```bash
# Step 1: Create the file
vim disk-audit.sh

# Step 2: Make it executable
chmod +x disk-audit.sh

# Step 3: Test it
./disk-audit.sh --help

# Step 4: Run it for real
./disk-audit.sh

# Step 5: Verify the output matches your expectations
echo "Exit code: $?"
```

### Extend It

Once the base project works, try these extensions:

1. **Add logging:** Write all output to a timestamped log file
2. **Add error handling:** Trap errors with `trap 'echo Error on line $LINENO' ERR`
3. **Add a config file:** Read settings from `~/.config/disk-audit/config`
4. **Add a `--dry-run` flag:** Show what would happen without doing it
5. **Add unit tests:** Use `bats` (Bash Automated Testing System)

### 📘 Ebook Coverage

This project exercises every core skill from B-020:

| Skill | Where Used in Project |
|---|---|
| Storage Management | Core project functionality |
| Error handling | `set -euo pipefail` + trap |
| Argument parsing | `${1:?...}` pattern |
| Output formatting | `echo` + color codes |
| Exit codes | `$?` verification step |

### 🎧 Audiobook Walkthrough (lippytmai voice):

> *"This is your capstone project for Disk Space: The Resource That Runs Out. The file is called disk-audit.sh.
> Here's what it does: a disk audit script that identifies large files and recommends cleanup. When you run it successfully, you've
> demonstrated mastery of Storage Management. That earns you CLL-L0-B020-DiskManager.
> Code it, test it, claim it."*

### 🎬 Video Build Guide:

**SHOW:** Empty terminal + VS Code / Neovim side by side
**BUILD:**
  - Create `disk-audit.sh` with `vim disk-audit.sh`
  - Type the code line by line with explanation
  - Run `chmod +x disk-audit.sh`
  - Execute: `./disk-audit.sh`
**VERIFY:**
  - Show successful output
  - Test edge cases
  - Show error handling in action

**CTA:** "You just built disk-audit.sh. Share it on GitHub, claim your CLL-L0-B020-DiskManager credential, and tag @lippytmai."

---

## Further Reading

- 📄 [Back to README](../README.md)
- 📄 [Product Excellence Framework](PRODUCT-EXCELLENCE-FRAMEWORK.md)
- 📄 [AI Clone Engine Swarms (ACSS)](ai-clone-engine-swarms.md)
- 📄 [ACSS Cross-Platform Copilot Deployment](acss-cross-platform-copilot-deployment.md)
- 📄 [ADA Deployment Activations](ai-deployment-activations.md)
- 📄 [AI Copilot Video Sandbox Creator (ACVS)](ai-copilot-video-sandbox-creator.md)
- 📄 [Previous: B-019](B-019-*.md)
- 📄 [Next: B-021](B-021-*.md)

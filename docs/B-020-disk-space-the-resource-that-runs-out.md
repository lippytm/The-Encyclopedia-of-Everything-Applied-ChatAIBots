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

## Further Reading

- 📄 [`docs/B-014-cron-the-machine-that-never-forgets.md`](B-014-cron-the-machine-that-never-forgets.md) — Schedule disk-monitor.sh with cron
- 📄 [`docs/B-012-the-container-that-held-everything.md`](B-012-the-container-that-held-everything.md) — Docker is the main disk hog to monitor
- 📄 [`docs/B-018-log-files-tell-the-truth.md`](B-018-log-files-tell-the-truth.md) — Log files are the second biggest disk hog
- 🏠 [`README.md`](../README.md) — Encyclopedia home

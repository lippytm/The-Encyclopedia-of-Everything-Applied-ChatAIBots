# B-021: The Linux Filesystem Explained

### FHS — Why Every Directory Has a Purpose and a Job

> *"The Linux filesystem is not chaos — it is a contract. The Filesystem Hierarchy Standard (FHS) says that /etc belongs to configuration, /var belongs to variable data, /home belongs to users, and /tmp belongs to no one permanently. When you understand this contract, you can navigate any Linux machine on Earth without ever having been there before."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Explain the purpose of every top-level directory in the Linux Filesystem Hierarchy Standard
2. Know exactly where to look for configuration files, logs, binaries, and user data
3. Create a well-organized project directory structure inside `~/developer-workspace`
4. Understand symlinks and how they bridge filesystem locations
5. Build a `filesystem-navigator.sh` that audits key FHS locations on any system

**Prerequisite:** B-001 through B-020

**Build Artifact:** `filesystem-navigator.sh` — audits every FHS top-level directory and reports what lives there on the current system

**Credential:** `CLL-L1-B021-FilesystemEngineer` — on-chain on Base

---

## Chapter 1: The Filesystem Hierarchy Standard

The FHS is not arbitrary — every directory exists for a specific type of data with specific ownership and permission characteristics:

```
/
├── bin/     → Essential user binaries (ls, cat, cp) — symlink to /usr/bin on modern systems
├── boot/    → Bootloader files (kernel, initrd, GRUB config)
├── dev/     → Device files (hardware represented as files)
├── etc/     → System-wide configuration files
├── home/    → User home directories (/home/charles/)
├── lib/     → Shared libraries for /bin and /sbin
├── media/   → Mount points for removable media (USB, CD)
├── mnt/     → Temporary mount points for filesystems
├── opt/     → Optional/third-party software packages
├── proc/    → Virtual filesystem — kernel and process information
├── root/    → Home directory of root user (not /home/root)
├── run/     → Runtime data (PIDs, sockets) — cleared on reboot
├── srv/     → Data served by the system (web server files, FTP)
├── sys/     → Virtual filesystem — hardware/kernel interface
├── tmp/     → Temporary files — may be cleared on reboot
├── usr/     → User utilities and applications (the largest directory)
│   ├── bin/    → Most user commands
│   ├── lib/    → Libraries for /usr/bin
│   ├── local/  → Locally compiled/installed software
│   └── share/  → Architecture-independent data
└── var/     → Variable data — logs, databases, mail, print spools
    ├── log/    → System and application log files
    ├── lib/    → Application state data
    ├── run/    → (legacy) runtime data
    └── tmp/    → Persistent temporary files
```

*[Reality — the FHS is maintained by the Linux Foundation. All major distributions (Arch, Ubuntu, Fedora, Debian) follow it with minor variations]*

---

## Chapter 2: The Most Important Directories

### /etc — Configuration Lives Here

```bash
ls /etc | head -30

# Key files to know:
cat /etc/hostname          # system hostname
cat /etc/hosts             # local DNS overrides
cat /etc/fstab             # filesystem mount table (B-020)
cat /etc/passwd            # user accounts (not passwords)
cat /etc/group             # group definitions
cat /etc/os-release        # OS identification
ls /etc/systemd/system/    # systemd unit files (B-010)
ls /etc/ssh/               # SSH configuration (B-013)
ls /etc/cron.d/            # system cron jobs (B-014)
```

### /var — Things That Change

```bash
ls /var/log/               # all log files (B-018)
ls /var/lib/docker/        # Docker data (B-012)
ls /var/lib/postgresql/    # PostgreSQL data files
du -sh /var/*              # what's taking space in /var
```

### /proc — The Kernel as a Filesystem

```bash
cat /proc/cpuinfo          # CPU information
cat /proc/meminfo          # memory statistics
cat /proc/uptime           # system uptime in seconds
ls /proc/$(pgrep python3)/ # files for a running process
cat /proc/$(pgrep sshd)/status  # process status
```

### /usr/local — Your Software

```bash
ls /usr/local/bin/         # manually installed programs
ls /usr/local/lib/         # manually installed libraries
# Convention: software you compile from source installs here
# Package manager software goes to /usr/bin and /usr/lib
```

---

## Chapter 3: Symlinks — The Filesystem's Shortcuts

```bash
# A symlink is a pointer to another file or directory
ls -la /bin   # → shows: bin -> usr/bin (on modern systems)

# Create a symlink
ln -s /home/charles/developer-workspace ~/workspace
ls -la ~ | grep workspace

# Create a symlink for a frequently used config
ln -s ~/.config/nvim/init.lua ~/init.lua

# Check where a symlink points
readlink -f ~/workspace
readlink -f /bin

# Remove a symlink (NOT rm -rf — that deletes the target)
unlink ~/workspace
# or
rm ~/workspace   # safe on symlinks

# Find all symlinks in a directory
find /usr/bin -type l | head -10
```

---

## Chapter 4: Organizing ~/developer-workspace

The `~/developer-workspace` directory is your personal FHS within the home directory. Apply the same discipline:

```bash
mkdir -p ~/developer-workspace/{
  projects,
  scripts,
  logs,
  backups,
  configs,
  sandbox,
  docs
}

# Create a README for your workspace
cat > ~/developer-workspace/README.md << 'EOF'
# Developer Workspace

## Structure
- projects/    Production and active projects (each with its own Git repo)
- scripts/     Personal automation scripts (B-004, B-006, B-013, B-014, B-018, etc.)
- logs/        Script and cron output logs (B-018)
- backups/     Local backup snapshots (B-023)
- configs/     Config templates (.env.example, nginx.conf templates)
- sandbox/     Throwaway experiments — cleared weekly by cron (B-014)
- docs/        Personal notes and cheat sheets
EOF
```

---

## Chapter 5: The Build — Filesystem Navigator

```bash
#!/bin/bash
# filesystem-navigator.sh — B-021 Build Artifact
# Audits key FHS directories on any Linux system
set -euo pipefail

REPORT="/tmp/fhs-audit-$(date +%Y%m%d-%H%M%S).txt"

{
    echo "======================================"
    echo "  Linux Filesystem Audit"
    echo "  Host: $(hostname)"
    echo "  Date: $(date)"
    echo "======================================"
    echo ""

    echo "--- SYSTEM IDENTITY ---"
    cat /etc/os-release 2>/dev/null | grep -E "^NAME|^VERSION" || echo "(unavailable)"
    echo ""

    echo "--- DISK USAGE BY TOP-LEVEL DIRECTORY ---"
    du -sh /bin /boot /etc /home /opt /root /srv /usr /var 2>/dev/null | sort -rh
    echo ""

    echo "--- /etc: KEY CONFIG FILES ---"
    for f in hostname hosts fstab os-release; do
        echo "  /etc/$f: $([ -f /etc/$f ] && echo EXISTS || echo MISSING)"
    done
    echo ""

    echo "--- /var/log: LOG FILES (top 10 by size) ---"
    du -sh /var/log/* 2>/dev/null | sort -rh | head -10
    echo ""

    echo "--- /proc: SYSTEM STATS ---"
    echo "  Uptime: $(awk '{printf "%.0f days, %.0f hours\n", $1/86400, ($1%86400)/3600}' /proc/uptime)"
    echo "  CPU cores: $(nproc)"
    echo "  Memory: $(awk '/MemTotal/{printf "%.1f GB\n", $2/1048576}' /proc/meminfo) total"
    echo ""

    echo "--- /usr/local: CUSTOM INSTALLS ---"
    ls /usr/local/bin/ 2>/dev/null | head -10 || echo "(empty)"
    echo ""

    echo "--- SYMLINKS IN /usr/bin (sample) ---"
    find /usr/bin -maxdepth 1 -type l | head -5 | while read link; do
        echo "  $link → $(readlink -f "$link")"
    done

    echo ""
    echo "Report complete."
} | tee "$REPORT"

echo ""
echo "Saved to: $REPORT"
```

```bash
chmod +x ~/scripts/filesystem-navigator.sh
~/scripts/filesystem-navigator.sh
```

---

## Chapter 6: Proof of Work

```bash
echo "=== B-021 Verification ==="
echo "FHS top-level dirs:"
ls -la / | grep "^d" | awk '{print $NF}' | tr '\n' '  '

echo ""
echo "Developer workspace structure:"
ls ~/developer-workspace/

echo ""
echo "Filesystem audit:"
~/scripts/filesystem-navigator.sh | head -20
```

---

## Further Reading

- 📄 [`docs/B-003-the-file-that-remembered-everything.md`](B-003-the-file-that-remembered-everything.md) — File permissions within the FHS
- 📄 [`docs/B-020-disk-space-the-resource-that-runs-out.md`](B-020-disk-space-the-resource-that-runs-out.md) — Monitoring /var and disk usage
- 📄 [`docs/B-023-archives-compression-and-backups.md`](B-023-archives-compression-and-backups.md) — Backing up key FHS directories
- 🏠 [`README.md`](../README.md) — Encyclopedia home

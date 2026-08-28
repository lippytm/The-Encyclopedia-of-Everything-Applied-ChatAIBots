# B-025: Linux on Every Platform

### WSL, VPS, Raspberry Pi, and Cloud — One Skill, Infinite Surfaces

> *"The beauty of Linux is that it runs everywhere — on a $35 Raspberry Pi in your bedroom, on a $5/month VPS in a datacenter, on a Windows machine through WSL2, on the most powerful AWS server money can rent. Learn it once, deploy it everywhere. This is the platform-agnostic superpower."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Install and configure Linux on at least 3 distinct platforms (WSL2, VPS, Raspberry Pi/cloud)
2. Use SSH to connect to and manage remote Linux instances (B-013 applied)
3. Apply core Linux skills consistently across all platforms
4. Build a `platform-bootstrap.sh` that configures any fresh Linux install with your toolkit
5. Understand what makes each platform unique and when to use each

**Prerequisite:** B-001 through B-024

**Build Artifact:** `~/scripts/platform-bootstrap.sh` — installs your full developer toolkit on any Debian/Ubuntu or Arch Linux system in one command

**Credential:** `CLL-L1-B025-PlatformEngineer` — on-chain on Base

---

## Chapter 1: The Four Linux Platforms

| Platform | Best For | Cost | Linux Distro |
|---|---|---|---|
| **WSL2** (Windows Subsystem for Linux) | Dev on Windows, no dual boot | Free | Ubuntu, Debian, Arch |
| **VPS** (Virtual Private Server) | Hosting, servers, learning in the cloud | $4–$20/mo | Ubuntu, Debian |
| **Raspberry Pi** | IoT, edge computing, home labs | $35–$80 hardware | Raspberry Pi OS (Debian) |
| **Cloud VM** (AWS EC2, GCP, DigitalOcean) | Production workloads, scale | Pay-per-use | Ubuntu, Amazon Linux |

---

## Chapter 2: WSL2 — Linux Inside Windows

*[Reality — WSL2 is a real Linux kernel running inside a Hyper-V lightweight VM on Windows 10/11]*

```powershell
# Install WSL2 (run in Windows PowerShell as Administrator)
wsl --install

# Install a specific distro
wsl --install -d Ubuntu-24.04
wsl --install -d Arch  # via AUR/community WSL distros

# List installed distros
wsl --list --verbose

# Launch your default distro
wsl

# Open a specific distro
wsl -d Ubuntu-24.04
```

```bash
# Inside WSL2 — you have a real Linux environment
uname -r     # Linux kernel version
cat /etc/os-release

# Access Windows files from Linux
ls /mnt/c/Users/YourName/

# Access Linux files from Windows Explorer:
# Type in address bar: \\wsl$\Ubuntu-24.04\home\charles\

# WSL2 performance tip: keep your files on the Linux filesystem (/home/)
# NOT on /mnt/c/ — Windows filesystem access is slow from Linux

# Install your toolkit (same as any Ubuntu system)
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl wget neovim build-essential python3-pip
```

---

## Chapter 3: VPS — Your Server in the Cloud

A VPS (Virtual Private Server) gives you root access to a Linux machine in a datacenter. Popular providers:

| Provider | Entry Price | Notes |
|---|---|---|
| **DigitalOcean Droplet** | $4/mo | Excellent docs, developer-friendly |
| **Hetzner Cloud** | €3.79/mo | Best price/performance in Europe |
| **Linode (Akamai)** | $5/mo | Reliable, long-standing |
| **Vultr** | $2.50/mo | Good global coverage |

```bash
# Connect to your VPS via SSH (B-013)
ssh root@YOUR_VPS_IP

# First thing: never work as root — create a user
adduser charles
usermod -aG sudo charles

# Switch to your new user
su - charles

# Set up SSH key authentication (B-013)
mkdir -p ~/.ssh && chmod 700 ~/.ssh
# On your local machine: ssh-copy-id charles@YOUR_VPS_IP

# Basic VPS hardening (B-019)
sudo ufw allow OpenSSH
sudo ufw enable
sudo nano /etc/ssh/sshd_config
# PermitRootLogin no
# PasswordAuthentication no
sudo systemctl restart sshd

# Now disconnect and reconnect as your user
exit
ssh charles@YOUR_VPS_IP
```

---

## Chapter 4: Raspberry Pi — Linux in Your Hand

```bash
# Flash Raspberry Pi OS to SD card:
# - Download Raspberry Pi Imager from raspberrypi.com/software
# - Choose OS: Raspberry Pi OS Lite (no desktop, for servers)
# - In advanced settings: set hostname, username/password, enable SSH, configure WiFi

# Once Pi is on your network, SSH in
ssh charles@raspberrypi.local
# or
ssh charles@PI_IP_ADDRESS

# Basic Pi info
uname -a
cat /proc/device-tree/model   # Pi model
vcgencmd measure_temp          # CPU temperature
cat /proc/cpuinfo | grep "Model"

# GPIO and Pi-specific tools
sudo apt install -y python3-gpiozero python3-rpi.gpio

# Run a simple LED blink (educational example):
python3 - << 'EOF'
from gpiozero import LED
from time import sleep
led = LED(17)
for _ in range(5):
    led.on(); sleep(0.5)
    led.off(); sleep(0.5)
print("Done!")
EOF
```

---

## Chapter 5: Cloud VMs — AWS, GCP, DigitalOcean

```bash
# AWS EC2 — launch from AWS Console or CLI:
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t3.micro \
    --key-name my-key \
    --security-group-ids sg-xxxxxxxx \
    --subnet-id subnet-xxxxxxxx

# Connect to EC2 (Ubuntu)
ssh -i my-key.pem ubuntu@EC2_PUBLIC_IP

# DigitalOcean — create a Droplet via CLI (doctl):
doctl compute droplet create my-droplet \
    --image ubuntu-24-04-x64 \
    --size s-1vcpu-1gb \
    --region nyc3 \
    --ssh-keys YOUR_KEY_ID

ssh root@DROPLET_IP
```

---

## Chapter 6: The Build — Platform Bootstrap Script

The core idea: one script that works on any fresh Debian/Ubuntu or Arch Linux installation:

```bash
#!/bin/bash
# platform-bootstrap.sh — B-025 Build Artifact
# Configures a fresh Linux install with the lippytmai developer toolkit
# Works on: Ubuntu 22.04+, Debian 12+, Raspberry Pi OS, WSL2
set -euo pipefail

TOOLKIT_REPO="https://raw.githubusercontent.com/lippytm"
LOG="/tmp/bootstrap-$(date +%Y%m%d-%H%M%S).log"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

log "=== Platform Bootstrap v1.0 ==="
log "Host: $(hostname)"
log "User: $(whoami)"
log "OS:   $(. /etc/os-release && echo "$NAME $VERSION_ID")"

# === Detect distro ===
if command -v apt &>/dev/null; then
    PKG_MANAGER="apt"
elif command -v pacman &>/dev/null; then
    PKG_MANAGER="pacman"
else
    log "ERROR: Unsupported package manager"; exit 1
fi
log "Package manager: $PKG_MANAGER"

# === Update ===
log "Updating package lists..."
if [[ "$PKG_MANAGER" == "apt" ]]; then
    sudo apt update -y >> "$LOG" 2>&1
    sudo apt upgrade -y >> "$LOG" 2>&1
else
    sudo pacman -Syu --noconfirm >> "$LOG" 2>&1
fi

# === Install core packages ===
log "Installing core packages..."
PACKAGES_APT="git curl wget neovim tmux htop tree jq unzip rsync ufw python3 python3-pip build-essential"
PACKAGES_PACMAN="git curl wget neovim tmux htop tree jq unzip rsync ufw python python-pip base-devel"

if [[ "$PKG_MANAGER" == "apt" ]]; then
    sudo apt install -y $PACKAGES_APT >> "$LOG" 2>&1
else
    sudo pacman -S --noconfirm $PACKAGES_PACMAN >> "$LOG" 2>&1
fi
log "Core packages installed."

# === Developer workspace ===
log "Creating developer workspace..."
mkdir -p ~/developer-workspace/{projects,scripts,logs,backups,configs,sandbox,docs}
mkdir -p ~/scripts/lib

# === Shell config ===
log "Configuring shell..."
if ! grep -q "bashrc_custom" ~/.bashrc 2>/dev/null; then
    cat >> ~/.bashrc << 'SHELLEOF'

# === lippytmai Developer Toolkit ===
alias ll='ls -la --color=auto'
alias la='ls -A'
alias ..='cd ..'
alias ...='cd ../..'
alias ws='cd ~/developer-workspace'
alias gs='git status'
alias gl='git log --oneline --graph --decorate --all'

mkcd() { mkdir -p "$1" && cd "$1"; }
gacp() { git add -A && git commit -m "${1:-auto: update}" && git push; }
serve() { python3 -m http.server "${1:-8080}"; }
extract() {
    case "$1" in
        *.tar.gz|*.tgz) tar xzf "$1" ;;
        *.tar.bz2)       tar xjf "$1" ;;
        *.tar.xz)        tar xJf "$1" ;;
        *.zip)           unzip   "$1" ;;
        *)               echo "Unknown: $1" ;;
    esac
}
SHELLEOF
    log "Shell configured."
fi

# === Git config (if not set) ===
if [[ -z "$(git config --global user.name 2>/dev/null)" ]]; then
    log "NOTE: Set git config manually: git config --global user.name 'Your Name'"
fi

# === Firewall (VPS/cloud only — skip WSL) ===
if ! grep -qi microsoft /proc/version 2>/dev/null; then
    log "Configuring firewall..."
    sudo ufw allow OpenSSH >> "$LOG" 2>&1 || true
    sudo ufw --force enable >> "$LOG" 2>&1 || true
    log "Firewall enabled (SSH allowed)."
fi

log "=== Bootstrap Complete ==="
log "Log: $LOG"
echo ""
echo "✅ Bootstrap complete on $(hostname)!"
echo "   Reload shell: source ~/.bashrc"
echo "   Full log: $LOG"
```

```bash
chmod +x ~/scripts/platform-bootstrap.sh

# On any new machine — run it:
curl -sO https://raw.githubusercontent.com/lippytm/scripts/main/platform-bootstrap.sh
bash platform-bootstrap.sh
```

---

## Chapter 7: Platform Comparison for ACSS

| Feature | WSL2 | VPS | Raspberry Pi | Cloud VM |
|---|---|---|---|---|
| **Development** | ✅ Excellent | ✅ Good | ⚠️ Limited RAM | ✅ Excellent |
| **Always-on server** | ❌ (Windows must be on) | ✅ 24/7 | ✅ Low power | ✅ 24/7 |
| **Cost** | Free | $4–20/mo | $35 one-time | Variable |
| **SSH key auth** | ✅ | ✅ | ✅ | ✅ |
| **Docker** | ✅ | ✅ | ✅ (ARM) | ✅ |
| **ACSS Agent hosting** | Dev only | ✅ | Edge agents | ✅ Production |

---

## Chapter 8: Proof of Work

```bash
echo "=== B-025 Verification ==="
echo "Platform info:"
uname -a
cat /etc/os-release | grep -E "^NAME|^VERSION"

echo ""
echo "Running bootstrap on current platform:"
~/scripts/platform-bootstrap.sh 2>/dev/null | tail -5

echo ""
echo "Workspace ready:"
ls ~/developer-workspace/

echo ""
echo "Phase 1 Linux Foundations COMPLETE — B-001 through B-025!"
echo "Credential target: CLL-L1-B025-PlatformEngineer"
```

---

## 🎓 Phase 1 Complete — Linux Foundations

Congratulations. You have completed all 25 Linux Foundation books (B-001–B-025):

| Books | Theme |
|---|---|
| B-001–B-005 | Core CLI: terminal, commands, files, scripting, packages |
| B-006–B-010 | System management: processes, networking, Git, text tools, systemd |
| B-011–B-015 | Environment: env vars, Docker, SSH, cron, Neovim |
| B-016–B-020 | Mastery: pipes, Arch/OMARCHY, logging, security, disk |
| B-021–B-025 | Depth: filesystem, functions, backups, user admin, cross-platform |

**Phase 2 begins:** Python Foundations (B-026–B-050)

---

## Further Reading

- 📄 [`docs/B-013-the-tunnel-that-kept-things-private.md`](B-013-the-tunnel-that-kept-things-private.md) — SSH in depth for remote access
- 📄 [`docs/B-024-the-user-who-could-do-anything.md`](B-024-the-user-who-could-do-anything.md) — User security across all platforms
- 📄 [`docs/ai-deployment-activations.md`](ai-deployment-activations.md) — ADA: deploying the 300-book series
- 🏠 [`README.md`](../README.md) — Encyclopedia home

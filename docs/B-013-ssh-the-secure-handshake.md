# B-013: SSH — The Secure Handshake

### Remote Login, File Transfer, and Tunneling with SSH

> *"SSH is the key to the world's infrastructure. Every cloud server, every blockchain node, every remote machine you will ever manage in your career is accessed through SSH. Learning it thoroughly is not optional — it is the price of entry to professional system administration."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Connect to a remote Linux server using SSH
2. Generate and use SSH key pairs for passwordless authentication
3. Transfer files with `scp` and `rsync`
4. Configure `~/.ssh/config` for easy multi-server management
5. Set up SSH tunneling (local port forwarding)

**Prerequisite:** B-001 through B-012

**Build Artifact:** A configured `~/.ssh/config` with at least one server entry + an `rsync` backup script that transfers files to a remote server

**Credential:** `CLL-L1-B013-SSHMaster` — on-chain on Base

---

## Chapter 1: How SSH Works

SSH (Secure Shell) creates an encrypted tunnel between your terminal and a remote machine. Before the tunnel opens, the two machines authenticate each other.

**Password authentication:** you type a password. Simple but weak — passwords can be brute-forced.

**Key-based authentication (recommended):**
1. You generate a key pair: private key (secret, stays on your machine) + public key (safe to share)
2. You put your public key on the server (`~/.ssh/authorized_keys`)
3. When you connect, SSH proves you hold the private key using a cryptographic challenge — no password sent over the wire

*[Reality — key-based SSH authentication is the standard for all production server access; password auth is disabled on most cloud servers by default]*

---

## Chapter 2: Generating SSH Keys

```bash
# Generate an Ed25519 key pair (modern, secure, fast)
ssh-keygen -t ed25519 -C "charles@lippytm.ai"
# Accept default location (~/.ssh/id_ed25519)
# Set a passphrase (protects your private key if your laptop is stolen)

# View your public key — this is safe to share
cat ~/.ssh/id_ed25519.pub
# ssh-ed25519 AAAA... charles@lippytm.ai

# Set correct permissions (required by SSH)
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub

# Add your key to ssh-agent (so you type passphrase once per session)
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### Key Types Comparison

| Type | Status | Key Size | Notes |
|---|---|---|---|
| `ed25519` | ✅ Recommended | 256-bit | Modern, fast, small, secure |
| `rsa` | ⚠️ Legacy | 4096-bit | Still common; use only if required |
| `ecdsa` | ✅ OK | 256-bit | Good but ed25519 is preferred |
| `dsa` | ❌ Broken | 1024-bit | Never use |

---

## Chapter 3: Connecting to a Server

```bash
# Basic SSH connection
ssh user@hostname
ssh charles@192.168.1.100
ssh charles@myserver.lippytm.ai

# Specify which key to use (-i)
ssh -i ~/.ssh/id_ed25519 charles@myserver.lippytm.ai

# Specify port (-p) if not 22
ssh -p 2222 charles@myserver.lippytm.ai

# Copy your public key to a server
ssh-copy-id charles@myserver.lippytm.ai

# Or manually: append your public key to authorized_keys
cat ~/.ssh/id_ed25519.pub | ssh charles@myserver.lippytm.ai \
    "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

# Test connection without logging in (-T)
ssh -T git@github.com
# Hi lippytm! You've successfully authenticated.
```

---

## Chapter 4: ~/.ssh/config — Server Aliases

The SSH config file lets you set connection parameters and create aliases for servers:

```bash
nano ~/.ssh/config
```

```
# ~/.ssh/config

# Format:
# Host <alias>
#     HostName <actual-hostname-or-ip>
#     User <username>
#     Port <port>
#     IdentityFile <path-to-private-key>

Host dev-server
    HostName dev.lippytm.ai
    User charles
    Port 22
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
    ServerAliveCountMax 3

Host prod-server
    HostName prod.lippytm.ai
    User charles
    Port 2222
    IdentityFile ~/.ssh/id_ed25519_prod

Host github
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519

# Defaults for all connections
Host *
    ServerAliveInterval 60
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_ed25519
```

```bash
chmod 600 ~/.ssh/config

# Now connect with just the alias
ssh dev-server
ssh prod-server

# Git also uses the alias
git clone github:lippytm/repo-name
```

---

## Chapter 5: scp and rsync — File Transfer

```bash
# scp — Secure Copy (simple but limited)

# Copy local file to remote
scp backup.sh charles@dev-server:/home/charles/

# Copy remote file to local
scp charles@dev-server:/var/log/app.log ./

# Copy directory (-r = recursive)
scp -r ~/developer-workspace/ charles@dev-server:/home/charles/

# rsync — Better scp (faster, resumable, differential)

# Sync local directory to remote (only sends changed files)
rsync -avz ~/developer-workspace/ charles@dev-server:/home/charles/developer-workspace/
# -a = archive (preserves permissions, timestamps, symlinks)
# -v = verbose
# -z = compress during transfer

# Dry run first (see what would change)
rsync -avzn ~/developer-workspace/ charles@dev-server:/home/charles/developer-workspace/

# Sync and delete files on destination that don't exist locally
rsync -avz --delete ~/developer-workspace/ charles@dev-server:/home/charles/developer-workspace/
```

*[Reality — rsync is the preferred tool for server backups, deployments, and data synchronization in production environments]*

---

## Chapter 6: SSH Tunneling

SSH can forward ports — create encrypted tunnels for traffic:

```bash
# Local port forwarding: access a remote service locally
# Forward local port 15432 → remote port 5432 (PostgreSQL)
ssh -L 15432:localhost:5432 charles@dev-server

# Now in another terminal:
psql -h localhost -p 15432 -U postgres devdb

# Keep the tunnel open in the background (-f = background, -N = no command)
ssh -fN -L 15432:localhost:5432 charles@dev-server

# Reverse tunnel: expose local service to remote server
ssh -R 8080:localhost:3000 charles@dev-server
```

---

## Chapter 7: The Build — rsync Backup Script

```bash
#!/bin/bash
# remote-backup.sh — B-013 Build Artifact
# Syncs developer-workspace to a remote server using rsync over SSH
set -euo pipefail

REMOTE_USER="${REMOTE_USER:-charles}"
REMOTE_HOST="${REMOTE_HOST:-dev-server}"
REMOTE_PATH="${REMOTE_PATH:-/home/charles/backups/developer-workspace}"
LOCAL_PATH="${LOCAL_PATH:-$HOME/developer-workspace}"
LOG_FILE="$HOME/developer-workspace/logs/remote-backup.log"
SSH_KEY="${SSH_KEY:-$HOME/.ssh/id_ed25519}"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"; }

log "Starting remote backup to ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}"

# Dry run first if DRY_RUN=1
if [ "${DRY_RUN:-0}" = "1" ]; then
    log "DRY RUN mode — no files will be transferred"
    rsync -avzn --exclude='.env' --exclude='venv/' --exclude='__pycache__/' \
        -e "ssh -i $SSH_KEY" \
        "$LOCAL_PATH/" "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}/"
else
    rsync -avz --exclude='.env' --exclude='venv/' --exclude='__pycache__/' \
        -e "ssh -i $SSH_KEY" \
        "$LOCAL_PATH/" "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}/"
    log "Remote backup complete"
fi
```

```bash
chmod +x ~/remote-backup.sh
DRY_RUN=1 ~/remote-backup.sh  # test it first
```

---

## Further Reading

- 📄 [`docs/B-010-the-service-that-started-itself.md`](B-010-the-service-that-started-itself.md) — systemd timer to schedule rsync backup
- 📄 [`docs/B-012-the-container-that-held-everything.md`](B-012-the-container-that-held-everything.md) — Docker Compose uses SSH keys for registry auth
- 📄 [`docs/linux-blockchain-educational-ecosystem.md`](linux-blockchain-educational-ecosystem.md) — SSH to blockchain nodes
- 🏠 [`README.md`](../README.md) — Encyclopedia home

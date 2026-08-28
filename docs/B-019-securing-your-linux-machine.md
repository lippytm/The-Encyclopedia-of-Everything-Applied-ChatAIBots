# B-019: Securing Your Linux Machine

### Firewall, fail2ban, SSH Hardening, and the Hardened Server Checklist

> *"Security is not a feature you add at the end. It is a series of decisions you make from the beginning: which services are exposed, who can access them, what authentication method they use, and what happens when someone tries to brute-force their way in. This book gives you the checklist every production server needs."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Configure `ufw` (Uncomplicated Firewall) to allow only necessary traffic
2. Harden SSH to disable password auth and root login
3. Install and configure `fail2ban` to block brute-force attacks
4. Audit running services and disable unnecessary ones
5. Produce a hardened server config file for new server provisioning

**Prerequisite:** B-001 through B-018

**Build Artifact:** A `harden-server.sh` script that applies all hardening steps to a fresh Linux server

**Credential:** `CLL-L2-B019-ServerGuardian` — on-chain on Base

---

## Chapter 1: The Threat Model

Before hardening, understand what you're defending against:

| Threat | Description | Mitigation |
|---|---|---|
| **Port scanning** | Bots scan for open ports 24/7 | Firewall: close unused ports |
| **SSH brute force** | Automated password guessing | Disable password auth + fail2ban |
| **Root login** | Direct root access over network | Disable root SSH login |
| **Stale services** | Old services running = more attack surface | Disable/remove unused services |
| **Unpatched packages** | Known CVEs in old packages | Automatic security updates |

*[Reality — a fresh Linux server exposed to the internet receives its first SSH brute-force attempt within minutes of launch]*

---

## Chapter 2: ufw — Uncomplicated Firewall

```bash
# Install ufw
sudo apt install ufw     # Ubuntu/Debian
sudo pacman -S ufw       # Arch

# Enable and set default policies
sudo ufw default deny incoming    # Block all incoming by default
sudo ufw default allow outgoing   # Allow all outgoing by default

# Allow SSH (ALWAYS do this before enabling, or you'll lock yourself out)
sudo ufw allow ssh              # port 22
sudo ufw allow 2222/tcp         # or your custom SSH port

# Allow common services
sudo ufw allow http             # port 80
sudo ufw allow https            # port 443

# Allow a specific IP only
sudo ufw allow from 203.0.113.10 to any port 5432

# Enable the firewall
sudo ufw enable

# Check status
sudo ufw status verbose
sudo ufw status numbered

# Remove a rule
sudo ufw delete 3              # by number
sudo ufw delete allow http     # by rule

# Disable completely (emergency)
sudo ufw disable
```

---

## Chapter 3: SSH Hardening

```bash
# Edit SSH config
sudo nvim /etc/ssh/sshd_config
```

```
# /etc/ssh/sshd_config — Hardened settings

# Change default port (reduces automated scan noise)
Port 2222

# Disable root login
PermitRootLogin no

# Disable password authentication (key-only)
PasswordAuthentication no
PubkeyAuthentication yes

# Disable empty passwords
PermitEmptyPasswords no

# Only allow specific users
AllowUsers charles

# Use modern ciphers only
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org

# Timeout idle connections after 10 minutes
ClientAliveInterval 300
ClientAliveCountMax 2

# Limit login attempts
MaxAuthTries 3
MaxSessions 5
```

```bash
# Test config before reloading (ALWAYS do this)
sudo sshd -t

# Reload SSH daemon
sudo systemctl reload sshd

# Verify you can still connect in a NEW terminal before closing existing session
```

---

## Chapter 4: fail2ban — Automatic Brute-Force Protection

```bash
# Install
sudo apt install fail2ban    # Ubuntu/Debian
sudo pacman -S fail2ban      # Arch

# Create local config (never edit the .conf file — use .local)
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nvim /etc/fail2ban/jail.local
```

```ini
# /etc/fail2ban/jail.local — key settings

[DEFAULT]
# Ban for 1 hour after 3 failures within 10 minutes
bantime  = 3600
findtime = 600
maxretry = 3

# Email alerts (optional)
destemail = charles@lippytm.ai
sendername = fail2ban
action = %(action_mwl)s

[sshd]
enabled = true
port = 2222
filter = sshd
logpath = %(sshd_log)s
maxretry = 3
bantime = 86400    # 24 hour ban for SSH brute force
```

```bash
# Start fail2ban
sudo systemctl enable --now fail2ban

# Check status
sudo fail2ban-client status
sudo fail2ban-client status sshd

# See banned IPs
sudo fail2ban-client get sshd banip

# Unban an IP manually (if you accidentally lock yourself out)
sudo fail2ban-client set sshd unbanip 203.0.113.42
```

---

## Chapter 5: The Build — Hardening Script

```bash
#!/bin/bash
# harden-server.sh — B-019 Build Artifact
# Applies security hardening to a fresh Ubuntu/Debian server
# Run as root after initial server setup and key-based SSH configured

set -euo pipefail
LOG="/root/harden-server.log"
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG"; }

# Prerequisites check
[ "$(id -u)" = "0" ] || { echo "Run as root"; exit 1; }
command -v ufw &>/dev/null || apt-get install -y ufw
command -v fail2ban-client &>/dev/null || apt-get install -y fail2ban

log "=== Hardening server: $(hostname) ==="

# 1. System update
log "Updating packages..."
apt-get update -q && apt-get upgrade -y -q

# 2. Firewall
log "Configuring firewall..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow 2222/tcp    # SSH on custom port
ufw allow http
ufw allow https
ufw --force enable
log "Firewall: $(ufw status | grep Status)"

# 3. SSH hardening
log "Hardening SSH..."
SSH_CONF="/etc/ssh/sshd_config"
cp "$SSH_CONF" "${SSH_CONF}.bak"
sed -i 's/^#*PermitRootLogin.*/PermitRootLogin no/' "$SSH_CONF"
sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' "$SSH_CONF"
sed -i 's/^#*MaxAuthTries.*/MaxAuthTries 3/' "$SSH_CONF"
sshd -t && systemctl reload sshd
log "SSH hardened: password auth disabled, root login disabled"

# 4. fail2ban
log "Configuring fail2ban..."
systemctl enable --now fail2ban
log "fail2ban: $(systemctl is-active fail2ban)"

# 5. Auto security updates (Ubuntu)
if command -v unattended-upgrades &>/dev/null; then
    log "Enabling unattended security updates..."
    echo 'Unattended-Upgrade::Automatic-Reboot "false";' >> /etc/apt/apt.conf.d/50unattended-upgrades
    systemctl enable --now unattended-upgrades
fi

log "=== Hardening complete. Review: $LOG ==="
log "IMPORTANT: Test SSH login in a new terminal before closing this session!"
```

---

## Chapter 6: Proof of Work

```bash
echo "=== B-019 Verification ==="
sudo ufw status verbose
echo ""
echo "fail2ban jails:"
sudo fail2ban-client status
echo ""
echo "SSH config check:"
grep -E "PermitRootLogin|PasswordAuthentication|MaxAuthTries" /etc/ssh/sshd_config
```

---

## Further Reading

- 📄 [`docs/B-013-ssh-the-secure-handshake.md`](B-013-ssh-the-secure-handshake.md) — SSH key setup prerequisite
- 📄 [`docs/B-018-log-files-tell-the-truth.md`](B-018-log-files-tell-the-truth.md) — Monitor auth.log for intrusion attempts
- 📄 [`docs/linux-blockchain-educational-ecosystem.md`](linux-blockchain-educational-ecosystem.md) — Securing blockchain nodes
- 🏠 [`README.md`](../README.md) — Encyclopedia home

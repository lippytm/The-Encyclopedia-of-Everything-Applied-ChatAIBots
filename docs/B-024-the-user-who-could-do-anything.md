# B-024: The User Who Could Do Anything

### sudo, root, User Management, and the Principle of Least Privilege

> *"root can delete everything. root can break the kernel. root has no undo. This is why we don't live as root — we become root for exactly as long as we need to, and then we step back. The discipline of 'least privilege' is what separates engineers from disasters."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Understand the difference between root, sudo, and standard users
2. Create and manage users and groups on Linux
3. Configure the sudoers file to grant scoped privileges
4. Apply the Principle of Least Privilege to system design
5. Build a `user-audit.sh` that reports all users, groups, and sudo access

**Prerequisite:** B-001 through B-023

**Build Artifact:** `~/scripts/user-audit.sh` — audits all system users, groups, and sudo grants

**Credential:** `CLL-L1-B024-UserAdmin` — on-chain on Base

---

## Chapter 1: The Linux User Model

Linux has three user categories:

| Type | UID Range | Description |
|---|---|---|
| **root** | 0 | Superuser — unrestricted access to everything |
| **System users** | 1–999 | Services and daemons (www-data, postgres, nobody) |
| **Regular users** | 1000+ | Human users (you) |

```bash
# Who am I?
whoami              # current username
id                  # UID, GID, and all groups
id charles          # UID, GID, groups for a specific user

# User database files (plain text)
cat /etc/passwd     # username:x:UID:GID:comment:home:shell
cat /etc/group      # groupname:x:GID:member1,member2
sudo cat /etc/shadow  # hashed passwords (root only)

# Currently logged-in users
who
w                   # with what they're running
last | head -10     # login history
```

---

## Chapter 2: sudo — Controlled Elevation

```bash
# sudo runs a single command as root (or another user)
sudo apt update
sudo systemctl restart nginx
sudo cat /etc/shadow

# sudo -i — interactive root shell (use sparingly)
sudo -i
exit              # ALWAYS exit the root shell when done

# sudo -u — run as a specific user
sudo -u postgres psql

# Who has sudo access?
sudo cat /etc/sudoers
getent group sudo
getent group wheel  # Arch Linux uses wheel instead of sudo

# Your current sudo privileges
sudo -l

# sudo timeout — stay elevated for N minutes (default: 15)
sudo -v            # extend sudo session without running a command
```

---

## Chapter 3: Creating and Managing Users

```bash
# Create a new user
sudo useradd -m -s /bin/bash newuser
# -m = create home directory, -s = set default shell

# With full options:
sudo useradd \
    -m \
    -s /bin/bash \
    -G sudo,docker \
    -c "New Developer Account" \
    developer1

# Set password
sudo passwd developer1

# Modify an existing user
sudo usermod -aG docker charles    # add charles to docker group
sudo usermod -s /bin/zsh charles   # change default shell
sudo usermod -c "Charles Lipshay" charles  # change display name

# Lock/unlock an account
sudo usermod -L developer1    # lock (prevents login)
sudo usermod -U developer1    # unlock

# Delete a user (keep home directory)
sudo userdel developer1
# Delete user AND home directory
sudo userdel -r developer1

# View user details
getent passwd charles
finger charles   # if finger is installed
```

---

## Chapter 4: Groups — Shared Access Control

```bash
# Create a group
sudo groupadd developers

# Add users to a group
sudo usermod -aG developers charles
sudo usermod -aG developers developer1

# Remove a user from a group (edit /etc/group directly or:)
sudo gpasswd -d developer1 developers

# View groups
groups                  # your groups
groups charles          # another user's groups
cat /etc/group          # all groups
getent group developers # specific group

# Create shared project directory accessible by group
sudo mkdir /opt/shared-project
sudo chown root:developers /opt/shared-project
sudo chmod 775 /opt/shared-project
# Now all members of 'developers' can read/write
```

---

## Chapter 5: /etc/sudoers — Fine-Grained Privilege Control

```bash
# ALWAYS edit sudoers with visudo — it validates before saving
sudo visudo

# sudoers syntax:
# USER  HOSTS=(RUNAS)  COMMANDS

# Allow charles to run any command as root:
charles ALL=(ALL:ALL) ALL

# Allow a user to run specific commands without password:
charles ALL=(ALL) NOPASSWD: /usr/bin/apt, /usr/bin/systemctl

# Allow a group to have sudo access:
%developers ALL=(ALL:ALL) ALL

# Allow user to restart nginx only:
www-manager ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx

# Best practice: create a sudoers.d drop-in file instead
sudo visudo -f /etc/sudoers.d/developers
# Add: %developers ALL=(ALL:ALL) ALL

# Verify sudoers is valid
sudo visudo -c
```

---

## Chapter 6: The Principle of Least Privilege

| ❌ Anti-Pattern | ✅ Best Practice |
|---|---|
| Run your app as root | Create a dedicated service user |
| Give full sudo to service accounts | Give only the commands they need |
| Share passwords | Each human gets their own account |
| Keep root shell open | `sudo -i` only when needed, then `exit` |
| `chmod 777` on shared dirs | Set group ownership + `chmod 775` |

```bash
# Create a service user (no login shell, no home dir)
sudo useradd \
    -r \
    -s /bin/false \
    -c "My App Service Account" \
    myapp-svc
# -r = system account (UID < 1000)
# -s /bin/false = cannot log in interactively

# Run a process as the service user
sudo -u myapp-svc /opt/myapp/bin/start.sh

# In systemd unit (B-010):
# [Service]
# User=myapp-svc
# Group=myapp-svc
```

---

## Chapter 7: The Build — User Audit Script

```bash
#!/bin/bash
# user-audit.sh — B-024 Build Artifact
# Reports all users, groups, and sudo access on the system
set -euo pipefail

echo "======================================"
echo "  Linux User & Privilege Audit"
echo "  Host: $(hostname)"
echo "  Date: $(date)"
echo "======================================"

echo ""
echo "--- CURRENT USER ---"
echo "  User:   $(whoami)"
echo "  UID:    $(id -u)"
echo "  Groups: $(groups | tr ' ' '\n' | sed 's/^/    /')"

echo ""
echo "--- HUMAN USER ACCOUNTS (UID >= 1000) ---"
awk -F: '$3 >= 1000 && $3 < 65534 {
    printf "  %-15s UID=%-6s Home=%-30s Shell=%s\n", $1, $3, $6, $7
}' /etc/passwd

echo ""
echo "--- SYSTEM SERVICE ACCOUNTS ---"
awk -F: '$3 > 0 && $3 < 1000 {
    printf "  %-20s UID=%s\n", $1, $3
}' /etc/passwd | sort

echo ""
echo "--- GROUPS WITH MEMBERS ---"
awk -F: '$4 != "" {
    printf "  %-20s GID=%-6s Members=%s\n", $1, $3, $4
}' /etc/group | sort

echo ""
echo "--- SUDO ACCESS ---"
if [[ -f /etc/sudoers ]]; then
    echo "  Users/groups with sudo access:"
    sudo grep -E "^[^#]" /etc/sudoers 2>/dev/null | grep -v "^Defaults\|^%\|^\$" | sed 's/^/  /' || echo "  (run as root for full view)"
    echo ""
    echo "  Groups with sudo access:"
    sudo grep -E "^%" /etc/sudoers 2>/dev/null | sed 's/^/  /' || true
fi

if [[ -d /etc/sudoers.d ]]; then
    echo ""
    echo "  sudoers.d drop-ins:"
    ls /etc/sudoers.d/ | sed 's/^/    /'
fi

echo ""
echo "--- RECENTLY LOGGED IN USERS ---"
last | head -10 | sed 's/^/  /'

echo ""
echo "--- FAILED LOGIN ATTEMPTS (last 5) ---"
sudo lastb 2>/dev/null | head -5 | sed 's/^/  /' || echo "  (requires root)"

echo ""
echo "Audit complete."
```

```bash
chmod +x ~/scripts/user-audit.sh
sudo ~/scripts/user-audit.sh
```

---

## Chapter 8: Proof of Work

```bash
echo "=== B-024 Verification ==="
echo "Current user:"
id

echo ""
echo "sudo privileges:"
sudo -l 2>/dev/null | grep -E "NOPASSWD|ALL" | head -5

echo ""
echo "Groups:"
cat /etc/group | grep -E "^sudo|^wheel|^docker" | head -5

echo ""
echo "User audit:"
sudo ~/scripts/user-audit.sh | head -30
```

---

## Further Reading

- 📄 [`docs/B-003-the-file-that-remembered-everything.md`](B-003-the-file-that-remembered-everything.md) — File ownership and chmod
- 📄 [`docs/B-013-the-tunnel-that-kept-things-private.md`](B-013-the-tunnel-that-kept-things-private.md) — SSH user access and key-based auth
- 📄 [`docs/B-019-the-firewall-that-asked-who-goes-there.md`](B-019-the-firewall-that-asked-who-goes-there.md) — Security + privilege for services
- 🏠 [`README.md`](../README.md) — Encyclopedia home

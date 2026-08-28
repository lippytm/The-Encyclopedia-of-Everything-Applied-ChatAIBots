# B-003: The File That Remembered Everything

### Linux Permissions, Users, and Groups — Because Not Everything Should Be Public

> *"A computer without access controls is a library where anyone can rewrite any book. Permissions are the locks on the shelves — and understanding them is how you become the librarian."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Read and interpret Linux file permission strings (`-rwxr-xr-x`)
2. Change file permissions using `chmod` (numeric and symbolic modes)
3. Change file ownership using `chown` and `chgrp`
4. Create a new user and group on a Linux system
5. Set up a secure project directory that only the right people can access

**Prerequisite:** B-001, B-002 (terminal navigation and basic commands)

**Build Artifact:** A secure `team-project/` directory structure with correct permissions for a 3-person team (owner, collaborator, public)

**Credential:** `CLL-L1-B003-PermissionsEngineer` — on-chain on Base

---

## Chapter 1: Why Permissions Exist

In 1969, Ken Thompson and Dennis Ritchie built Unix — the operating system that Linux and macOS are both descended from. From day one, it was designed to be a **multi-user system**: many people logging into the same machine simultaneously.

This created an immediate problem: if Alice and Bob are both using the same computer, how do you stop Bob from reading Alice's private files? Or from accidentally deleting the operating system?

The answer: **file permissions**.

Every file on a Linux system has three pieces of ownership information:

| Concept | What It Means |
|---|---|
| **Owner** | The user who created (or was assigned) the file |
| **Group** | A named collection of users who share access |
| **Others** | Everyone else on the system |

And for each of those three, the file can allow or deny three operations:

| Permission | Symbol | What It Allows |
|---|---|---|
| **Read** | `r` | View the file's contents (or list a directory) |
| **Write** | `w` | Modify the file's contents (or create/delete files in a directory) |
| **Execute** | `x` | Run the file as a program (or enter a directory with `cd`) |

*[Reality — this permission model has been stable since Unix V7 in 1979 and is still in use in 2026]*

---

## Chapter 2: Reading the Permission String

Run `ls -la` in any directory:

```bash
ls -la ~/developer-workspace
```

You'll see output like this:

```
drwxr-xr-x 5 charles developers 4096 Aug 28 02:00 project-alpha
-rw-r--r-- 1 charles charles     234 Aug 28 02:00 README.md
-rwxr-x--- 1 charles developers  891 Aug 28 02:01 deploy.sh
```

Let's decode the first column:

```
- r w x r - x r - -
│ │││ │││ │││
│ │││ │││ └└└── Others:      r-- = read only
│ │││ └└└────── Group:       r-x = read + execute
│ └└└────────── Owner:       rwx = read + write + execute
└────────────── Type: - = file, d = directory, l = symlink
```

### Full Decode Table

| String | Owner | Group | Others | Meaning |
|---|---|---|---|---|
| `-rwxr-xr-x` | rwx | r-x | r-x | Executable: owner full, everyone can read+run |
| `-rw-r--r--` | rw- | r-- | r-- | Typical file: owner can edit, others read-only |
| `-rw-------` | rw- | --- | --- | Private: only owner can read/write |
| `drwxr-xr-x` | rwx | r-x | r-x | Directory: owner full, others can list+enter |
| `drwx------` | rwx | --- | --- | Private directory: only owner can use it |

---

## Chapter 3: chmod — Changing Permissions

`chmod` has two modes: **symbolic** (human-readable) and **numeric** (octal). Both are useful.

### Symbolic Mode

```bash
# Syntax: chmod [who][+/-/=][permissions] file

# Add execute permission for the owner
chmod u+x deploy.sh

# Remove write permission from group
chmod g-w config.json

# Give read permission to everyone (owner, group, others)
chmod a+r README.md

# Set exact permissions: owner=rwx, group=r-x, others=---
chmod u=rwx,g=rx,o= private-script.sh
```

**Who codes:**
- `u` = user (owner)
- `g` = group
- `o` = others
- `a` = all (u + g + o)

### Numeric (Octal) Mode

Each permission is a bit: r=4, w=2, x=1. Add them up for each group:

| Octal | Binary | Permissions |
|---|---|---|
| `7` | 111 | rwx (read + write + execute) |
| `6` | 110 | rw- (read + write) |
| `5` | 101 | r-x (read + execute) |
| `4` | 100 | r-- (read only) |
| `0` | 000 | --- (no permissions) |

```bash
# chmod [owner][group][others] file

chmod 755 deploy.sh     # -rwxr-xr-x  (typical script)
chmod 644 config.json   # -rw-r--r--  (typical file)
chmod 600 .secret       # -rw-------  (private)
chmod 700 private/      # drwx------  (private directory)

# Apply recursively to a directory and all contents (-R)
chmod -R 755 public-project/
```

*[Reality — 755 for executables/directories and 644 for regular files are the most common permission patterns in production systems]*

---

## Chapter 4: chown and chgrp — Changing Ownership

```bash
# Change owner of a file
chown alice report.txt

# Change owner AND group at the same time
chown alice:developers report.txt

# Change just the group
chgrp developers report.txt

# Change ownership recursively for a whole directory
chown -R alice:developers ~/projects/team-project/

# View current owner and group
ls -la report.txt
# -rw-r--r-- 1 alice developers 1234 Aug 28 report.txt
```

> ⚠️ *[Reality — `chown` usually requires `sudo` (superuser) privileges to change files you don't own]*

### sudo — Running Commands as Administrator

```bash
# sudo = "superuser do" — run a command as root (the system administrator)
sudo chown root:root /etc/config-file
sudo chmod 600 /etc/config-file

# See who you are
whoami
# charles

# See who root is
sudo whoami
# root
```

---

## Chapter 5: Users and Groups

### Creating and Managing Users

```bash
# Create a new user
sudo useradd -m alice          # -m = create home directory

# Set a password for the user
sudo passwd alice

# Create a user with specific shell and comment
sudo useradd -m -s /bin/bash -c "Alice Collaborator" alice

# Delete a user (but keep their home directory)
sudo userdel alice

# Delete user AND home directory
sudo userdel -r alice

# List all users
cat /etc/passwd | cut -d: -f1
```

### Creating and Managing Groups

```bash
# Create a new group
sudo groupadd developers

# Add a user to a group
sudo usermod -aG developers charles    # -a = append (don't remove from other groups)
sudo usermod -aG developers alice

# See what groups a user belongs to
groups charles
# charles : charles sudo developers

# See all groups
cat /etc/group | cut -d: -f1

# Remove a user from a group
sudo gpasswd -d alice developers
```

*[Reality — changes to group membership take effect at next login]*

---

## Chapter 6: The Build — Secure Team Project Directory

You're setting up a project directory for a 3-person team:
- **You** (owner): full access to everything
- **Collaborators** (developers group): can read all files, write to `src/` and `docs/`, cannot touch `secrets/`
- **Public** (others): can read `docs/` only

```bash
# Step 1: Create the group (if it doesn't exist)
sudo groupadd developers 2>/dev/null || echo "Group exists"
sudo usermod -aG developers $USER

# Step 2: Create the directory structure
cd ~
mkdir -p team-project/{src,tests,docs,secrets,logs}
cd team-project

# Step 3: Create placeholder files
echo "# Team Project" > docs/README.md
echo "# Source code goes here" > src/main.py
echo "SECRET_KEY=do-not-share" > secrets/env.secret
touch logs/app.log

# Step 4: Set ownership — everything owned by you, group=developers
sudo chown -R $USER:developers .

# Step 5: Set directory permissions
chmod 750 .           # drwxr-x---  owner=full, group=enter+list, others=nothing
chmod 775 src/        # drwxrwxr-x  owner+group can create files
chmod 775 docs/       # drwxrwxr-x  owner+group can create files
chmod 750 tests/      # drwxr-x---  group can read/enter, not write
chmod 700 secrets/    # drwx------  ONLY owner can enter
chmod 755 logs/       # drwxr-xr-x  group can read logs

# Step 6: Set file permissions
chmod 664 docs/README.md    # owner+group read/write, others read
chmod 664 src/main.py       # owner+group read/write, others read
chmod 600 secrets/env.secret  # ONLY owner can read
chmod 644 logs/app.log      # owner write, everyone read

# Step 7: Verify
echo "=== Permission Verification ==="
ls -la
echo ""
ls -la src/
ls -la secrets/
ls -la docs/
```

**Expected output of `ls -la` on `team-project/`:**

```
drwxr-x--- 6 charles developers 4096 Aug 28 .
drwxrwxr-x 2 charles developers 4096 Aug 28 docs
drwx------ 2 charles developers 4096 Aug 28 secrets
drwxrwxr-x 2 charles developers 4096 Aug 28 src
drwxr-x--- 2 charles developers 4096 Aug 28 tests
drwxr-xr-x 2 charles developers 4096 Aug 28 logs
```

🎯 **Build complete.** You've set up a permission structure that protects your secrets while allowing collaborative access to shared code.

---

## Chapter 7: Common Patterns in Production

These permission patterns appear in almost every real Linux system:

| Pattern | chmod | Use Case |
|---|---|---|
| Private key / secret | `600` `-rw-------` | SSH keys, `.env` files, API keys |
| Config file | `644` `-rw-r--r--` | Application configuration |
| Executable script | `755` `-rwxr-xr-x` | Deploy scripts, CLI tools |
| Web server files | `644` + `755` dirs | Web root content |
| Private directory | `700` `drwx------` | Personal secrets folder |
| Shared team dir | `775` `drwxrwxr-x` | Collaborative source directories |

```bash
# Quick application: secure an SSH key (required by SSH itself)
mkdir -p ~/.ssh
chmod 700 ~/.ssh
touch ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

---

## Chapter 8: Proof of Work

```bash
cd ~/team-project

echo "=== B-003 Build Verification ==="
echo "Current user: $(whoami)"
echo "Groups: $(groups)"
echo ""
echo "Directory permissions:"
ls -la
echo ""
echo "Secrets directory (should be 700):"
ls -la secrets/
echo ""
echo "Can we read the secret file?"
cat secrets/env.secret
echo ""
echo "Docs (should be 775):"
ls -la docs/
```

Verify:
- `secrets/` shows `drwx------`
- `secrets/env.secret` shows `-rw-------`
- `src/` shows `drwxrwxr-x`
- `docs/` shows `drwxrwxr-x`

---

## Chapter 9: Mutation

```bash
# MUTATION 1: Use a special permission — the sticky bit
# Sticky bit on a directory: users can only delete their own files
chmod +t /tmp
ls -la / | grep tmp
# drwxrwxrwt  ← the 't' is the sticky bit

# MUTATION 2: Find files with dangerous permissions
# Find world-writable files in your home directory (security audit pattern)
find ~ -perm -o+w -type f 2>/dev/null

# MUTATION 3: Use umask to set default permissions
# umask subtracts from the default (666 for files, 777 for dirs)
umask 022  # results in 644 files and 755 directories (most common default)
umask 027  # results in 640 files and 750 directories (more restrictive)
echo "Current umask: $(umask)"
```

---

## Chapter 10: What Comes Next

| Book | Title | What You'll Build |
|---|---|---|
| **B-004** | *The Script That Did My Job* | Bash backup script using permissions and paths |
| **B-005** | *Installing Things Without Breaking Things* | Python dev environment with correct file permissions |
| **B-008** | *Files That Never Get Lost* | Git — the version control system for your code |

---

## Further Reading

- 📄 [`docs/B-002-commands-that-actually-work.md`](B-002-commands-that-actually-work.md) — Commands used throughout this book
- 📄 [`docs/linux-blockchain-educational-ecosystem.md`](linux-blockchain-educational-ecosystem.md) — Full Linux curriculum
- 📄 [`docs/P011-EBOOK-000-course-series-master-plan.md`](P011-EBOOK-000-course-series-master-plan.md) — All 300 books
- 🏠 [`README.md`](../README.md) — Encyclopedia home

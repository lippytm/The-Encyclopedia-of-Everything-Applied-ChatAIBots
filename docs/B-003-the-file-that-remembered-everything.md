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

## Chapter 12: Done-For-You Lessons

> *"Files are the memory of every system ever built. Master how they're organized and you master how everything works."*

Ten builds that give you real, working tools for navigating, managing, and understanding the file system as a professional.

| Icon | Format | What it is |
|---|---|---|
| 📘 | **Ebook** | Annotated diagram or reference map |
| 🎧 | **Audiobook** | Narrator script — pause and build |
| 🎬 | **Video** | SHOW→BUILD→VERIFY terminal scene |

---

### DFY Lesson 1 — File System Map You Can Read

**What you'll have:** A printed or saved reference showing what lives where in a Linux filesystem, annotated with your notes.
**Time:** 10 minutes.

---

📘 **Ebook Figure**

```
/
├── bin/        → essential user commands (ls, cp, mv, bash)
├── boot/       → kernel and bootloader files — don't touch
├── dev/        → device files (disks, terminals, /dev/null)
├── etc/        → ALL system configuration files (network, users, services)
├── home/       → your personal space (/home/lippytm/)
│   └── lippytm/
│       ├── .bashrc      → shell config (you own this)
│       ├── .ssh/        → SSH keys (protect this)
│       ├── projects/    → your code
│       └── notes/       → your knowledge base
├── lib/        → shared libraries for /bin and /sbin
├── proc/       → virtual filesystem — live kernel & process data
├── root/       → home directory for the root user (not /)
├── run/        → runtime data (PIDs, sockets) — cleared on reboot
├── srv/        → data served by web/ftp servers
├── sys/        → virtual filesystem — hardware device data
├── tmp/        → temporary files — cleared on reboot
├── usr/        → user programs and libraries (usr/bin, usr/lib)
└── var/        → variable data: logs, caches, mail (/var/log/)
```

*Figure 12.1 — The Linux filesystem is a city. This is the city map. Every building serves a specific purpose.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 1: File System Map You Can Read.
>
> Every file on your Linux system has a home — and that home is not random. `/etc` always holds configuration. `/var/log` always holds logs. `/tmp` is always wiped on reboot. Once you internalize this map, you know where to look when something breaks — without searching. Your deliverable is this map, annotated with examples from your own machine.
>
> Time to build: 10 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** Navigate to 6 key directories with `cd` + `ls`. Each directory reveals its purpose through its contents.
- **BUILD:** Learner explores their own machine, adding personal examples to each row of the map.
- **VERIFY:** `ls /etc | wc -l` — count config files. `ls /var/log` — spot the logs.

🤖 **Copilot Assist — DFY Lesson 1**

> **Use this prompt with your book copilot right now:**
>
> *"I found a directory I don't recognize at /opt/containerd/. Which directory in the filesystem map does this belong to conceptually, and is it safe to leave it alone?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-003 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


---

### DFY Lesson 2 — Hidden Files Inventory Script

**What you'll have:** `hidden-inv.sh` — lists all hidden files in your home directory with sizes.
**Time:** 10 minutes.

---

📘 **Ebook Figure**

```bash
#!/usr/bin/env bash
# hidden-inv.sh — inventory of dotfiles in your home directory
echo "=== Hidden Files in $HOME ==="
echo ""
find "$HOME" -maxdepth 1 -name ".*" -not -name ".." | sort | while read -r f; do
  if [[ -f "$f" ]]; then
    size=$(du -sh "$f" 2>/dev/null | cut -f1)
    echo "  📄 $size  $f"
  elif [[ -d "$f" ]]; then
    size=$(du -sh "$f" 2>/dev/null | cut -f1)
    echo "  📁 $size  $f/"
  fi
done
echo ""
echo "Total: $(find "$HOME" -maxdepth 1 -name ".*" | wc -l) hidden items"
```

```
=== Hidden Files in /home/lippytm ===
  📄 4.0K  /home/lippytm/.bash_history
  📄 1.2K  /home/lippytm/.bashrc
  📁 128K  /home/lippytm/.config/
  📁 4.0K  /home/lippytm/.ssh/
  ...
Total: 23 hidden items
```

*Figure 12.2 — Hidden files configure your entire environment. Knowing what's there is step one of controlling it.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 2: Hidden Files Inventory Script.
>
> Your home directory contains a hidden city of dotfiles — configuration for your shell, your editor, your SSH keys, your package managers. Most users never know what's there. This script inventories all of it in one shot, with sizes, so you can see exactly what's configuring your environment — and what you own.
>
> Your deliverable is: `hidden-inv.sh` — a full hidden file inventory with sizes.
>
> Time to build: 10 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** Run `hidden-inv.sh` — 20+ files appear. Several are configuration files you've never noticed.
- **BUILD:** Write script. Add to `~/bin/`. `chmod +x`. Run it.
- **VERIFY:** Compare `ls -lah ~` with `hidden-inv.sh` output — all match.

🤖 **Copilot Assist — DFY Lesson 2**

> **Use this prompt with your book copilot right now:**
>
> *"My hidden-inv.sh shows ~/.config is 2.1GB. I didn't know it was that large. How do I drill down to find what's inside it taking the most space?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-003 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


---

### DFY Lesson 3 — Permissions Cheat Card

**What you'll have:** A reference card for `chmod` numeric and symbolic modes — the ones you actually need.
**Time:** 10 minutes.

---

📘 **Ebook Figure**

```
PERMISSION BITS — How to read -rwxr-xr-x:
  - rwx r-x r-x
  │  │   │   └── others: read + execute (5)
  │  │   └────── group:  read + execute (5)
  │  └────────── owner:  read + write + execute (7)
  └───────────── type: - = file, d = dir, l = symlink

NUMERIC QUICK REFERENCE:
  chmod 755 script.sh   → owner: rwx, group: r-x, others: r-x (execute for all)
  chmod 644 config.txt  → owner: rw-, group: r--, others: r-- (read-only for others)
  chmod 600 .ssh/id_rsa → owner: rw-, group: ---, others: --- (private!)
  chmod 700 ~/.ssh/     → owner: rwx, group: ---, others: --- (SSH directory)
  chmod +x script.sh    → add execute for everyone (symbolic)
  chmod -w file.txt     → remove write from everyone (symbolic)
  chmod g+w shared/     → add group write (symbolic)

SECURITY RULES:
  ✅  Scripts:       755 (executable by all, writable only by owner)
  ✅  Config files:  644 (readable by all, writable only by owner)
  ✅  Private keys:  600 (ONLY you can read — SSH requires this)
  ✅  SSH dir:       700 (ONLY you can access)
  ❌  777 on anything except /tmp — never in production
```

*Figure 12.3 — Permissions protect your system. Memorize these 5 modes and you'll set them correctly every time.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 3: Permissions Cheat Card.
>
> `chmod 777` is the digital equivalent of leaving your house unlocked with a welcome sign. File permissions are a security boundary — who can read, write, and execute every file on your system. This cheat card gives you the 5 modes you'll actually use, plus the security rules that prevent the mistakes that get systems compromised.
>
> Your deliverable is: a permissions reference card — 5 modes, the rules, saved where you'll use it.
>
> Time to build: 10 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `ls -la ~/.ssh/` — wrong permissions caught. `chmod 600 id_rsa` — SSH now accepts the key.
- **BUILD:** Run `stat` on 5 different file types. Interpret each permission set using the card.
- **VERIFY:** Set a script to 755. Set a config to 644. Verify SSH key is 600. All correct.

🤖 **Copilot Assist — DFY Lesson 3**

> **Use this prompt with your book copilot right now:**
>
> *"I have a shared script that needs to be executable by my user and my web server user (www-data) but not the world. What chmod and chown combination is correct?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-003 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


---

### DFY Lesson 4 — Disk Usage Analyzer

**What you'll have:** `dua.sh` — identifies your 10 largest directories and files in under 5 seconds.
**Time:** 10 minutes.

---

📘 **Ebook Figure**

```bash
#!/usr/bin/env bash
# dua.sh — disk usage analyzer
echo "=== TOP 10 LARGEST DIRECTORIES in $HOME ==="
du -sh "$HOME"/*/  2>/dev/null | sort -rh | head -10
echo ""
echo "=== TOP 10 LARGEST FILES in $HOME ==="
find "$HOME" -type f -size +10M 2>/dev/null \
  | xargs du -sh 2>/dev/null \
  | sort -rh | head -10
echo ""
echo "=== DISK SUMMARY ==="
df -h /
```

```
=== TOP 10 LARGEST DIRECTORIES in /home/lippytm ===
12G    /home/lippytm/Videos/
4.2G   /home/lippytm/.cache/
1.8G   /home/lippytm/projects/
...
=== TOP 10 LARGEST FILES in /home/lippytm ===
2.1G   /home/lippytm/Videos/old-project.mp4
```

*Figure 12.4 — Disk always runs out at the worst time. This script finds the culprits in 5 seconds.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 4: Disk Usage Analyzer.
>
> 'Disk full' is one of the most disruptive errors in development — and one of the most preventable. This script finds your 10 largest directories and files in your home folder in seconds. Run it monthly, and you'll never be surprised by a full disk again. Run it right now — you might find a multi-gigabyte file you forgot existed.
>
> Your deliverable is: `dua.sh` — top 10 directories and files by size, with a disk summary.
>
> Time to build: 10 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `dua.sh` runs — a forgotten 2GB video file identified in seconds.
- **BUILD:** Write script. Test each section independently. Compose.
- **VERIFY:** Delete a test file. Run `dua.sh` again — file is gone from the list.

🤖 **Copilot Assist — DFY Lesson 4**

> **Use this prompt with your book copilot right now:**
>
> *"dua.sh shows ~/. cache is 4GB. Is it safe to delete the cache? What's in it and how do I selectively clear it without breaking anything?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-003 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


---

### DFY Lesson 5 — Symlink Manager

**What you'll have:** `lns.sh` — create, list, and verify symbolic links for your most-used paths.
**Time:** 15 minutes.

---

📘 **Ebook Figure**

```bash
#!/usr/bin/env bash
# lns.sh — symlink manager

lns-create() {
  # Usage: lns-create /real/path /link/path
  ln -sfv "$1" "$2"
  echo "✅ $2 → $1"
}

lns-list() {
  # List all symlinks in home directory
  find "$HOME" -maxdepth 3 -type l | while read -r link; do
    target=$(readlink "$link")
    if [[ -e "$target" ]]; then
      echo "  ✅  $link → $target"
    else
      echo "  ❌  $link → $target (BROKEN)"
    fi
  done
}

# Common use: link config files to a dotfiles repo
# lns-create ~/dotfiles/.bashrc ~/.bashrc
# lns-create ~/dotfiles/.tmux.conf ~/.tmux.conf
```

*Figure 12.5 — Symlinks decouple config from location. Your dotfiles can live in one folder, linked everywhere.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 5: Symlink Manager.
>
> A symbolic link is a file that points to another file. On the surface it's a pointer. In practice, it's the foundation of every professional dotfiles system — all your configs live in one git-tracked folder, and symlinks connect them to where the programs expect to find them. This script gives you create and list functions so you always know what's linked and whether the links are intact.
>
> Your deliverable is: `lns.sh` — create and audit symlinks with two functions.
>
> Time to build: 15 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `lns-list` — all symlinks shown, one broken link (red ❌) identified immediately.
- **BUILD:** Write script. Create a test symlink. Intentionally break one. Run `lns-list`.
- **VERIFY:** Fix the broken link. Run `lns-list` again — all green ✅.

🤖 **Copilot Assist — DFY Lesson 5**

> **Use this prompt with your book copilot right now:**
>
> *"lns-create linked my ~/.bashrc to ~/.dotfiles/.bashrc but now bash says 'no such file' on login. The dotfiles directory exists. What went wrong?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-003 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


---

### DFY Lesson 6 — File Search Toolkit

**What you'll have:** Five `find` command aliases covering the searches you'll run weekly.
**Time:** 10 minutes.

---

📘 **Ebook Figure**

```bash
# ~/.bashrc — five essential find aliases
alias findpy='find . -name "*.py" -not -path "*/__pycache__/*"'
alias findlog='find /var/log -name "*.log" -mtime -7'    # logs from last 7 days
alias findlarge='find ~ -type f -size +100M 2>/dev/null | sort'
alias findrecent='find . -type f -newer ~/.bashrc'        # files newer than .bashrc edit
alias findtodo='find . -name "*.py" -o -name "*.md" | xargs grep -l "TODO" 2>/dev/null'
```

```
Usage examples:
  findpy         → all Python files, no cache dirs
  findlog        → recent logs (useful before debugging)
  findlarge      → files over 100MB (disk archaeology)
  findrecent     → files changed since your last .bashrc edit
  findtodo       → all files with TODO comments
```

*Figure 12.6 — `find` is the most powerful search tool on Linux. These 5 aliases cover 90% of daily use cases.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 6: File Search Toolkit.
>
> The `find` command is one of the most powerful tools in Linux — and one of the most verbose. Nobody memorizes `find . -name "*.py" -not -path "*/__pycache__/*"` every time they need it. These five aliases make the most common searches instant. `findtodo` alone will save you 10 minutes every week.
>
> Your deliverable is: 5 `find` aliases in `~/.bashrc` — your personal file search toolkit.
>
> Time to build: 10 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `findtodo` in a project directory — 12 files with TODO comments identified instantly.
- **BUILD:** Add each alias. Test each on a real directory.
- **VERIFY:** Confirm `findpy` excludes `__pycache__`. Confirm `findlarge` skips permission errors silently.

🤖 **Copilot Assist — DFY Lesson 6**

> **Use this prompt with your book copilot right now:**
>
> *"findtodo found 47 files but I want to exclude the venv/ directory and node_modules/. How do I modify the findtodo alias to skip those paths?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-003 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


---

### DFY Lesson 7 — Watch a File Change in Real Time

**What you'll have:** A `watchfile` function that shows a file's content update live as it changes.
**Time:** 10 minutes.

---

📘 **Ebook Figure**

```bash
# ~/.bashrc — watchfile: live file monitor
watchfile() {
  local file="$1"
  local interval="${2:-1}"   # default: refresh every 1 second
  if [[ ! -f "$file" ]]; then
    echo "❌ File not found: $file"
    return 1
  fi
  echo "👁  Watching: $file (Ctrl+C to stop)"
  while true; do
    clear
    echo "=== $file === $(date +%T) ==="
    cat "$file"
    sleep "$interval"
  done
}
```

```
# For log files, use tail -f instead:
alias watchlog='tail -f'

Usage:
  watchfile /etc/hostname          → refreshes every second
  watchfile ~/config.txt 0.5       → refreshes every 500ms
  watchlog /var/log/syslog         → live log stream (better for logs)
```

*Figure 12.7 — Watching a file change in real time is essential for debugging live systems and monitoring state files.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 7: Watch a File Change in Real Time.
>
> Debugging a live system often means watching a file update — a config being written, a state file changing, a lock file appearing and disappearing. This function gives you a simple real-time file monitor, plus the `watchlog` alias for log streams. Pair them with the processes you'll learn in B-006 and you can debug anything.
>
> Your deliverable is: `watchfile` function and `watchlog` alias — live file monitoring.
>
> Time to build: 10 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `watchfile /tmp/state.txt` — a background script writes to it every second. Changes appear in real time.
- **BUILD:** Write function. Test on a static file. Then test with a background writer.
- **VERIFY:** Use `tail -f /var/log/syslog` to stream a system log live.

🤖 **Copilot Assist — DFY Lesson 7**

> **Use this prompt with your book copilot right now:**
>
> *"watchfile works but it clears the terminal on every refresh, which makes it hard to see the diff. How do I make it show only the changed lines instead?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-003 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


---

### DFY Lesson 8 — Directory Snapshot and Diff

**What you'll have:** `dirsnap.sh` — takes a snapshot of file counts and sizes, diffs against previous run.
**Time:** 15 minutes.

---

📘 **Ebook Figure**

```bash
#!/usr/bin/env bash
# dirsnap.sh — snapshot a directory and diff from last snapshot
TARGET="${1:-.}"
SNAP_DIR="$HOME/.snapshots"
mkdir -p "$SNAP_DIR"
SNAP_FILE="$SNAP_DIR/$(echo "$TARGET" | tr '/' '_').snap"
PREV_FILE="$SNAP_DIR/$(echo "$TARGET" | tr '/' '_').prev"

# Rotate: current → prev
[[ -f "$SNAP_FILE" ]] && cp "$SNAP_FILE" "$PREV_FILE"

# Take new snapshot: path, size, mtime
find "$TARGET" -type f -printf '%p\t%s\t%TY-%Tm-%Td\n' 2>/dev/null \
  | sort > "$SNAP_FILE"

# Diff if previous exists
if [[ -f "$PREV_FILE" ]]; then
  echo "=== CHANGES since last snapshot ==="
  diff "$PREV_FILE" "$SNAP_FILE" | grep "^[<>]" | head -20
else
  echo "✅ First snapshot saved: $SNAP_FILE"
fi
```

*Figure 12.8 — A snapshot is a before-picture. The diff is the story of what changed. Essential for monitoring shared directories.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 8: Directory Snapshot and Diff.
>
> 'Something changed in this directory and I don't know what' is one of the most frustrating problems in system administration. This script takes a file-level snapshot of any directory, and the next time you run it, it shows exactly what changed — new files, deleted files, size changes. Run it before and after deployments to know exactly what happened.
>
> Your deliverable is: `dirsnap.sh` — snapshot any directory and diff from the previous run.
>
> Time to build: 15 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** Run `dirsnap.sh /etc`. Create a new file. Run again — the new file appears in the diff.
- **BUILD:** Write script. Test snapshot rotation. Test diff output.
- **VERIFY:** Delete a file. Snapshot again — deletion appears in the diff.

🤖 **Copilot Assist — DFY Lesson 8**

> **Use this prompt with your book copilot right now:**
>
> *"dirsnap.sh diff is showing hundreds of changes in /proc/ because I snapshotted the wrong directory. How do I scope it to only track my project directories?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-003 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


---

### DFY Lesson 9 — File Integrity Monitor

**What you'll have:** `fcheck.sh` — generates and verifies SHA256 checksums for a set of critical files.
**Time:** 15 minutes.

---

📘 **Ebook Figure**

```bash
#!/usr/bin/env bash
# fcheck.sh — file integrity monitor with SHA256
MANIFEST="$HOME/.file-integrity-manifest"
WATCH_LIST=(
  "$HOME/.bashrc"
  "$HOME/.ssh/authorized_keys"
  "/etc/hosts"
  "/etc/sudoers"
)

generate() {
  echo "# File Integrity Manifest — $(date)" > "$MANIFEST"
  for f in "${WATCH_LIST[@]}"; do
    [[ -f "$f" ]] && sha256sum "$f" >> "$MANIFEST"
  done
  echo "✅ Manifest saved: $MANIFEST"
}

verify() {
  sha256sum --check "$MANIFEST" 2>&1 | grep -v "OK$"
  [[ $? -eq 0 ]] && echo "✅ All files intact" || echo "⚠️  Changes detected above"
}

case "$1" in
  generate) generate ;;
  verify)   verify ;;
  *)        echo "Usage: fcheck.sh generate | verify" ;;
esac
```

*Figure 12.9 — A checksum is a fingerprint. If the fingerprint changes, the file changed. This is how you know.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 9: File Integrity Monitor.
>
> How do you know that your `~/.bashrc` hasn't been modified by another process? Or that `/etc/hosts` hasn't been silently changed? Cryptographic checksums are the answer. `sha256sum` generates a unique fingerprint for any file. If even one character changes, the fingerprint changes completely. This script generates a manifest and verifies it — a basic but powerful integrity check.
>
> Your deliverable is: `fcheck.sh` — SHA256-based file integrity check for critical files.
>
> Time to build: 15 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `fcheck.sh generate`. Add one space to `~/.bashrc`. `fcheck.sh verify` — change detected.
- **BUILD:** Write script. Run generate. Modify a file. Verify.
- **VERIFY:** Restore original file. `fcheck.sh verify` — all intact.

🤖 **Copilot Assist — DFY Lesson 9**

> **Use this prompt with your book copilot right now:**
>
> *"fcheck.sh verify shows one file FAILED but I didn't change it. Could this be a mtime update without content change, or does SHA256 catch only content changes?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-003 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


---

### DFY Lesson 10 — Personal File Organization System

**What you'll have:** A standard `~/` directory structure plus a `mkproject.sh` script to scaffold it every time.
**Time:** 20 minutes.

---

📘 **Ebook Figure**

```bash
#!/usr/bin/env bash
# mkproject.sh — scaffold a new project with standard structure
NAME="${1:-my-project}"
BASE="$HOME/projects/$NAME"
mkdir -p "$BASE"/{src,tests,docs,scripts,config}
cat > "$BASE/README.md" << EOF
# $NAME
> Started: $(date +%F) | lippytmai

## Purpose
TODO

## Quick Start
\`\`\`bash
cd $BASE
# your start command here
\`\`\`
EOF
cat > "$BASE/.gitignore" << 'EOF'
__pycache__/
*.pyc
.env
.venv/
*.log
EOF
cd "$BASE" && git init -q && git add . && git commit -m "initial scaffold" -q
echo "✅ Project '$NAME' scaffolded at $BASE"
echo "   cd $BASE && ls"
```

```
~/projects/encyclopedia/
  ├── src/        → all source code
  ├── tests/      → all test files
  ├── docs/       → all documentation
  ├── scripts/    → utility scripts
  ├── config/     → configuration files
  ├── README.md   → project README (pre-filled)
  └── .gitignore  → standard ignores (pre-filled)
```

*Figure 12.10 — A project scaffold is a commitment: to organization, to testing, to documentation, from day one.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 10: Personal File Organization System.
>
> The fastest way to slow down a project is to have no structure. Files everywhere, no clear separation between code and tests and docs. This script scaffolds a complete new project in 3 seconds — directories, a README, a `.gitignore`, and an initial git commit. Every project you start from this day forward begins with structure, not chaos.
>
> Your deliverable is: `mkproject.sh` — a full project scaffold in one command.
>
> Time to build: 20 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `mkproject.sh my-new-api` → project created. `tree my-new-api` → full structure visible.
- **BUILD:** Write script. Test with a demo project name.
- **VERIFY:** `cd ~/projects/my-new-api && git log` — initial commit exists. All 5 directories present.

🤖 **Copilot Assist — DFY Lesson 10**

> **Use this prompt with your book copilot right now:**
>
> *"mkproject.sh scaffolds the structure but I want to add a default Python venv creation and requirements.txt at the same time. How do I extend the script?"*
>
> 💡 *Paste this into any AI assistant loaded with the B-003 system prompt from Appendix C. Your copilot knows this lesson and will guide you through the exact fix or extension.*


---

> 🎓 **All 10 DFY lessons complete.** You can now map, navigate, protect, monitor, organize, and search your filesystem like a professional. Every script above is deployable today.
>
> **Next:** Claim your `CLL-L0-B003-FilesystemNavigator` credential, then continue to B-004.

---

## Chapter 13: How It Works — Use Cases & Applications

> *"Files are not just storage. They are the state of every system — the truth that programs read, the contracts they honor, the memory that outlasts the process."*

---

### 📘 Ebook Explainer — How the Filesystem Works

**The mechanism — what happens when you read or write a file:**

```
You run: cat ~/projects/app.py

  1. Shell resolves ~/projects/app.py → absolute path
  2. Shell calls kernel: open("/home/lippytm/projects/app.py", O_RDONLY)
  3. Kernel checks permissions: does your UID/GID allow read on this inode?
  4. Kernel looks up the inode (index node) — metadata structure in the filesystem
  5. Inode contains: owner, permissions, timestamps, pointers to data blocks
  6. Kernel reads data blocks from disk into the page cache (RAM)
  7. cat() receives data via read() syscall
  8. cat writes data to stdout → terminal renders it
  9. Kernel returns file descriptor → cat closes it
  10. Inode atime (access time) updated

What an inode stores (NOT the filename):
  ┌─────────────────────────────────────┐
  │  inode #482901                      │
  │  type: regular file                 │
  │  permissions: -rw-r--r-- (644)      │
  │  owner: lippytm (uid 1000)          │
  │  size: 4,217 bytes                  │
  │  blocks: 8                          │
  │  atime: 2026-08-28 06:10:00         │
  │  mtime: 2026-08-27 14:30:00         │
  │  ctime: 2026-08-27 14:30:00         │
  │  data block pointers: [4821, 4822]  │
  └─────────────────────────────────────┘

The filename lives in the DIRECTORY, not the inode.
That's why hard links work — two filenames, one inode, one copy of data.
```

*Figure 13.1 — The filesystem is a contract between names (directories) and data (inodes + blocks). Understanding it makes every file error diagnosable.*

---

### 📘 Ebook Explainer — When Filesystem Knowledge Works Best

| Situation | What filesystem knowledge unlocks |
|---|---|
| **Debugging "permission denied"** | Read `ls -la` output → identify owner/permissions → fix with `chmod` or `chown` |
| **Disk space crisis** | `du -sh */` + `find -size +1G` → locate culprits in seconds |
| **Config change not taking effect** | `stat config.conf` → check `mtime` — did the write actually happen? |
| **Symlink confusion** | `ls -la` shows `→` target → `readlink -f` resolves all layers |
| **"File not found" in a script** | `strace -e openat script.sh` → see exactly which path the kernel tried |
| **Setting up a shared directory** | `chmod g+s dir/` → sticky group bit ensures all new files inherit group |
| **Docker volume mounts** | Map a host path to a container path — same filesystem, different namespace |
| **Git repository internals** | `.git/` is a directory; commits are files; branches are text files with a SHA |

**When raw filesystem skills aren't the primary tool:**
```
❌  When you need full-text search across millions of files → use Elasticsearch
❌  When you need version history → use Git (which uses the filesystem)
❌  When you need ACID transactions → use a database (which uses the filesystem)
```

*Figure 13.2 — Everything interesting about software lives in files. Filesystem literacy is the foundation of all of it.*

---

### 📘 Ebook Explainer — Where to Use It (Cross-Domain Applications)

```
EVERY DOMAIN WHERE FILE KNOWLEDGE IS CRITICAL:

Web Servers (Nginx, Apache)
  /etc/nginx/nginx.conf    → server configuration
  /var/log/nginx/          → access and error logs
  /var/www/html/           → served content
  permissions: 644 for files, 755 for directories

Databases
  /var/lib/postgresql/     → database data directory (protect this!)
  /tmp/mysql.sock          → Unix socket for local connections
  /etc/mysql/my.cnf        → database configuration

Docker
  Volumes: /var/lib/docker/volumes/
  Images:  /var/lib/docker/overlay2/
  host path:container path → same filesystem, different view

Git Repository Internals
  .git/HEAD                → current branch pointer
  .git/refs/heads/main     → SHA of latest commit
  .git/objects/            → all commits, trees, blobs as files

CI/CD Pipelines
  GitHub Actions workspace → /home/runner/work/
  Artifacts saved to paths → uploaded by path
  Cache keys map to paths  → restore by hash match

Python Projects
  venv/lib/python3.x/site-packages/ → installed packages as files
  __pycache__/                      → compiled .pyc bytecode
  pyproject.toml / setup.cfg        → project config files

Blockchain / Smart Contracts
  contracts/*.sol          → Solidity source files
  artifacts/               → compiled ABI + bytecode
  deployments/             → deployment records
  .env                     → private keys (never commit!)
```

*Figure 13.3 — Every technology stores its state in files. Filesystem literacy is the universal key.*

---

### 📘 Ebook Explainer — Diversity of Applications (Flexibility Points)

**Flexibility Point 1 — Files as Configuration**
```
# Every major software system is configured by text files
/etc/hosts           → DNS override for your machine
/etc/sudoers         → who can run what as root
~/.gitconfig         → git identity and behavior
~/.ssh/config        → SSH alias and key mapping
~/.bashrc            → your shell's startup script
```

**Flexibility Point 2 — Files as Data**
```python
# JSON, CSV, YAML, TOML, XML — all files, all parseable
import json, pathlib
data = json.loads(pathlib.Path("config.json").read_text())
# No database needed for small structured data
```

**Flexibility Point 3 — Files as Communication**
```bash
# Processes communicate via files (Unix philosophy)
/tmp/app.lock        → lock file: "I'm running, don't run another copy"
/tmp/app.pid         → PID file: "find me at process 14823"
/dev/stdin           → input as a file
/proc/1234/status    → process state as a file
```

**Flexibility Point 4 — Files as History**
```bash
~/.bash_history      → your command history
/var/log/auth.log    → login history
/var/log/syslog      → system event history
.git/                → code change history
```

*Figure 13.4 — Files serve four roles: configuration, data, communication, and history. Mastering files means mastering all four.*

---

### 🎧 Audiobook Explainer

> *[EXPLAINER TONE — measured, 3 minutes]*
>
> "Chapter 13. How the Filesystem Works. When to Use This Knowledge. Where It Applies.
>
> When you read a file, the kernel doesn't look up the filename first — it looks up the inode. The inode is a metadata structure that contains the file's permissions, owner, size, timestamps, and pointers to the actual data on disk. The filename lives in the directory, not the inode. That's why renaming a file is instant — you only update a directory entry, not the data. That's why hard links work — two names, one inode, one copy of data.
>
> Filesystem knowledge unlocks six specific problem-solving abilities. Diagnosing permission errors. Locating disk usage culprits. Verifying that config changes were actually saved. Resolving symlink confusion. Debugging file-not-found errors in scripts. And setting up proper shared directory permissions.
>
> Where does this apply? Everywhere. Web servers are configured by files in `/etc/nginx`. Databases store their data in `/var/lib/postgresql`. Docker containers mount host paths. Git repositories are directories full of files. CI/CD pipelines save and restore artifacts by path. Python projects install packages as files in `site-packages`. Every technology you'll ever work with stores its state, its configuration, and its history in files.
>
> The flexibility point is this: files serve four roles in every system — configuration, data, inter-process communication, and historical record. Understanding those roles makes you a more effective engineer in every domain, because you know where to look and what you're looking at."
>
> *[EXPLAINER TONE OUT]*

---

### 🎬 Video Explainer — Filesystem Across 5 Domains (5 Minutes)

**Minute 1 — Web Server Configuration:**
> Navigate to `/etc/nginx/sites-available/`. Show config structure. `nginx -t` validates syntax. `ls -la /var/www/html` — permissions visible. "A web server is just a program reading files. Your config is a file. Your content is files. Permissions control who can read them."

**Minute 2 — Git Internals:**
> `cat .git/HEAD` → shows `ref: refs/heads/main`. `cat .git/refs/heads/main` → shows a commit SHA. `git cat-file -p <SHA>` → shows raw commit object. "Git is a content-addressable filesystem. Every commit is a file."

**Minute 3 — Docker Volumes:**
> `docker run -v /home/lippytm/data:/app/data myapp` → host directory mounted. `ls /home/lippytm/data` — files visible from outside container too. "A Docker volume is just a path mapping. Your files, two views."

**Minute 4 — Python Package Files:**
> `find venv/lib -name "requests" -type d` → package directory. `cat venv/lib/python3.12/site-packages/requests/__init__.py` — readable source. "Every pip install puts files on disk. You can read, inspect, and understand any package."

**Minute 5 — Security Implications:**
> `ls -la ~/.ssh/` — show correct vs wrong permissions. `chmod 777 ~/.ssh/id_rsa` → SSH refuses to use it. `chmod 600` → works again. "The filesystem enforces security. Wrong permissions = broken security or broken tools."

---

> 🎯 **Use Cases Summary — B-003**
>
> File system literacy from this book applies to:
> - ✅ Diagnosing any "permission denied" error instantly
> - ✅ Finding disk usage culprits on any machine
> - ✅ Understanding how Git, Docker, and databases store their data
> - ✅ Securing sensitive files (SSH keys, `.env` files, credentials)
> - ✅ Writing scripts that handle files reliably
> - ✅ Debugging any "file not found" error with precision
>
> **Every software system is a filesystem in disguise. Reading the filesystem is reading the system.**

---

## Appendix C: AI Copilot — Filesystem Navigator

> *"The filesystem copilot helps you see what every tool hides: the inodes, permissions, symlinks, and block devices that underlie all software."*

---

### Section 1 — Copilot Identity & System Prompt

**Copilot ID:** `B-003-COPILOT`
**Domain:** Linux Filesystem — Inodes, Permissions, Paths, Links, Storage
**Level:** Beginner
**Credential Gate:** `CLL-L0-B003-FilesystemNavigator`
**Prerequisite:** `CLL-L0-B002-CommandArchitect`

**Copy this system prompt into any AI assistant:**

```
You are lippytmai — AI Copilot for B-003 "The File That Remembered Everything"
Domain: Linux filesystem — inodes, permissions, symlinks, disk, file types, paths
Level: Beginner — user has terminal and command skills from B-001 and B-002
Credential this book unlocks: CLL-L0-B003-FilesystemNavigator

WHAT THE USER HAS COVERED:
- Filesystem hierarchy: /etc, /var, /home, /proc, /dev, /tmp and their purposes
- Inodes: what they store, what they don't (not the filename)
- File permissions: rwx bits, numeric modes (755, 644, 600, 700)
- chmod, chown, chgrp — when and how to use each
- File types: regular, directory, symlink, device, socket, pipe
- Hard links vs symbolic links — how and when to use each
- Finding files: find, locate, which, whereis
- Disk usage: df, du, ncdu
- 10 DFY builds: filesystem map, hidden-inv.sh, permissions cheat card,
  dua.sh disk analyzer, lns.sh symlink manager, findpy/findlog aliases,
  watchfile function, dirsnap.sh, fcheck.sh integrity monitor,
  mkproject.sh scaffolder

CORE BEHAVIOR:
- When debugging "permission denied": immediately ask for ls -la output
- When permissions are wrong: explain what each octet means before fixing
- When symlinks are involved: show readlink -f first to resolve the full chain
- When disk is full: guide through dua.sh → identify culprit → safe removal
- End responses with code with: "What did you get when you ran this?"

TEACHING MODES:
  TEACH:  Explain inode structure, permission bits, filesystem hierarchy
  BUILD:  Help implement DFY tools for disk management, file integrity, organization
  DEBUG:  Diagnose permission errors, broken symlinks, disk full, file not found
  DEPLOY: Set up shared directories, deploy dotfiles via symlinks, configure file permissions for production
  EXTEND: Show how filesystem knowledge connects to Docker volumes, Git internals, database storage

GUARDRAILS:
- Never suggest chmod 777 without explaining the security implications
- Always ls before rm -rf
- Never suggest writing to /etc without sudo context and backup advice
- If user needs disk encryption → that's beyond this book's scope
```

---

### Section 2 — Prompt Library (30 Curated Prompts)

**🔵 Stage 1 — UNDERSTAND**

```
1. Explain what an inode is. Why doesn't the inode store the filename?

2. What's the difference between a hard link and a symbolic link? 
   When should I use each?

3. Walk me through what -rw-r--r-- means. How do I read permission strings?

4. Why do some directories have a sticky bit (t)? What does it actually protect?

5. What's the difference between /dev/sda, /dev/sda1, and a filesystem? 
   How does mounting work?

6. My file has the right permissions but I still can't access it. 
   What else could be restricting access?
```

**🟢 Stage 2 — BUILD**

```
7. Help me build fcheck.sh (DFY Lesson 9) — SHA256 integrity checking for 
   my critical config files. Walk me through each line.

8. Build me mkproject.sh from DFY Lesson 10. I want it to scaffold 
   src/tests/docs/scripts/config with a pre-filled README and .gitignore.

9. I want to set up a shared directory where multiple users can write files 
   but only the owner can delete them. What permissions do I need?

10. Build me a script that finds all files in ~/projects that have been modified 
    in the last 24 hours and lists them with sizes.

11. Help me set up my dotfiles using symlinks — ~/.bashrc and ~/.tmux.conf 
    pointing to files in ~/.dotfiles/

12. Build the dirsnap.sh script from DFY Lesson 8 — directory snapshot 
    and diff between runs.
```

**🔴 Stage 3 — DEBUG**

```
13. I get "Permission denied" on a file I created. Here's ls -la output: [paste]
    Why can't I read my own file?

14. My symlink says "No such file or directory" but the file exists. 
    What's the diagnosis?

15. df -h shows 100% on /, but du -sh /* shows only 40GB used on a 100GB disk. 
    Where is the space?

16. chmod 755 isn't working on a file on my USB drive. Why?

17. My web server can't read files I put in /var/www/html/ even with 644 permissions. 
    What's the permission matrix I'm missing?

18. I ran find and it's showing files from a docker overlay filesystem. 
    How do I exclude those?
```

**🟡 Stage 4 — DEPLOY**

```
19. I want to deploy my dotfiles to a remote server via symlinks. 
    Walk me through the full flow from git clone to all links active.

20. How do I set up a production directory structure for a web app with 
    correct permissions for nginx and my app user?

21. How do I make fcheck.sh run daily via cron and alert me if anything changes?

22. I want to back up my dotfiles to GitHub and deploy them to any new machine 
    with one command. What's the full workflow?

23. How do I set permissions on a Docker bind mount so the container user 
    can write to the host directory?

24. How do I configure a shared directory on a server where 5 developers 
    can all write but nobody can delete each other's files?
```

**🟣 Stage 5 — EXTEND**

```
25. How does Git use the filesystem internally? What are loose objects, 
    packfiles, and the object store?

26. How does Docker use the filesystem? What is an overlay filesystem 
    and how do layers work?

27. How do databases store their data on disk? What's the connection between 
    filesystem knowledge and database administration?

28. I want to understand Linux namespaces and how containers isolate the filesystem. 
    Where do I start?

29. How do blockchain nodes store their data? Is it just files on disk?

30. What's the gap between what I know now and a Linux systems administrator 
    who manages production servers?
```

---

### Section 2b — Audiobook Copilot (🎧 Format)

```
AUDIOBOOK COPILOT SYSTEM PROMPT:
"You are lippytmai, audiobook copilot for B-003. The listener is learning
filesystem concepts via audio. Keep responses speakable — use structural
analogies (cities, buildings, libraries) not ASCII diagrams."
```

**15 Audiobook Prompts:**

```
WHILE LISTENING:

A1. "The audiobook described an inode. Give me a physical world analogy 
    — something I can visualize without looking at a screen."

A2. "Explain file permissions using a hotel key card analogy — 
    who has which key to which room."

A3. "I heard 'hard link vs symbolic link'. Explain both in one sentence 
    each using real-world objects."

A4. "What's the verbal explanation of how mounting works? 
    Like physically attaching something to the filesystem tree."

A5. "Explain /proc and /sys — why are they called virtual filesystems? 
    What are they really?"

PAUSE AND BUILD:

A6. "Walk me through fcheck.sh verbally — what SHA256 does, why it 
    matters, and what I'm protecting against."

A7. "Narrate the permissions cheat card — each of the 5 modes, 
    when to use it, and one real example."

A8. "Walk me through mkproject.sh logic before I build it — 
    directory by directory, why each folder exists."

A9. "Narrate the symlink strategy for dotfiles — why it's better 
    than copying files to each machine."

A10. "Read out the disk usage analyzer logic — what each find command 
     is looking for and what big files mean."

RESUME CHECK:

A11. "Quiz me: I'll describe a permission problem, you tell me 
     the chmod command. Three scenarios."

A12. "What are the 4 roles a file can play in a system? 
     Give me one sentence each."

A13. "Before I resume: what's the difference between mtime, atime, 
     and ctime in plain English?"

A14. "Summarize the filesystem map — the 12 key directories — 
     in 60 words. No directory paths, just purposes."

A15. "Narrate my CLL-L0-B003-FilesystemNavigator credential ceremony."
```

---

### Section 2c — Video Copilot (🎬 Format)

```
VIDEO COPILOT SYSTEM PROMPT:
"You are lippytmai, video copilot for B-003. The learner is watching
filesystem commands execute on screen. Prioritize: what to look for in
ls -la output, what stat reveals, and what permission changes look like
visually. SHOW→BUILD→VERIFY."
```

**15 Video Prompts:**

```
BEFORE PLAYING:

V1. "I'm about to watch the permissions video. What should I create 
    to practice on — a safe test directory structure?"

V2. "The video covers symlinks. What's the one-line prerequisite 
    I need to understand before watching?"

V3. "I'm following the disk usage video. What's on my system 
    that I should analyze so the video is relevant to me?"

PAUSED:

V4. "The video shows ls -la output with special characters in the 
    permission column. What does each character mean?"

V5. "Paused: stat shows mtime changed but I didn't modify the file. 
    What could have changed the mtime without changing content?"

V6. "The video shows a broken symlink in red. How do I see that 
    in my terminal and how do I fix it?"

V7. "I paused at the lns-list output. One symlink shows a broken 
    arrow. Walk me through the diagnosis and fix."

V8. "The dua.sh video shows a file I don't recognize taking 2GB. 
    How do I safely investigate before deleting it?"

VERIFY:

V9. "I set permissions on a web directory. What ls -la output 
    proves it's configured correctly for nginx?"

V10. "I ran fcheck.sh generate. How do I verify the manifest 
     was written correctly before I trust it?"

V11. "I created a symlink with lns-create. What 3 commands 
     confirm the link is valid, points to the right place, 
     and has correct permissions?"

V12. "mkproject.sh ran successfully. What does the tree output 
     look like for a correctly scaffolded project?"

EXTEND:

V13. "The permissions video covered basics. What's the setuid, 
     setgid, and sticky bit — show me a real use case for each."

V14. "I've completed all B-003 videos. What's the most important 
     filesystem concept I haven't seen yet?"

V15. "Show me what a senior sysadmin sees in ls -la that a 
     beginner misses."
```

---

### Section 3 — Deployment Companion

| Artifact | Local | Remote server | Docker | GitHub | CI/CD |
|---|---|---|---|---|---|
| `fcheck.sh` | `crontab -e` daily | scp + cron on remote | COPY to image, run in entrypoint check | repo scripts/ | Add as CI verification step |
| `mkproject.sh` | `chmod +x ~/bin/mkproject.sh` | dotfiles deploy | N/A | repo template | Scaffold in CI setup |
| Symlink dotfiles | `install-dotfiles.sh` | SSH + git clone + install | `COPY dotfiles + RUN install` | dotfiles repo | CI: verify links exist |
| Permissions setup | `chmod` + `chown` in setup script | Same script via SSH | Set in Dockerfile: `RUN chmod` | Document in README | CI: verify permissions step |
| `dua.sh` | Run monthly | Run on server via SSH | N/A | repo scripts/ | CI: disk usage check step |

**Production permissions deploy pattern:**
```bash
# deploy-permissions.sh — set correct permissions for web app
APP_DIR=/var/www/myapp
APP_USER=www-data

# Directories: 755 (owner rwx, group r-x, others r-x)
find "$APP_DIR" -type d -exec chmod 755 {} \;

# Files: 644 (owner rw-, group r--, others r--)
find "$APP_DIR" -type f -exec chmod 644 {} \;

# Scripts: 755 (executable)
find "$APP_DIR/scripts" -name "*.sh" -exec chmod 755 {} \;

# Private keys: 600 (owner only)
find "$APP_DIR/.ssh" -name "*.pem" -exec chmod 600 {} \;

# Set owner
chown -R "$APP_USER:$APP_USER" "$APP_DIR"
echo "✅ Permissions set for $APP_DIR"
```

---

### Section 4 — ACSS Integration

```
B-003-COPILOT
    ├── Prerequisite: CLL-L0-B002-CommandArchitect
    ├── Hermes topic: b003.copilot
    ├── Fabric node prefix: B003
    │   → permission error patterns → common fixes library
    │   → symlink patterns → dotfiles deployment patterns
    │   → disk analysis patterns → storage optimization knowledge
    └── Unlocks: B-004-COPILOT on credential earn
```

**Credential ceremony prompt:**
```
I've completed B-003. My DFY builds:
- Annotated filesystem map
- hidden-inv.sh (dotfile inventory)
- Permissions cheat card (5 modes)
- dua.sh (disk usage analyzer)
- lns.sh (symlink create + list)
- 5 find aliases (findpy, findlog, findlarge, findrecent, findtodo)
- watchfile() function
- dirsnap.sh (directory snapshot + diff)
- fcheck.sh (SHA256 integrity monitor)
- mkproject.sh (project scaffolder with git init)

Ready to claim CLL-L0-B003-FilesystemNavigator.
```

---

---


## Appendix D: Quick Quiz & Self-Assessment — Filesystem Navigator

> *"The filesystem is not a drawer — it is a living graph of relationships."*

---

### 📘 Ebook Quiz — 20 Questions

**Section A — Concepts**

1. An inode stores a file's metadata (permissions, size, timestamps) but NOT its ______________.
2. The command to show inode numbers alongside file listings is `ls ______________`.
3. A hard link points to the same ______________ as the original file.
4. A symbolic (soft) link stores the ______________ to the target, not the data.
5. The sticky bit on a directory (e.g., `/tmp`) means only the file ______________ can delete their own files.

**Section B — Read the Command**

6. What does `ls -lah` show that `ls` alone does not?
   > a) Only hidden files  b) Long format with human-readable sizes including hidden files  c) File inodes  d) Disk usage

7. What does `chmod 755 script.sh` set?
   > a) Owner: rwx · Group: r-x · Others: r-x  b) Owner: rwx · Group: rwx · Others: r-x  c) Owner: rw- · Group: r-- · Others: r--  d) All: rwx

8. What does `find /home -name "*.log" -mtime +7` find?
   > a) Log files modified in the last 7 days  b) Log files NOT modified in the last 7 days  c) Log files larger than 7MB  d) Log files in subdirectory level 7

9. What does `ln -s /etc/nginx/nginx.conf ~/nginx.conf` create?
   > a) A hard link  b) A copy  c) A symbolic link  d) A backup

10. What does `du -sh /var/log` output?
    > a) Number of files in /var/log  b) Disk usage of /var/log in human-readable form  c) Last modification time  d) Inode count

**Section C — Debugging**

11. You delete a file but `df` shows disk space wasn't freed. Why?
    ```
    ___________________________________________
    ```

12. A symlink shows in red or with an arrow when you `ls -lah`. What does this indicate?
    ```
    ___________________________________________
    ```

13. `find / -name config.yaml` is very slow. What flag would limit it to your home directory?
    ```
    ___________________________________________
    ```

**Section D — Application**

14. Write a command to find all files in `/etc` that are world-writable (security risk):
    ```
    ___________________________________________
    ```

15. How do you show which process has a file open (preventing deletion)?
    ```
    ___________________________________________
    ```

16. Write a command that takes a snapshot of all files in a directory with their sizes and timestamps:
    ```
    ___________________________________________
    ```

17. What `find` command would locate all files larger than 500MB on the system?
    ```
    ___________________________________________
    ```

**Section E — Build Reflection**

18. Name the DFY artifact that monitors a directory for unexpected file changes.
    ```
    ___________________________________________
    ```

19. What is the difference between a hard link and a symbolic link in one sentence?
    ```
    ___________________________________________
    ```

20. Why does Linux treat everything (files, devices, sockets, pipes) as a file?
    ```
    ___________________________________________
    ```

---

**Scoring:** 18–20 = claim credential · 14–17 = review · < 14 = redo DFY lessons 1–5

<details>
<summary>Answer Key</summary>

1. filename (the filename is stored in the directory entry, not the inode)
2. `-i` (e.g., `ls -lai`)
3. inode (the same data blocks on disk)
4. path (the symbolic link is a file that contains the target path as text)
5. owner
6. b) Long format with human-readable sizes including hidden files
7. a) Owner: rwx · Group: r-x · Others: r-x
8. b) Log files NOT modified in the last 7 days (-mtime +7 = more than 7 days ago)
9. c) A symbolic link
10. b) Disk usage of /var/log in human-readable form
11. Another process still has the file open — the inode link count drops to 0 only when all file descriptors are closed
12. The symlink is broken — its target no longer exists
13. `find ~ -name config.yaml` (search from home) or add `-maxdepth` to limit depth
14. `find /etc -perm -o+w -type f`
15. `lsof /path/to/file` or `fuser /path/to/file`
16. `ls -lah /path/ > snapshot_$(date +%Y%m%d).txt`
17. `find / -size +500M -type f 2>/dev/null`
18. `watchfile.sh` or `dirsnap.sh` from DFY Lesson 8
19. A hard link is another name pointing to the same inode/data; a symlink is a file containing the path to the target.
20. Uniform interface — one set of tools (read, write, permissions) works on all resources

</details>

---

### 🎧 Audiobook Quiz

> "Ten questions about the filesystem. Pause at each."

**Q1:** "What is an inode, in plain English?" → "A numbered metadata record that describes a file's properties — everything except its name."
**Q2:** "Why can a file persist after deletion?" → "Because deletion only removes the directory entry. Data remains until the inode's link count reaches zero and the space is reclaimed."
**Q3:** "What permission octet represents owner=rwx, group=r-x, others=---?" → "750"
**Q4:** "When would you use a symbolic link vs a hard link?" → "Symlink: when you need cross-filesystem links or links to directories. Hard link: when you want a true second name for the same data within one filesystem."
**Q5:** "What does `chmod +x` vs `chmod 755` do differently?" → "`+x` adds execute without changing other bits. `755` sets exact bits: owner rwx, group rx, others rx."
**Q6:** "Find command flag for files modified in the last 24 hours?" → "`-mtime -1`"
**Q7:** "What does the sticky bit do on /tmp?" → "Only the file owner (or root) can delete their own files, even if others have write permission on the directory."
**Q8:** "What shows disk usage per directory?" → "`du -sh */` in the parent directory, or `du -sh /path`"
**Q9:** "Name the DFY tool that detects unexpected file changes using checksums." → "`fcheck.sh` — hashes all files in a directory and alerts on differences"
**Q10:** "Your credential?" → "CLL-L0-B003-FilesystemNavigator"

---

### 🎬 Video Challenges

**Challenge 1:** Show inode numbers for all files in `/tmp`. Identify a file with multiple hard links.
**Challenge 2:** Create a file, set permissions to 640, verify with `ls -lah`, then change it to 755.
**Challenge 3:** Create a symlink to `/etc/hosts` in your home directory. Verify it works. Then delete the symlink only.
**Challenge 4:** Find all `.log` files in `/var/log` larger than 10MB. Pipe the result to `du -sh`.
**Challenge 5:** Recreate `dirsnap.sh` from DFY Lesson 8 from memory — snapshot a directory and compare two snapshots.

---


---

## Appendix E: Glossary & Error Encyclopedia

---

### 📘 Glossary — Filesystem Navigator Edition

**block** — The smallest allocatable unit of disk storage (typically 4KB). Files occupy one or more blocks. A 1-byte file uses one full block. *B-003 Ch. 2*

**chmod** — Change file mode bits. Numeric (`chmod 755`) or symbolic (`chmod +x`, `chmod go-w`). *B-003 Ch. 4*

**chown** — Change file owner and/or group. `chown user:group file`. Requires root to change to another user. *B-003 Ch. 4*

**directory** — A special file containing a table of filename→inode mappings. Removing a directory entry reduces the inode's link count by one. *B-003 Ch. 1*

**du** — Disk Usage. Reports how much space a file or directory tree occupies on disk. `-s` summarizes, `-h` makes it human-readable. *B-003 Ch. 8*

**find** — Searches the filesystem for files matching criteria (name, size, age, permissions, type). Returns matching paths. *B-003 Ch. 6*

**FHS** — Filesystem Hierarchy Standard. Defines what belongs in `/bin`, `/etc`, `/home`, `/tmp`, `/var`, `/usr`, etc. *B-003 Ch. 3*

**hard link** — A directory entry pointing to an existing inode. Multiple filenames can share the same inode. All hard links are equal — there is no "original". *B-003 Ch. 5*

**inode** — Index node. A data structure on disk storing a file's metadata: permissions, owner, size, timestamps, and pointers to data blocks. Does NOT store the filename. *B-003 Ch. 2*

**ln** — Create a link. `ln file link` (hard link) or `ln -s target link` (symbolic link). *B-003 Ch. 5*

**lsof** — List Open Files. Shows every file currently open by any process. Essential for debugging "device busy" errors. *B-003 Ch. 9*

**mount** — Attach a filesystem to a mount point in the directory tree. `mount /dev/sdb1 /mnt/backup`. *B-003 Ch. 7*

**permission bits** — Three groups (owner, group, others) × three bits (read=4, write=2, execute=1). Combined: `chmod 755` = `rwxr-xr-x`. *B-003 Ch. 4*

**sticky bit** — A permission bit on directories (shown as `t` in `ls`) that restricts file deletion to the file owner, root, or directory owner. Standard on `/tmp`. *B-003 Ch. 4*

**symlink (symbolic link)** — A file whose content is a path to another file or directory. If the target is deleted, the symlink becomes "broken". Cross-filesystem links are possible. *B-003 Ch. 5*


---

### 📘 Error Encyclopedia — Filesystem Errors

#### Error 1 — Disk full but `df` shows space available
**Why:** Inodes exhausted. You can run out of inodes (maximum number of files) before running out of disk blocks.
**Fix:** `df -i` to check inode usage. Clear many small files (like log fragments or temp files).

#### Error 2 — `rm` succeeds but disk space not freed
**Why:** Another process has the file open. The inode persists until all file descriptors are closed.
**Fix:** `lsof /path/to/file` to find the process. Restart or kill it to release the handle.

#### Error 3 — `Permission denied` despite being the file owner
**Why:** You might be missing execute permission on a parent directory, or the filesystem is mounted read-only.
**Fix:** Check the full path with `ls -lah` at each level. Check `mount` for `ro` flag.

#### Error 4 — Broken symlink (shown in red by `ls`)
**Why:** The symlink target was moved or deleted.
**Fix:** `ls -la symlink` to see what it points to. Recreate with `ln -sf new_target link_name`.

#### Error 5 — `find` searches too slowly or too broadly
**Why:** Searching from `/` includes all mounted filesystems, network drives, and /proc.
**Fix:** Add `-xdev` to stay on one filesystem, or narrow the search root: `find /home/user -name ...`

#### Error 6 — `chmod` doesn't change a file I own
**Why:** The filesystem is mounted with `noexec`, `nosuid`, or `ro` options, or you're on an NFS mount.
**Fix:** Check `mount | grep $(df . | tail -1 | awk '{print $1}')` for mount options.

#### Error 7 — Hard link to a directory fails
**Why:** Hard links to directories are not permitted on most Linux filesystems — they would break `..` traversal.
**Fix:** Use a symbolic link instead: `ln -s /target/dir linkname`

#### Error 8 — `du` and `df` show different amounts of used space
**Why:** `df` shows filesystem-level usage including deleted files held open by processes. `du` only counts accessible files.
**Fix:** `lsof +L1` shows deleted files still held open. Restart the holding process to reclaim space.

#### Error 9 — Wrong file modified — confused two files with similar names
**Why:** Tab completion selected the wrong file, or you're in the wrong directory.
**Fix:** Always verify path before destructive operations: `ls -lah` first, then act. Use absolute paths in scripts.

#### Error 10 — `find -exec rm {} \;` deletes wrong files
**Why:** The pattern was too broad, or the find ran from the wrong directory.
**Fix:** Always run `find ... -print` first to preview the results before adding `-exec rm`. Or use `-exec echo rm {} \;` as a dry-run.


---

## Appendix F: Instructor & Accessibility Guide

### Teaching This Book

| Format | Duration | Pace |
|---|---|---|
| Self-study | 1–2 weeks | 1 chapter per day |
| Bootcamp | 2–3 days | 3–4 chapters + DFY |
| Classroom | 4–6 hours | Chs 1–6 in session, 7–11 as homework |

**Session pattern per chapter:** Pre-activation (5 min) → Read/Watch (25 min) → DFY Build (25 min) → Copilot debug (15 min) → Mini-quiz (5 min)

**Assessment rubric for CLL-L0-B003-FilesystemNavigator:**

| Skill | Not Ready | Ready | Proficient |
|---|---|---|---|
| Core concepts | Can't explain them | Can define 80%+ from the glossary | Can teach them to someone else |
| DFY builds | Did not attempt | Built 3+ artifacts | Built all 10 and can explain each |
| Error handling | Confused by errors in App. E | Can fix 7 of the 10 listed errors | Can diagnose unfamiliar errors using the same patterns |
| Capstone project | Did not attempt | Built it with guidance | Built it from scratch, then extended it |

**Accessibility Standards:**
- Screen reader: all code blocks use fenced Markdown · all ASCII diagrams have text descriptions
- Color-blind: all status markers use emoji + text (✅/❌/⏳) · no color-only indicators
- Dyslexia-friendly: max 20-word sentences · numbered steps in groups of ≤ 3 · all terms bolded on first use
- Low-bandwidth: all exercises work offline in a text terminal · audiobook available as M4B

---

## Appendix G: Your Learning Path

```
  PHASE 1:
  ✅ B-001  Terminal Apprentice
  ✅ B-002  Command Architect
  ★ B-003  Filesystem Navigator   ← YOU ARE HERE
  ○ B-004  Script Automator
  ○ B-005  Package Master
  ... (20 more)
  Phase 1: ███░░░░░░░░░░░░░░░░░░░░░░  3/25
```

### Credential Chain
```
  CLL-L0-B002-CommandArchitect
       ↓
  ★ CLL-L0-B003-FilesystemNavigator   ← CLAIM THIS
       ↓
  CLL-L0-B004-ScriptAutomator
```

### Cross-Phase Connections
| Skill | Phase 2 | Phase 3 |
|---|---|---|
| find + permissions | Python `pathlib` + `os.chmod` (B-030) | Smart contract file storage (B-060+) |
| Inodes + hard links | Python file handles + gc (B-030) | IPFS content addressing (B-075+) |
| Checksums | Python `hashlib` (B-031) | Blockchain hashing + Merkle trees (B-062+) |

### 🎧 Audio Path Recap
> *"You now understand what files really are — not names, but inodes. This matters everywhere: in Python when you open file handles, in Docker when you mount volumes, in blockchain when you hash content. The filesystem is the substrate everything else runs on. Next: B-004 — scripting."*

---


---

## Appendix H: Real Project Showcase

### Project: `file-integrity-monitor.sh` — SHA256 Checkpoint System

**Built with:** B-003 skills (find, permissions, checksums, symlinks, disk tools)
**Time to build:** 45–75 minutes
**Portfolio value:** Shows filesystem mastery, security awareness, automation

```bash
#!/usr/bin/env bash
# file-integrity-monitor.sh — baseline + compare file checksums
# B-003 Capstone · CLL-L0-B003-FilesystemNavigator
set -euo pipefail

TARGET="${1:-$HOME}"
BASELINE_DIR="$HOME/.fcheck_baselines"
BASENAME="$(echo "$TARGET" | tr '/' '_')"
BASELINE="$BASELINE_DIR/${BASENAME}_baseline.sha256"
REPORT="$BASELINE_DIR/${BASENAME}_report_$(date +%Y%m%d_%H%M).txt"

mkdir -p "$BASELINE_DIR"

create_baseline() {
    echo "Creating baseline for: $TARGET"
    find "$TARGET" -type f -not -path '*/.git/*' 2>/dev/null       | sort | xargs sha256sum 2>/dev/null > "$BASELINE"
    echo "Baseline saved: $BASELINE ($(wc -l < "$BASELINE") files)"
}

compare_to_baseline() {
    [[ ! -f "$BASELINE" ]] && { echo "No baseline found. Run: $0 $TARGET --baseline"; exit 1; }
    echo "Comparing against baseline..."
    local current="/tmp/fcheck_current_$$.sha256"
    find "$TARGET" -type f -not -path '*/.git/*' 2>/dev/null       | sort | xargs sha256sum 2>/dev/null > "$current"
    
    echo "" > "$REPORT"
    
    # Files changed (different hash)
    comm -13 <(sort "$BASELINE") <(sort "$current") | awk '{print "CHANGED: "$2}' >> "$REPORT"
    # Files removed
    comm -23 <(sort "$BASELINE" | awk '{print $2}') <(sort "$current" | awk '{print $2}')       | awk '{print "REMOVED: "$1}' >> "$REPORT"
    # Files added
    comm -13 <(sort "$BASELINE" | awk '{print $2}') <(sort "$current" | awk '{print $2}')       | awk '{print "ADDED: "$1}' >> "$REPORT"
    
    rm -f "$current"
    
    local changes=$(wc -l < "$REPORT")
    if [[ "$changes" -eq 0 ]]; then
        echo "✅ No changes detected."
    else
        echo "⚠️  $changes change(s) detected. Report: $REPORT"
        cat "$REPORT"
    fi
}

case "${2:---compare}" in
    --baseline) create_baseline ;;
    --compare)  compare_to_baseline ;;
    *) echo "Usage: $0 [directory] [--baseline|--compare]" ;;
esac
```

#### 🎧 Audiobook
> *"The capstone for the filesystem book is a file integrity monitor. It takes a SHA256 hash snapshot of every file in a directory, then lets you compare against it later to detect any changes, additions, or deletions. This is the same technique used by professional security tools. It uses find, xargs, sha256sum, sort, and comm — every core tool from this book."*

#### 🎬 Video
1. (0:00) Why file integrity monitoring matters
2. (2:00) Write baseline creation (find | sort | sha256sum)
3. (5:00) Write comparison logic (comm -13 / -23 / -12)
4. (9:00) Test: create baseline, modify a file, run compare
5. (11:00) Report shown, changes detected
6. (12:00) Credential claim



## Further Reading

- 📄 [`docs/B-002-commands-that-actually-work.md`](B-002-commands-that-actually-work.md) — Commands used throughout this book
- 📄 [`docs/linux-blockchain-educational-ecosystem.md`](linux-blockchain-educational-ecosystem.md) — Full Linux curriculum
- 📄 [`docs/P011-EBOOK-000-course-series-master-plan.md`](P011-EBOOK-000-course-series-master-plan.md) — All 300 books
- 🏠 [`README.md`](../README.md) — Encyclopedia home

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

---

> 🎓 **All 10 DFY lessons complete.** You can now map, navigate, protect, monitor, organize, and search your filesystem like a professional. Every script above is deployable today.
>
> **Next:** Claim your `CLL-L0-B003-FilesystemNavigator` credential, then continue to B-004.

---

## Further Reading

- 📄 [`docs/B-002-commands-that-actually-work.md`](B-002-commands-that-actually-work.md) — Commands used throughout this book
- 📄 [`docs/linux-blockchain-educational-ecosystem.md`](linux-blockchain-educational-ecosystem.md) — Full Linux curriculum
- 📄 [`docs/P011-EBOOK-000-course-series-master-plan.md`](P011-EBOOK-000-course-series-master-plan.md) — All 300 books
- 🏠 [`README.md`](../README.md) — Encyclopedia home

# B-021–B-025 HDVG Video Scene Manifests

### Phase 1 — Batch 5 — Linux Foundations Final Cluster

> *Scene manifests are the bridge between the written ebook and the ACVS production pipeline. Each manifest becomes an input to `ACVSScriptAgent`, which routes via Hermes and renders via HDVG.*

---

## B-021: The Linux Filesystem Explained
**Mode:** Tutorial | **Narrator:** lippytmai | **Credential:** `CLL-L1-B021-FilesystemEngineer`

```json
{
  "book_id": "B-021",
  "title": "The Linux Filesystem Explained",
  "mode": "Tutorial",
  "narrator": "lippytmai",
  "total_scenes": 7,
  "scenes": [
    {
      "id": "B021-S001",
      "title": "The FHS Contract",
      "narration": "The Linux Filesystem Hierarchy Standard is a contract between the kernel and every program on your system. Every directory has a purpose. Learn the contract, and you can navigate any Linux machine on Earth without ever having been there before.",
      "visual_prompt": "Animated directory tree expanding from / root. Each top-level dir appears with a glowing label as narrated.",
      "duration_sec": 50
    },
    {
      "id": "B021-S002",
      "title": "/etc — Where Config Lives",
      "narration": "If you want to know how any service is configured, start in /etc. The hostname of the machine? /etc/hostname. How drives mount? /etc/fstab. The SSH configuration? /etc/ssh/sshd_config. It's all here.",
      "visual_prompt": "Terminal showing ls /etc with key files highlighted one by one as mentioned.",
      "code_block": "ls /etc | head -30\ncat /etc/hostname\ncat /etc/os-release",
      "duration_sec": 65
    },
    {
      "id": "B021-S003",
      "title": "/var — Data That Changes",
      "narration": "/var is where everything variable lives. Log files accumulate in /var/log. Docker stores its images in /var/lib/docker. Your database writes to /var/lib/postgresql. Watch /var when disk space runs low.",
      "visual_prompt": "du command output showing /var/* sizes, /var/log directory expanding.",
      "code_block": "du -sh /var/*\nls /var/log/ | head -10",
      "duration_sec": 55
    },
    {
      "id": "B021-S004",
      "title": "/proc — The Kernel as Files",
      "narration": "/proc is not a real directory on disk. It's a virtual window into the kernel — a live view of every process, every CPU, all your memory. Reading /proc/cpuinfo reads the CPU in real time. This is Linux philosophy: everything is a file.",
      "visual_prompt": "cat /proc/cpuinfo output, animated CPU cores lighting up. then cat /proc/meminfo.",
      "code_block": "cat /proc/cpuinfo | grep 'model name'\ncat /proc/meminfo | grep MemTotal\ncat /proc/uptime",
      "duration_sec": 60
    },
    {
      "id": "B021-S005",
      "title": "Symlinks — The Filesystem's Shortcuts",
      "narration": "A symlink is a pointer to another file or directory. Modern Linux systems have /bin pointing to /usr/bin. You can create your own — like a shortcut from ~/workspace to ~/developer-workspace. ln -s source destination.",
      "visual_prompt": "ls -la /bin showing the symlink arrow → usr/bin. Then creating a symlink and navigating it.",
      "code_block": "ls -la /bin\nln -s ~/developer-workspace ~/workspace\nls -la ~ | grep workspace\nreadlink -f ~/workspace",
      "duration_sec": 55
    },
    {
      "id": "B021-S006",
      "title": "Build: filesystem-navigator.sh",
      "narration": "Now we build. Our artifact is filesystem-navigator.sh — it audits your entire system and produces a report of what lives in each key directory. One script. Any Linux machine. Every time.",
      "visual_prompt": "Code editor (nvim) with filesystem-navigator.sh being written. Then running it and seeing the output report.",
      "code_block": "chmod +x ~/scripts/filesystem-navigator.sh\n~/scripts/filesystem-navigator.sh",
      "duration_sec": 80
    },
    {
      "id": "B021-S007",
      "title": "Mission: Audit Your System",
      "narration": "Your mission: run the filesystem navigator on your machine and find out what's taking up the most space in /var. Report back. The engineer who knows their filesystem never gets surprised by a full disk.",
      "visual_prompt": "Mission brief card: 'Know Your Filesystem'",
      "interactive_overlay": {
        "type": "build_gate",
        "challenge": "Run ~/scripts/filesystem-navigator.sh and identify your largest /var directory",
        "credential_trigger": "CLL-L1-B021-FilesystemEngineer"
      },
      "duration_sec": 40
    }
  ]
}
```

---

## B-022: Shell Functions and Aliases
**Mode:** Tutorial | **Narrator:** lippytmai | **Credential:** `CLL-L1-B022-ShellCrafter`

```json
{
  "book_id": "B-022",
  "title": "Shell Functions and Aliases",
  "mode": "Tutorial",
  "narrator": "lippytmai",
  "total_scenes": 7,
  "scenes": [
    {
      "id": "B022-S001",
      "title": "Aliases — Shortcuts with Memory",
      "narration": "An alias is an abbreviation. alias ll='ls -la' means every time you type ll, the shell expands it to ls -la. This is not magic — it's deliberate engineering. Every senior developer has a personal alias library. Today you start yours.",
      "visual_prompt": "Terminal demonstrating alias creation and use — before and after comparison.",
      "code_block": "alias ll='ls -la --color=auto'\nalias gs='git status'\nalias ..='cd ..'\nll\ngs",
      "duration_sec": 55
    },
    {
      "id": "B022-S002",
      "title": "Making Aliases Permanent",
      "narration": "Aliases set in the terminal disappear when you close the session. To keep them forever, add them to ~/.bashrc or ~/.zshrc. Then run source ~/.bashrc to reload without restarting.",
      "visual_prompt": "nvim ~/.bashrc with alias section being added. Then source ~/.bashrc and verification.",
      "code_block": "echo \"alias ll='ls -la --color=auto'\" >> ~/.bashrc\nsource ~/.bashrc\nalias | grep ll",
      "duration_sec": 50
    },
    {
      "id": "B022-S003",
      "title": "Shell Functions — When Aliases Aren't Enough",
      "narration": "Aliases can't take arguments. Functions can. mkcd() creates a directory AND cd's into it. gacp() does git add, commit, and push in one command. Functions make your workflow feel like a superpower.",
      "visual_prompt": "Side by side: alias limitation (no args) vs function (args work). mkcd demo.",
      "code_block": "mkcd() { mkdir -p \"$1\" && cd \"$1\"; }\nmkcd test-dir\npwd",
      "duration_sec": 65
    },
    {
      "id": "B022-S004",
      "title": "The Developer Toolkit Functions",
      "narration": "Let's build the functions every developer needs. gacp for git. extract for any archive format. newproject for starting a project. serve for a quick HTTP server. These go into your function library.",
      "visual_prompt": "Code editor filling out dev-toolkit.sh with each function. Terminal demo of gacp and newproject.",
      "code_block": "gacp() { git add -A && git commit -m \"${1:-auto}\" && git push; }\nextract() { case \"$1\" in *.tar.gz) tar xzf \"$1\" ;; *.zip) unzip \"$1\" ;; esac; }\nserve() { python3 -m http.server \"${1:-8080}\"; }",
      "duration_sec": 70
    },
    {
      "id": "B022-S005",
      "title": "Structuring Your Function Library",
      "narration": "Don't put everything in .bashrc — it becomes unmaintainable. Instead: create ~/scripts/lib/dev-toolkit.sh and source it from .bashrc. One source line, modular toolkit. Easy to update, easy to share.",
      "visual_prompt": "Directory tree showing ~/scripts/lib/. nvim dev-toolkit.sh. echo 'source ...' >> ~/.bashrc.",
      "code_block": "mkdir -p ~/scripts/lib\n# ... write dev-toolkit.sh ...\necho 'source ~/scripts/lib/dev-toolkit.sh' >> ~/.bashrc\nsource ~/.bashrc",
      "duration_sec": 60
    },
    {
      "id": "B022-S006",
      "title": "Build: dev-toolkit.sh",
      "narration": "Now we build. Your artifact is ~/scripts/lib/dev-toolkit.sh — a complete modular shell library. Every function we've covered, organized, commented, and ready to source on any machine you set up.",
      "visual_prompt": "nvim showing the complete dev-toolkit.sh. source it. Run each function.",
      "code_block": "source ~/scripts/lib/dev-toolkit.sh\nmkcd /tmp/test-b022\nnewproject my-test-project",
      "duration_sec": 75
    },
    {
      "id": "B022-S007",
      "title": "Mission: Build Your Personal Toolkit",
      "narration": "Your mission: add at least 5 aliases and 3 functions of your own choosing to dev-toolkit.sh. Things that would save you time every day. This toolkit travels with you to every machine.",
      "visual_prompt": "Mission card: 'Build Your Toolkit'",
      "interactive_overlay": {
        "type": "build_gate",
        "challenge": "Create dev-toolkit.sh with 5+ aliases and 3+ functions sourced from .bashrc",
        "credential_trigger": "CLL-L1-B022-ShellCrafter"
      },
      "duration_sec": 40
    }
  ]
}
```

---

## B-023: Archives, Compression, and Backups
**Mode:** Tutorial | **Narrator:** lippytmai | **Credential:** `CLL-L1-B023-BackupEngineer`

```json
{
  "book_id": "B-023",
  "title": "Archives, Compression, and Backups",
  "mode": "Tutorial",
  "narrator": "lippytmai",
  "total_scenes": 8,
  "scenes": [
    {
      "id": "B023-S001",
      "title": "Archiving vs. Compression",
      "narration": "These are two different operations. Archiving combines multiple files into one. Compression reduces its size. tar archives. gzip compresses. tar.gz does both. Understanding the difference means you always know what flag to use.",
      "visual_prompt": "Animated diagram: files → tar → one archive file → gzip → smaller file.",
      "duration_sec": 45
    },
    {
      "id": "B023-S002",
      "title": "tar — The Universal Archiver",
      "narration": "tar is your main tool. c for create, x for extract, t for list, f for filename, z for gzip. tar -czf creates. tar -xzf extracts. tar -tzf lists. Four combinations. That's 80% of your archive work.",
      "visual_prompt": "Terminal showing create, extract, list commands. Archive appears, then extracted files appear.",
      "code_block": "tar -czf backup.tar.gz ~/scripts/\ntar -tzf backup.tar.gz\ntar -xzf backup.tar.gz -C /tmp/restore/",
      "duration_sec": 70
    },
    {
      "id": "B023-S003",
      "title": "gzip, bzip2, xz — Compression Tradeoffs",
      "narration": "Not all compression is equal. gzip is fastest but largest. xz is smallest but slowest. bzip2 is in between. zstd is the modern choice: fast AND small. Pick based on your constraint: time or space.",
      "visual_prompt": "Comparison table animating: speed vs compression ratio for gzip/bzip2/xz/zstd.",
      "code_block": "gzip -k largefile.sql\nbzip2 -k largefile.sql\nxz -k largefile.sql\nls -lh largefile.sql*",
      "duration_sec": 60
    },
    {
      "id": "B023-S004",
      "title": "rsync — Incremental Backups",
      "narration": "rsync is what makes backups efficient. The first backup transfers everything. Every subsequent backup transfers only what changed. -a for archive mode, --delete to mirror deletions. Dry run first with --dry-run.",
      "visual_prompt": "rsync first run (all files transfer, progress bar). Second run (only 2 changed files transfer, instant).",
      "code_block": "rsync -av ~/developer-workspace/ ~/backups/workspace/\nrsync -av --dry-run ~/developer-workspace/ ~/backups/workspace/",
      "duration_sec": 70
    },
    {
      "id": "B023-S005",
      "title": "The Retention Policy",
      "narration": "A backup system without retention fills your disk. The solution: keep snapshots for N days and delete older ones automatically. find with -mtime +30 finds files older than 30 days. Combined with -delete, that's your retention policy.",
      "visual_prompt": "find command filtering and deleting old snapshots. Disk space reclaimed.",
      "code_block": "find ~/backups/snapshots/ -name '*.tar.gz' -mtime +30 -delete\nls ~/backups/snapshots/ | wc -l",
      "duration_sec": 55
    },
    {
      "id": "B023-S006",
      "title": "Restoring from Backup",
      "narration": "A backup you've never tested is not a backup — it's a guess. List your snapshots. Pick one. Extract to /tmp. Compare with current. If it looks right, restore. Always test before you need it.",
      "visual_prompt": "ls snapshots. tar extract to /tmp/restore. diff showing they match.",
      "code_block": "ls ~/backups/snapshots/\ntar -xzf ~/backups/snapshots/workspace-LATEST.tar.gz -C /tmp/restore/\ndiff -r ~/developer-workspace/ /tmp/restore/latest/ | head",
      "duration_sec": 60
    },
    {
      "id": "B023-S007",
      "title": "Build: backup-system.sh",
      "narration": "Now we build the full backup system. rsync to latest/, snapshot to timestamped archive, clean up old snapshots, log everything. Schedule with cron at 2 AM every day. Your data is now protected.",
      "visual_prompt": "backup-system.sh running end to end. Crontab being edited.",
      "code_block": "chmod +x ~/scripts/backup-system.sh\n~/scripts/backup-system.sh\ncrontab -l | grep backup",
      "duration_sec": 80
    },
    {
      "id": "B023-S008",
      "title": "Mission: Back Up and Restore",
      "narration": "Your mission: run backup-system.sh, verify the snapshot exists, then restore a specific file from the snapshot to /tmp. Show proof that the restore worked. Engineers who can restore are engineers you can trust.",
      "visual_prompt": "Mission card: 'Backup and Restore'",
      "interactive_overlay": {
        "type": "build_gate",
        "challenge": "Create a backup snapshot and restore one file from it to /tmp",
        "credential_trigger": "CLL-L1-B023-BackupEngineer"
      },
      "duration_sec": 40
    }
  ]
}
```

---

## B-024: The User Who Could Do Anything
**Mode:** Tutorial | **Narrator:** lippytmai | **Credential:** `CLL-L1-B024-UserAdmin`

```json
{
  "book_id": "B-024",
  "title": "The User Who Could Do Anything",
  "mode": "Tutorial",
  "narrator": "lippytmai",
  "total_scenes": 7,
  "scenes": [
    {
      "id": "B024-S001",
      "title": "root — The User With No Limits",
      "narration": "root can delete the kernel. root has no undo. This is why you never live as root — you become root for exactly as long as you need to, and then you step back. The discipline of least privilege is what separates engineers from disasters.",
      "visual_prompt": "Animation: root user icon with all doors opening vs. regular user with selective doors. Danger animation when root runs rm -rf /.",
      "duration_sec": 55
    },
    {
      "id": "B024-S002",
      "title": "sudo — Controlled Elevation",
      "narration": "sudo runs one command as root. sudo -i drops you to a root shell — use it sparingly and always exit when done. sudo -l shows what you're allowed to do. sudo -u runs as another user. These four commands are 90% of your sudo work.",
      "visual_prompt": "Terminal: sudo apt update, sudo -l output, sudo -u postgres psql.",
      "code_block": "sudo apt update\nsudo -l\nwhoami\nsudo -i\nwhoami\nexit\nwhoami",
      "duration_sec": 65
    },
    {
      "id": "B024-S003",
      "title": "Creating and Managing Users",
      "narration": "useradd creates a user. usermod modifies one. userdel removes one. The -m flag creates a home directory. The -G flag assigns groups. The -s flag sets the shell. Three flags. That's enough to create any user you need.",
      "visual_prompt": "Terminal: useradd command with flags. /home directory appearing. getent passwd showing new user.",
      "code_block": "sudo useradd -m -s /bin/bash -G sudo developer1\nsudo passwd developer1\ngetent passwd developer1\nid developer1",
      "duration_sec": 70
    },
    {
      "id": "B024-S004",
      "title": "Groups — Shared Access Control",
      "narration": "Groups let multiple users share access to resources. Create a developers group. Add users to it. Set a shared directory with group ownership and 775 permissions. Everyone in the group can read and write. No one else can.",
      "visual_prompt": "groupadd → usermod -aG → mkdir shared → chown → chmod 775 → test access from both users.",
      "code_block": "sudo groupadd developers\nsudo usermod -aG developers charles\ngroups charles\nsudo mkdir /opt/shared\nsudo chown root:developers /opt/shared\nsudo chmod 775 /opt/shared",
      "duration_sec": 65
    },
    {
      "id": "B024-S005",
      "title": "sudoers — Fine-Grained Privilege",
      "narration": "Always edit sudoers with visudo — it validates before saving. You can give a user specific commands with NOPASSWD. You can give a group full sudo. You can create drop-in files in /etc/sudoers.d/. Never edit sudoers directly — visudo only.",
      "visual_prompt": "sudo visudo opening. Syntax explained line by line. sudoers.d drop-in file created.",
      "code_block": "sudo visudo -f /etc/sudoers.d/developers\n# Add: %developers ALL=(ALL:ALL) ALL\nsudo visudo -c",
      "duration_sec": 70
    },
    {
      "id": "B024-S006",
      "title": "Build: user-audit.sh",
      "narration": "Our build artifact: user-audit.sh. It reports every human account, every system service account, every group with members, and all sudo grants on the system. Run it on any machine and instantly understand its user model.",
      "visual_prompt": "user-audit.sh running. Clean formatted output showing users, groups, sudo. Perfect for new server onboarding.",
      "code_block": "chmod +x ~/scripts/user-audit.sh\nsudo ~/scripts/user-audit.sh",
      "duration_sec": 75
    },
    {
      "id": "B024-S007",
      "title": "Mission: Least Privilege Setup",
      "narration": "Your mission: create a service user that cannot log in interactively. Give it ownership of a specific directory. Give a developer group sudo access to restart nginx only. Show proof of the principle of least privilege in action.",
      "visual_prompt": "Mission card: 'Apply Least Privilege'",
      "interactive_overlay": {
        "type": "build_gate",
        "challenge": "Create a non-login service user and configure scoped sudo for a developer group",
        "credential_trigger": "CLL-L1-B024-UserAdmin"
      },
      "duration_sec": 40
    }
  ]
}
```

---

## B-025: Linux on Every Platform
**Mode:** Explainer + Tutorial | **Narrator:** lippytmai | **Credential:** `CLL-L1-B025-PlatformEngineer`

```json
{
  "book_id": "B-025",
  "title": "Linux on Every Platform",
  "mode": "Explainer",
  "narrator": "lippytmai",
  "total_scenes": 8,
  "scenes": [
    {
      "id": "B025-S001",
      "title": "One Skill, Four Surfaces",
      "narration": "Linux runs on a $35 Raspberry Pi, a $5 VPS, a Windows machine through WSL2, and the most powerful AWS server money can rent. The skills you've built in this series work on ALL of them. Today we prove it.",
      "visual_prompt": "Four screens simultaneously: Raspberry Pi, VPS terminal, WSL2 inside Windows, AWS console. Same commands running on all four.",
      "duration_sec": 55
    },
    {
      "id": "B025-S002",
      "title": "WSL2 — Linux Inside Windows",
      "narration": "WSL2 is a real Linux kernel running inside a Hyper-V VM on Windows. It's not emulation. It's not a container. It's Linux. Install Ubuntu in one PowerShell command: wsl --install. Then everything you've learned works immediately.",
      "visual_prompt": "Windows PowerShell: wsl --install. WSL2 Ubuntu opening. uname -r showing real Linux kernel. /home directory. /mnt/c showing Windows files.",
      "code_block": "# In PowerShell:\nwsl --install -d Ubuntu-24.04\n# Then in WSL2:\nuname -r\nwhoami\nls /mnt/c/Users/",
      "duration_sec": 70
    },
    {
      "id": "B025-S003",
      "title": "VPS — Your Server in the Cloud",
      "narration": "A VPS gives you root access to a Linux machine in a datacenter for $4 to $20 a month. Create a user. Set up SSH key auth. Enable the firewall. Disable root login. Four steps. Your VPS is now hardened and ready to run anything.",
      "visual_prompt": "DigitalOcean dashboard creating a Droplet. SSH connection. User creation. UFW enable. Security checklist completing.",
      "code_block": "ssh root@YOUR_VPS_IP\nadduser charles\nusermod -aG sudo charles\nufw allow OpenSSH && ufw enable",
      "duration_sec": 75
    },
    {
      "id": "B025-S004",
      "title": "Raspberry Pi — Linux at the Edge",
      "narration": "The Raspberry Pi runs Raspberry Pi OS — a Debian derivative. Everything you know from Debian and Ubuntu works here. It costs $35. It uses 3 watts. It runs 24/7 on your desk. SSH in from any machine on your network.",
      "visual_prompt": "Raspberry Pi hardware. Raspberry Pi Imager flashing SD card. SSH connecting. CPU temp. GPIO LED demo.",
      "code_block": "ssh charles@raspberrypi.local\nuname -a\nvcgencmd measure_temp\ncat /proc/device-tree/model",
      "duration_sec": 65
    },
    {
      "id": "B025-S005",
      "title": "Cloud VMs — Production Scale",
      "narration": "When you need more power, the cloud delivers it on demand. AWS EC2, DigitalOcean Droplets, Hetzner — all run the same Linux commands you've been learning. The difference is scale and pricing, not the shell.",
      "visual_prompt": "AWS console launching EC2. ssh -i key.pem ubuntu@IP. Same terminal. Same commands.",
      "code_block": "ssh -i my-key.pem ubuntu@EC2_PUBLIC_IP\nuname -r\ncat /etc/os-release\nsudo apt update",
      "duration_sec": 55
    },
    {
      "id": "B025-S006",
      "title": "Build: platform-bootstrap.sh",
      "narration": "Our final build artifact for Phase 1: platform-bootstrap.sh. One script. Any fresh Debian, Ubuntu, or Arch Linux install. It updates packages, installs your toolkit, creates your workspace, configures your shell, and enables the firewall. Run it on any new machine and be productive in 3 minutes.",
      "visual_prompt": "platform-bootstrap.sh running on a fresh VPS. Packages installing. Workspace creating. Shell configuring. ✅ checkmarks appearing.",
      "code_block": "chmod +x ~/scripts/platform-bootstrap.sh\n~/scripts/platform-bootstrap.sh\nsource ~/.bashrc\nls ~/developer-workspace/",
      "duration_sec": 85
    },
    {
      "id": "B025-S007",
      "title": "Phase 1 Complete — 25 Books",
      "narration": "You have completed Phase 1 of the lippytm.ai Linux Foundations curriculum. 25 books. 25 build artifacts. 25 credentials. You can navigate the filesystem, write scripts, manage processes, configure SSH, use Docker, schedule cron jobs, manage users, compress archives, and deploy on any platform. That's Linux mastery.",
      "visual_prompt": "Scrolling montage of all 25 book covers (B-001 through B-025). Credential badges appearing. Progress bar hitting 100%. Celebration animation.",
      "duration_sec": 90
    },
    {
      "id": "B025-S008",
      "title": "Mission: Deploy on 3 Platforms",
      "narration": "Your final Phase 1 mission: run platform-bootstrap.sh on at least 3 different Linux environments — WSL2, a VPS, and one of Raspberry Pi or a cloud VM. Screenshot each successful run. You are a platform engineer.",
      "visual_prompt": "Mission card: 'Platform Engineer — Phase 1 Graduate'",
      "interactive_overlay": {
        "type": "build_gate",
        "challenge": "Run platform-bootstrap.sh on 3 distinct Linux environments",
        "credential_trigger": "CLL-L1-B025-PlatformEngineer"
      },
      "duration_sec": 45
    }
  ]
}
```

---

## Video Production Summary — Batch 5

| Book | Scenes | Total Duration | Mode | Status |
|---|---|---|---|---|
| B-021 | 7 | ~6.5 min | Tutorial | ⏳ Awaiting G13 |
| B-022 | 7 | ~7 min | Tutorial | ⏳ Awaiting G13 |
| B-023 | 8 | ~8 min | Tutorial | ⏳ Awaiting G13 |
| B-024 | 7 | ~7 min | Tutorial | ⏳ Awaiting G13 |
| B-025 | 8 | ~9 min | Explainer+Tutorial | ⏳ Awaiting G13 |

---

## Further Reading

- 📄 [`docs/ai-copilot-video-sandbox-creator.md`](ai-copilot-video-sandbox-creator.md) — ACVS pipeline spec
- 📄 [`docs/P011-VIDEO-001-hd-video-generator.md`](P011-VIDEO-001-hd-video-generator.md) — HDVG system
- 📄 [`docs/creative-building-process.md`](creative-building-process.md) — Unified creative pipeline
- 🏠 [`README.md`](../README.md) — Encyclopedia home

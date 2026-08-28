# B-016–B-020 HDVG Scene Manifests

### HD Video Generator Scripts — Phase 1 Batch 4

**Batch:** Phase 1 · Batch 4
**Approved:** ✅ G13 — Charles Earl Lipshay — 2026-08-28
**Narration Voice:** `lippytmai` (ElevenLabs)
**Output Format:** MP4/WebM/HLS via FFmpeg composer
**Interactive Runtime:** GESN overlay engine

---

## B-016 — Pipes, Redirects, and Composition

```json
{
  "book_id": "B-016",
  "title": "Pipes, Redirects, and Composition",
  "credential": "CLL-L1-B016-PipelineBuilder",
  "total_duration_sec": 1020,
  "scenes": [
    {
      "id": "B016-S01",
      "title": "The Unix Philosophy",
      "narration": "In 1973, Douglas McIlroy had a simple idea: programs should do one thing well, and they should be able to talk to each other. He invented the pipe operator — a vertical bar — and changed computing forever. Every data pipeline, every ETL job, every log aggregation system traces its lineage directly to that one character.",
      "visual_prompt": "Timeline animation from 1973 Bell Labs to 2026 data pipelines. ASCII art pipe symbol transforms into modern pipeline diagrams.",
      "duration_sec": 75
    },
    {
      "id": "B016-S02",
      "title": "The Pipe Operator",
      "narration": "The pipe takes stdout from one command and sends it as stdin to the next. Simple. Composable. Powerful. ls output becomes grep input becomes wc input. Each tool does one thing. Together they do anything.",
      "visual_prompt": "Animated data flow: boxes labeled ls, grep, wc connected by pipe arrows. Data particles flowing left to right through each filter.",
      "code_block": "ls /etc | grep \"^s\" | wc -l\nps aux | grep python | grep -v grep\ncat /var/log/syslog | grep error | tail -20",
      "interactive_overlay": {
        "type": "quiz",
        "question": "What does the pipe operator | do?",
        "options": [
          "Redirects to a file",
          "Sends stdout of one command to stdin of the next",
          "Runs commands in parallel",
          "Separates commands on the same line"
        ],
        "correct": "Sends stdout of one command to stdin of the next",
        "explanation": "| connects commands: the output of the left command becomes the input of the right command."
      },
      "duration_sec": 150
    },
    {
      "id": "B016-S03",
      "title": "Redirects — Wiring the Streams",
      "narration": "Every process has three streams: stdin, stdout, stderr. Redirection rewires them. Greater-than writes stdout to a file. Double greater-than appends. 2-greater-than captures errors. Ampersand-greater-than captures both. Master these operators and you control all data flow in Linux.",
      "visual_prompt": "Diagram of three streams (0=stdin, 1=stdout, 2=stderr) with redirect operators shown as switches rewiring them to files or /dev/null.",
      "code_block": "python3 app.py > output.log 2>&1\necho \"$(date): done\" >> events.log\npython3 app.py 2> errors.log\npython3 app.py | tee run.log",
      "duration_sec": 150
    },
    {
      "id": "B016-S04",
      "title": "The Build — Log Analysis Pipeline",
      "narration": "You'll build a one-liner that reads an access log, extracts IP addresses, counts them, sorts by frequency, and shows the top 10 offenders. Every tool in the chain does exactly one thing. The pipeline does everything.",
      "visual_prompt": "Terminal building the pipeline step by step: cat | cut | sort | uniq -c | sort -rn | head. Each stage shows the data transformation.",
      "code_block": "cat access.log \\\n  | cut -d' ' -f1 \\\n  | sort \\\n  | uniq -c \\\n  | sort -rn \\\n  | head -10",
      "interactive_overlay": {
        "type": "build_gate",
        "challenge": "Run: echo -e 'a\\nb\\na\\nc\\na\\nb' | sort | uniq -c | sort -rn",
        "expected_output": "      3 a\n      2 b\n      1 c",
        "credential": "CLL-L1-B016-PipelineBuilder"
      },
      "duration_sec": 180
    },
    {
      "id": "B016-S05",
      "title": "Mission Complete",
      "narration": "Pipes. Redirects. Composition. You now think in data flow rather than individual commands. The pipeline is your superpower. The CLL-L1-B016-PipelineBuilder credential is yours.",
      "visual_prompt": "Credential card: CLL-L1-B016-PipelineBuilder minting on Base. Progress: 16/25 Linux foundations.",
      "interactive_overlay": {
        "type": "mission_complete",
        "credential_earned": "CLL-L1-B016-PipelineBuilder",
        "next_book": "B-017: The Arch Linux Advantage"
      },
      "duration_sec": 60
    }
  ]
}
```

---

## B-017 — The Arch Linux Advantage

```json
{
  "book_id": "B-017",
  "title": "The Arch Linux Advantage",
  "credential": "CLL-L1-B017-ArchOperator",
  "total_duration_sec": 1080,
  "scenes": [
    {
      "id": "B017-S01",
      "title": "Why Arch?",
      "narration": "Arch Linux is not easier than Ubuntu. It's better. Not because it's harder — but because it forces you to understand your system. Every service you run, you chose to run. Every package installed, you know why it's there. The OMARCHY standard is built on Arch because Arch developers are serious developers.",
      "visual_prompt": "Split comparison: Ubuntu auto-configuring 800 packages vs clean Arch install with only 50 packages — all chosen. Memory usage: 2.1GB vs 180MB at idle.",
      "duration_sec": 90
    },
    {
      "id": "B017-S02",
      "title": "pacman — The Package Manager",
      "narration": "pacman is the fastest, cleanest package manager in Linux. -S to install, -Syu to update everything, -Rs to remove cleanly with orphaned dependencies. The syntax is terse but consistent. After a week you'll never want to type apt-get again.",
      "visual_prompt": "Terminal: pacman -Syu running, showing package database sync then upgrade list. Then pacman -Ss 'text editor' showing results. Clean output, no noise.",
      "code_block": "sudo pacman -Syu\nsudo pacman -S neovim git docker\npacman -Ss \"text editor\"\npacman -Qe | wc -l  # count installed",
      "interactive_overlay": {
        "type": "quiz",
        "question": "What does 'pacman -Syu' do?",
        "options": [
          "Search for packages",
          "Synchronize and upgrade all packages",
          "Remove unused packages",
          "Show package info"
        ],
        "correct": "Synchronize and upgrade all packages",
        "explanation": "-S = sync, -y = refresh database, -u = upgrade all. Run this first before any install."
      },
      "duration_sec": 150
    },
    {
      "id": "B017-S03",
      "title": "The AUR — 90,000 Extra Packages",
      "narration": "The official Arch repos have 14,000 packages. The AUR adds 90,000 more. Any software that exists for Linux is probably in the AUR. yay gives you AUR access with the same pacman syntax. Always inspect a PKGBUILD before installing — it's a shell script that will run on your machine.",
      "visual_prompt": "Package count comparison: Ubuntu 60k, Debian 58k, Arch official 14k, Arch+AUR 104k. AUR submission flow animation.",
      "code_block": "yay -S google-chrome\nyay -S visual-studio-code-bin\nyay -Syu  # update official + AUR\nyay -G some-package  # inspect PKGBUILD first",
      "duration_sec": 150
    },
    {
      "id": "B017-S04",
      "title": "OMARCHY Bootstrap",
      "narration": "OMARCHY is the opinionated developer workstation standard for the ACSS ecosystem. It specifies the shell, terminal, editor, window manager, browser, and font — every choice made for performance and consistency. The bootstrap script installs everything in one run.",
      "visual_prompt": "OMARCHY stack table animating in: Zsh, Alacritty, Neovim, Hyprland, Brave, JetBrains Mono, Catppuccin. Then omarchy-bootstrap.sh running in a terminal.",
      "interactive_overlay": {
        "type": "build_gate",
        "challenge": "Run: pacman -Qe | grep -c '' to count your explicitly installed packages",
        "expected_output": "(any number — shows you chose every package)",
        "credential": "CLL-L1-B017-ArchOperator"
      },
      "duration_sec": 150
    },
    {
      "id": "B017-S05",
      "title": "Mission Complete",
      "narration": "Arch installed, pacman mastered, AUR unlocked, OMARCHY bootstrapped. You now run the same developer workstation as every lippytm.ai engineer. The CLL-L1-B017-ArchOperator credential is yours.",
      "visual_prompt": "Credential card: CLL-L1-B017-ArchOperator. Progress: 17/25.",
      "interactive_overlay": {
        "type": "mission_complete",
        "credential_earned": "CLL-L1-B017-ArchOperator",
        "next_book": "B-018: Log Files Tell the Truth"
      },
      "duration_sec": 60
    }
  ]
}
```

---

## B-018 — Log Files Tell the Truth

```json
{
  "book_id": "B-018",
  "title": "Log Files Tell the Truth",
  "credential": "CLL-L1-B018-LogAnalyst",
  "total_duration_sec": 1020,
  "scenes": [
    {
      "id": "B018-S01",
      "title": "The Black Box",
      "narration": "When a plane crashes, the first thing investigators retrieve is the black box. Logs are your system's black box. When a production service goes down at 3 AM, the logs are the only witness. The developer who can read them quickly is the developer who gets to go back to sleep quickly.",
      "visual_prompt": "Dark terminal at 3 AM. Service crash. Developer opens journalctl. Error found. Service restarted. Developer sleeps. Timestamp shows 4 minutes total.",
      "duration_sec": 75
    },
    {
      "id": "B018-S02",
      "title": "journalctl — The systemd Log Query Engine",
      "narration": "journalctl is the gateway to everything your systemd-based system has logged. Filter by service, by time, by priority, by boot. Follow live with -f. Get only errors with -p err. Combine filters to drill directly to the problem.",
      "visual_prompt": "journalctl command gallery: -u nginx, --since today, -p err, -b -1 (previous boot), -f live follow. Each shows real-looking output with timestamps.",
      "code_block": "journalctl -u nginx -p err --since today\njournalctl -b -1  # previous boot\njournalctl -f     # live follow\njournalctl --vacuum-size=500M",
      "interactive_overlay": {
        "type": "quiz",
        "question": "Which journalctl flag shows logs from the previous boot?",
        "options": ["-b 0", "-b -1", "--last-boot", "--previous"],
        "correct": "-b -1",
        "explanation": "-b 0 is current boot. -b -1 is one boot ago. -b -2 is two boots ago. Useful after crashes."
      },
      "duration_sec": 180
    },
    {
      "id": "B018-S03",
      "title": "logrotate — Prevent the Full Disk",
      "narration": "Log files grow forever. Without logrotate, /var/log fills your disk and everything stops. logrotate compresses old logs, deletes logs older than your retention policy, and runs every day via cron or systemd. One config file protects you forever.",
      "visual_prompt": "Disk space visualization: log directory growing over 90 days without logrotate (full). Same directory with logrotate: stable size, compressed archives.",
      "code_block": "/home/charles/logs/*.log {\n    daily\n    rotate 30\n    compress\n    missingok\n    notifempty\n    create 644 charles charles\n}",
      "duration_sec": 150
    },
    {
      "id": "B018-S04",
      "title": "Build Gate — Log Monitor",
      "narration": "Your log-monitor.sh scans all your service logs, counts errors, reports the top issues, and saves a daily summary. It runs via cron. You wake up every morning with yesterday's system story already written.",
      "visual_prompt": "log-monitor.sh running. Output shows each log file: OK with green checkmarks, then one log with 3 ERRORS highlighted in red. Summary file created.",
      "interactive_overlay": {
        "type": "build_gate",
        "challenge": "Run: journalctl -p err --since today --no-pager | wc -l",
        "expected_output": "(any number — confirms journalctl access)",
        "credential": "CLL-L1-B018-LogAnalyst"
      },
      "duration_sec": 120
    },
    {
      "id": "B018-S05",
      "title": "Mission Complete",
      "narration": "Logs located. journalctl mastered. logrotate configured. Daily summary running. You are no longer afraid of system failures — you have the evidence trail to fix them. The CLL-L1-B018-LogAnalyst credential is yours.",
      "visual_prompt": "Credential card: CLL-L1-B018-LogAnalyst. Progress: 18/25.",
      "interactive_overlay": {
        "type": "mission_complete",
        "credential_earned": "CLL-L1-B018-LogAnalyst",
        "next_book": "B-019: Securing Your Linux Machine"
      },
      "duration_sec": 60
    }
  ]
}
```

---

## B-019 — Securing Your Linux Machine

```json
{
  "book_id": "B-019",
  "title": "Securing Your Linux Machine",
  "credential": "CLL-L2-B019-ServerGuardian",
  "total_duration_sec": 1200,
  "scenes": [
    {
      "id": "B019-S01",
      "title": "47 Seconds",
      "narration": "A fresh Linux server connected to the internet receives its first automated SSH brute-force attempt within 47 seconds of launch. Not minutes. Not hours. 47 seconds. This is the reality of public infrastructure. This book teaches you to be ready before that timer runs out.",
      "visual_prompt": "Server launch animation. Timer starts: 0:00. At 0:47, first connection attempt appears in auth.log. 0:48, 0:49 — rapid fire attempts. Then: firewall enabled, fail2ban running — attempts blocked immediately.",
      "duration_sec": 90
    },
    {
      "id": "B019-S02",
      "title": "ufw — The Firewall That Makes Sense",
      "narration": "ufw wraps iptables in a human-readable interface. Two rules define your security posture: deny all incoming by default, allow outgoing. Then you open exactly the ports you need — SSH, HTTP, HTTPS — and nothing else. The internet cannot reach what it cannot see.",
      "visual_prompt": "ufw configuration: default deny incoming (red wall) → allow ssh, http, https (green doors in the wall). Network diagram shows blocked and allowed traffic.",
      "code_block": "sudo ufw default deny incoming\nsudo ufw default allow outgoing\nsudo ufw allow 2222/tcp  # SSH\nsudo ufw allow http\nsudo ufw allow https\nsudo ufw enable\nsudo ufw status verbose",
      "interactive_overlay": {
        "type": "quiz",
        "question": "What should you do BEFORE running 'sudo ufw enable'?",
        "options": [
          "Reboot the server",
          "Allow SSH so you don't lock yourself out",
          "Disable password authentication",
          "Install fail2ban"
        ],
        "correct": "Allow SSH so you don't lock yourself out",
        "explanation": "Always allow your SSH port before enabling ufw. Forgetting this locks you out of the server permanently."
      },
      "duration_sec": 180
    },
    {
      "id": "B019-S03",
      "title": "SSH Hardening — Disable the Weak Entry Points",
      "narration": "Three SSH settings eliminate the most common attack vectors: disable password authentication (keys only), disable root login, set MaxAuthTries to 3. Test your sshd_config with sshd -t before reloading. Always verify you can still connect in a new terminal before closing the old one.",
      "visual_prompt": "sshd_config file with dangerous defaults highlighted red. Then each hardened setting applied — lines turn green. sshd -t returns 'no errors'. Test connection succeeds.",
      "code_block": "# /etc/ssh/sshd_config\nPermitRootLogin no\nPasswordAuthentication no\nMaxAuthTries 3\nPort 2222\n\n# ALWAYS test first:\nsudo sshd -t\nsudo systemctl reload sshd",
      "duration_sec": 180
    },
    {
      "id": "B019-S04",
      "title": "fail2ban — The Automatic Bouncer",
      "narration": "fail2ban monitors your logs for failed authentication attempts. After 3 failures in 10 minutes, it bans the IP for 24 hours. Automatically. No manual intervention. An IP that tried to brute-force your SSH is gone before you even wake up to see the alert.",
      "visual_prompt": "fail2ban log animation: IP 203.0.113.42 fails 3 times in 8 minutes. fail2ban triggers ban. IP blocked in firewall. fail2ban-client status sshd shows banned IP.",
      "code_block": "[sshd]\nenabled = true\nport = 2222\nmaxretry = 3\nbantime = 86400  # 24 hours\n\n# Monitor:\nsudo fail2ban-client status sshd",
      "interactive_overlay": {
        "type": "build_gate",
        "challenge": "Run: sudo ufw status verbose | grep -E 'Status|Logging|Default'",
        "expected_output": "Status: active\nDefault: deny (incoming), allow (outgoing)",
        "credential": "CLL-L2-B019-ServerGuardian"
      },
      "duration_sec": 180
    },
    {
      "id": "B019-S05",
      "title": "Mission Complete — Level 2 Credential",
      "narration": "Firewall configured. SSH hardened. fail2ban active. Hardening script ready for any new server. Server security at this level is not advanced knowledge — it is the minimum standard. You have met the minimum. The CLL-L2-B019-ServerGuardian credential is yours — your first Level 2.",
      "visual_prompt": "Credential card with L2 badge: CLL-L2-B019-ServerGuardian. Gold border indicating Level 2. Progress: 19/25.",
      "interactive_overlay": {
        "type": "mission_complete",
        "credential_earned": "CLL-L2-B019-ServerGuardian",
        "level_milestone": "First Level 2 (L2) credential earned",
        "next_book": "B-020: Disk Space — The Resource That Runs Out"
      },
      "duration_sec": 90
    }
  ]
}
```

---

## B-020 — Disk Space: The Resource That Runs Out

```json
{
  "book_id": "B-020",
  "title": "Disk Space: The Resource That Runs Out",
  "credential": "CLL-L1-B020-DiskOperator",
  "total_duration_sec": 1020,
  "scenes": [
    {
      "id": "B020-S01",
      "title": "No Warning. Just Full.",
      "narration": "Unlike CPU or RAM, disk space has no graceful degradation. When it fills, everything stops simultaneously. Databases reject writes. Logging daemons crash. Container builds fail. The lesson every engineer learns once the hard way: monitor disk space proactively, not reactively.",
      "visual_prompt": "Production server: disk at 99%. Database throws error. Log daemon exits. Docker build fails. Three simultaneous crash notifications. Timestamp: 3:17 AM. Developer phone rings.",
      "duration_sec": 75
    },
    {
      "id": "B020-S02",
      "title": "df and du — Know What You Have",
      "narration": "df shows you how much space each filesystem has. du shows you what is consuming it. Used together — df to find the full filesystem, du to find the culprit directory — you can diagnose any disk space issue in under two minutes.",
      "visual_prompt": "df -h showing each filesystem. One at 94% highlighted. Then du -sh /* | sort -rh showing /var/log is the culprit. Drill down: du -sh /var/log/* | sort -rh.",
      "code_block": "df -h\ndu -sh ~/* | sort -rh | head -10\nfind /var/log -size +100M -exec ls -lh {} \\;",
      "interactive_overlay": {
        "type": "quiz",
        "question": "Which command shows which DIRECTORIES are consuming the most disk space?",
        "options": ["df -h", "lsblk -f", "du -sh * | sort -rh", "fdisk -l"],
        "correct": "du -sh * | sort -rh",
        "explanation": "du measures directory sizes. sort -rh sorts human-readable sizes largest first."
      },
      "duration_sec": 150
    },
    {
      "id": "B020-S03",
      "title": "The Common Space Hogs",
      "narration": "Four things fill your disk: Docker images and volumes, systemd journal logs, package cache, and application log files. Knowing how to clean each one is essential maintenance. Docker system prune. journalctl vacuum. pacman -Sc. logrotate. Four commands. Hundreds of gigabytes recovered.",
      "visual_prompt": "Pie chart: disk space breakdown — Docker 40%, logs 25%, package cache 20%, app data 15%. Then each cleanup command running and the slice shrinking.",
      "code_block": "docker system df\ndocker system prune -a\njournalctl --vacuum-size=500M\nsudo pacman -Sc\nsudo apt-get clean",
      "duration_sec": 150
    },
    {
      "id": "B020-S04",
      "title": "Build Gate — Disk Monitor Script",
      "narration": "Your disk-monitor.sh checks every filesystem, alerts when above 85% full, auto-cleans Docker dangling images, and saves a daily report. Add it to cron at 8 AM and you'll know every morning before the problem becomes a crisis.",
      "visual_prompt": "disk-monitor.sh running. Green checks for filesystems under threshold. One yellow warning at 80%. Docker cleanup triggered. Report file created. Crontab entry added.",
      "interactive_overlay": {
        "type": "build_gate",
        "challenge": "Run: df -h | awk 'NR>1 {gsub(\"%\",\"\",$5); if($5>0) print $5\"% \"$6}'",
        "expected_output": "(disk usage percentages per mount point)",
        "credential": "CLL-L1-B020-DiskOperator"
      },
      "duration_sec": 150
    },
    {
      "id": "B020-S05",
      "title": "Milestone — Linux Foundations Cluster 80% Complete",
      "narration": "Twenty books complete. You now operate Linux at a professional level: terminal, commands, permissions, scripting, environments, processes, networking, Git, text processing, services, secrets, containers, SSH, scheduling, editing, pipelines, package management, logging, security, and disk management. Five books remain in this cluster. The CLL-L1-B020-DiskOperator credential is yours.",
      "visual_prompt": "Progress wall showing all 20 credential cards B-001 through B-020. Progress bar: 20/25 Linux foundations (80%). B-021 'User Accounts and Groups' teaser card.",
      "interactive_overlay": {
        "type": "mission_complete",
        "credential_earned": "CLL-L1-B020-DiskOperator",
        "milestone": "20/25 Linux Foundations Complete (80%)",
        "next_book": "B-021: User Accounts and Groups"
      },
      "duration_sec": 90
    }
  ]
}
```

---

*Generated by HDVG Pipeline — lippytmai Narration Voice — GESN Interactive Overlay Engine*
*All 5 video scripts approved under QEP-B016-B020 G13 — Charles Earl Lipshay — 2026-08-28*

---

## Further Reading

- 📄 [`docs/P011-VIDEO-001-hd-video-generator.md`](P011-VIDEO-001-hd-video-generator.md) — HDVG pipeline architecture
- 📄 [`docs/QEP-B016-B020-phase1-batch4-quality-evidence-packet.md`](QEP-B016-B020-phase1-batch4-quality-evidence-packet.md) — Batch 4 QEP (✅ approved)
- 📄 [`docs/B-011-B015-VIDEO-scene-manifests.md`](B-011-B015-VIDEO-scene-manifests.md) — Batch 3 video scripts
- 🏠 [`README.md`](../README.md) — Encyclopedia home

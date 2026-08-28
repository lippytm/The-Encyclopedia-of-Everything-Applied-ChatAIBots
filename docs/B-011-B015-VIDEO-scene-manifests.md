# B-011–B-015 HDVG Scene Manifests

### HD Video Generator Scripts — Phase 1 Batch 3

**Batch:** Phase 1 · Batch 3
**Approved:** ✅ G13 — Charles Earl Lipshay — 2026-08-28
**Narration Voice:** `lippytmai` (ElevenLabs)
**Output Format:** MP4/WebM/HLS via FFmpeg composer
**Interactive Runtime:** GESN overlay engine

---

## B-011 — Environment Variables and Secrets

```json
{
  "book_id": "B-011",
  "title": "Environment Variables and Secrets",
  "credential": "CCSLL-L0-B011-SecretKeeper",
  "total_duration_sec": 1080,
  "scenes": [
    {
      "id": "B011-S01",
      "title": "The Most Expensive Mistake",
      "narration": "In 2022, a developer committed their AWS secret key to a public GitHub repo. Within 47 seconds — before they could delete it — automated bots had cloned the repo and started spinning up cloud servers. The bill: $47,000. Today you learn the pattern that prevents this forever.",
      "visual_prompt": "Text editor split screen: left shows a .env file with fake AWS keys, right shows git log with a red warning highlight on the commit that added it. Timer counting up from 0s to 47s.",
      "duration_sec": 90
    },
    {
      "id": "B011-S02",
      "title": "What Are Environment Variables?",
      "narration": "Environment variables are key-value pairs that live outside your code. Your program reads them at startup — so the same code can run in development with test credentials, and in production with real ones, without changing a single line.",
      "visual_prompt": "Terminal split: left runs 'printenv' showing PATH, HOME, USER. Right shows a Python script reading os.getenv('DATABASE_URL'). Arrows connecting the env vars to the Python call.",
      "code_block": "export DATABASE_URL=\"postgresql://localhost:5432/devdb\"\necho $DATABASE_URL\npython3 -c \"import os; print(os.getenv('DATABASE_URL'))\"",
      "duration_sec": 120
    },
    {
      "id": "B011-S03",
      "title": "The .env File Pattern",
      "narration": "The .env file is where you store your local secrets. One critical rule: it is NEVER committed to Git. You also create a .env.example — a template with placeholder values — which you DO commit. Anyone who clones your repo knows exactly what environment variables they need to set.",
      "visual_prompt": "Side by side: .env with real values (blurred) and .env.example with placeholder values. Then git status showing .env not tracked, .env.example staged.",
      "code_block": "# .env — NEVER commit\nDATABASE_URL=postgresql://localhost:5432/devdb\nSECRET_KEY=dev-secret-replace-me\n\n# .env.example — DO commit\nDATABASE_URL=postgresql://localhost:5432/yourdb\nSECRET_KEY=replace-with-random-secret",
      "interactive_overlay": {
        "type": "quiz",
        "question": "Which file should be committed to Git?",
        "options": [".env", ".env.example", "Both", "Neither"],
        "correct": ".env.example",
        "explanation": ".env contains real secrets — never committed. .env.example is a safe template."
      },
      "duration_sec": 150
    },
    {
      "id": "B011-S04",
      "title": "python-dotenv and the Config Class",
      "narration": "python-dotenv loads your .env file into os.environ automatically. Combined with a Config class, you get fail-fast startup — if a required variable is missing, your app crashes immediately with a clear error, rather than failing mysteriously at runtime.",
      "visual_prompt": "Terminal showing pip install python-dotenv, then running config.py. Output shows each config key with value summary — SECRET_KEY shows '***set***' not the real value.",
      "code_block": "from dotenv import load_dotenv\nimport os, sys\nload_dotenv()\n\nclass Config:\n    DATABASE_URL: str = os.environ[\"DATABASE_URL\"]\n    SECRET_KEY: str = os.environ[\"SECRET_KEY\"]\n    DEBUG: bool = os.getenv(\"DEBUG\",\"false\").lower() == \"true\"\n\n    @classmethod\n    def validate(cls):\n        missing = [k for k in [\"DATABASE_URL\",\"SECRET_KEY\"] if not os.getenv(k)]\n        if missing:\n            print(f\"FATAL: Missing: {missing}\")\n            sys.exit(1)",
      "duration_sec": 180
    },
    {
      "id": "B011-S05",
      "title": "Proof of Work + Credential Mint",
      "narration": "You've built a secure config loader, a .env file, a .env.example template, and updated .gitignore. Git status shows .env is invisible to version control. The pattern is in your muscle memory. The CCSLL-L0-B011-SecretKeeper credential is yours.",
      "visual_prompt": "Terminal running proof of work commands: git status, python3 src/config.py showing success output. Then credential mint animation on Base blockchain.",
      "interactive_overlay": {
        "type": "build_gate",
        "challenge": "Your .env file should NOT appear in git status. Run: git status | grep .env",
        "expected_output": "(empty — .env is gitignored)",
        "credential": "CCSLL-L0-B011-SecretKeeper"
      },
      "duration_sec": 120
    },
    {
      "id": "B011-S06",
      "title": "Mission Complete",
      "narration": "Secrets never in code. Environment variables for everything that changes between environments. The .env pattern is the foundation of every professional Python, Node, and Go project on the planet. You now speak the language.",
      "visual_prompt": "Credential card animation: CCSLL-L0-B011-SecretKeeper minting on Base. Text overlay: '15 ebooks complete — B-016 unlocked'.",
      "interactive_overlay": {
        "type": "mission_complete",
        "credential_earned": "CCSLL-L0-B011-SecretKeeper",
        "next_book": "B-012: The Container That Held Everything"
      },
      "duration_sec": 60
    }
  ]
}
```

---

## B-012 — The Container That Held Everything

```json
{
  "book_id": "B-012",
  "title": "The Container That Held Everything",
  "credential": "CSEL-L0-B012-ContainerPilot",
  "total_duration_sec": 1200,
  "scenes": [
    {
      "id": "B012-S01",
      "title": "It Works On My Machine",
      "narration": "Every developer has said it. 'But it works on my machine.' Docker eliminates this sentence from the software lexicon. A Docker container packs your code, its runtime, its dependencies, its OS libraries — everything it needs — into a single portable unit that runs identically anywhere.",
      "visual_prompt": "Split screen: Developer's MacBook running app successfully. Teammate's Ubuntu machine failing. Then Docker logo animates over both machines — app runs identically on both.",
      "duration_sec": 90
    },
    {
      "id": "B012-S02",
      "title": "Containers vs Virtual Machines",
      "narration": "Containers are not virtual machines. A VM emulates an entire computer — CPU, RAM, full OS. A container shares the host kernel and isolates only the process. Containers start in milliseconds, not minutes. They're megabytes, not gigabytes.",
      "visual_prompt": "Animated diagram: VM stack (Hardware → Hypervisor → Guest OS → App). Container stack (Hardware → Host OS → Container Runtime → App). Timer shows VM takes 2 minutes to start, container takes 0.3s.",
      "interactive_overlay": {
        "type": "quiz",
        "question": "A Docker container shares what with the host machine?",
        "options": ["CPU only", "The Linux kernel", "The entire OS", "Nothing"],
        "correct": "The Linux kernel",
        "explanation": "Containers share the host kernel — this is why they start fast and use less RAM than VMs."
      },
      "duration_sec": 120
    },
    {
      "id": "B012-S03",
      "title": "Essential Docker Commands",
      "narration": "Four commands get you 80% of your Docker work done: docker pull, docker run, docker ps, and docker logs. Pull downloads an image. Run creates and starts a container. PS lists what's running. Logs shows output.",
      "visual_prompt": "Terminal showing each command with annotated output. docker pull postgres:16-alpine showing layer downloads. docker run showing container ID. docker ps showing table of running containers.",
      "code_block": "docker pull postgres:16-alpine\ndocker run -d --name mydb \\\n  -e POSTGRES_PASSWORD=secret \\\n  -p 5432:5432 \\\n  postgres:16-alpine\ndocker ps\ndocker logs mydb",
      "duration_sec": 150
    },
    {
      "id": "B012-S04",
      "title": "Writing a Dockerfile",
      "narration": "A Dockerfile is a recipe for your image. FROM sets the base. COPY brings in your code. RUN installs dependencies. CMD defines what runs when the container starts. One important security rule: always create a non-root user and switch to it before CMD.",
      "visual_prompt": "Code editor showing Dockerfile with each instruction highlighted as narration describes it. Then: docker build command running, showing layer caching.",
      "code_block": "FROM python:3.12-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY src/ ./src/\nRUN useradd -m appuser && chown -R appuser:appuser /app\nUSER appuser\nCMD [\"python3\", \"src/app.py\"]",
      "duration_sec": 150
    },
    {
      "id": "B012-S05",
      "title": "Docker Compose — The Full Stack",
      "narration": "docker compose is where Docker gets powerful. One YAML file defines your entire application: your app container, your database, their network, their volumes, their health checks. One command — docker compose up — starts everything.",
      "visual_prompt": "docker-compose.yml file animating into two running containers (app + db) connected by a network. Terminal showing docker compose up -d then docker ps showing both services healthy.",
      "code_block": "docker compose up -d\ndocker compose logs -f db\ndocker exec -it project-alpha-db psql -U postgres devdb\ndocker compose down",
      "interactive_overlay": {
        "type": "build_gate",
        "challenge": "Run: docker compose up -d && docker ps | grep project-alpha",
        "expected_output": "Two containers running: project-alpha-app and project-alpha-db",
        "credential": "CSEL-L0-B012-ContainerPilot"
      },
      "duration_sec": 180
    },
    {
      "id": "B012-S06",
      "title": "Mission Complete",
      "narration": "Your application and database now run in isolated, reproducible containers. Anyone who clones your repo and runs docker compose up gets an identical environment. This is infrastructure as code. The CSEL-L0-B012-ContainerPilot credential is yours.",
      "visual_prompt": "Credential card: CSEL-L0-B012-ContainerPilot minting on Base. Progress bar: 12/25 Linux foundations complete.",
      "interactive_overlay": {
        "type": "mission_complete",
        "credential_earned": "CSEL-L0-B012-ContainerPilot",
        "next_book": "B-013: SSH — The Secure Handshake"
      },
      "duration_sec": 90
    }
  ]
}
```

---

## B-013 — SSH: The Secure Handshake

```json
{
  "book_id": "B-013",
  "title": "SSH: The Secure Handshake",
  "credential": "CLL-L1-B013-SSHMaster",
  "total_duration_sec": 1080,
  "scenes": [
    {
      "id": "B013-S01",
      "title": "The Key to the World's Infrastructure",
      "narration": "Every cloud server on Earth is accessed via SSH. Every blockchain node. Every CI/CD runner. SSH is not optional knowledge — it is the price of entry to professional system administration and cloud development.",
      "visual_prompt": "World map with glowing server nodes. Lines connecting a laptop to servers in AWS us-east-1, a VPS in Germany, a blockchain node in Singapore — all labeled 'SSH encrypted tunnel'.",
      "duration_sec": 60
    },
    {
      "id": "B013-S02",
      "title": "Key Pairs: The Cryptographic Handshake",
      "narration": "SSH key authentication works like a lock and key. You generate two mathematically linked keys: a private key that never leaves your machine, and a public key you give to every server. When you connect, the server challenges you to prove you hold the private key — without you ever sending it.",
      "visual_prompt": "Animation: key pair generation — private key stays on laptop (vault icon), public key travels to server (envelope icon). Connection attempt: server sends challenge, laptop signs it with private key, server verifies with public key. Tunnel opens.",
      "code_block": "ssh-keygen -t ed25519 -C \"charles@lippytm.ai\"\ncat ~/.ssh/id_ed25519.pub\nssh-copy-id charles@myserver.lippytm.ai",
      "interactive_overlay": {
        "type": "quiz",
        "question": "Which SSH key type is recommended in 2026?",
        "options": ["dsa", "rsa-1024", "ed25519", "ecdsa-256"],
        "correct": "ed25519",
        "explanation": "Ed25519 is modern, fast, and secure. DSA is broken. RSA needs 4096 bits minimum. Ed25519 is the OMARCHY standard."
      },
      "duration_sec": 150
    },
    {
      "id": "B013-S03",
      "title": "~/.ssh/config — Never Type a Long Command Again",
      "narration": "The SSH config file turns long ssh -i ~/.ssh/id_ed25519 -p 2222 charles@dev.lippytm.ai commands into ssh dev-server. One line. Define all your server aliases once, and connect with ease forever after.",
      "visual_prompt": "Terminal showing the before (long ssh command) then ~/.ssh/config being written, then after (ssh dev-server). Side-by-side comparison of command length.",
      "code_block": "# ~/.ssh/config\nHost dev-server\n    HostName dev.lippytm.ai\n    User charles\n    Port 22\n    IdentityFile ~/.ssh/id_ed25519\n\n# Connect with just:\nssh dev-server",
      "duration_sec": 150
    },
    {
      "id": "B013-S04",
      "title": "rsync — The Best Backup Tool You Already Have",
      "narration": "rsync transfers files over SSH, but only the parts that changed. A 10GB directory that changed by 50KB transfers 50KB. It's resumable, it preserves permissions, and it excludes .env and venv automatically — so you never accidentally send secrets to a remote server.",
      "visual_prompt": "rsync running: first run transfers 2.3GB in 45s. Second run (only 3 files changed) transfers 12KB in 0.2s. Progress bars side by side showing the dramatic difference.",
      "code_block": "rsync -avz --exclude='.env' --exclude='venv/' \\\n    -e \"ssh -i ~/.ssh/id_ed25519\" \\\n    ~/developer-workspace/ \\\n    charles@dev-server:/home/charles/developer-workspace/",
      "duration_sec": 150
    },
    {
      "id": "B013-S05",
      "title": "Build Gate + Credential",
      "narration": "You now have key-based authentication, an SSH config with server aliases, and an rsync script that backs up your workspace. Run the proof of work to earn your credential.",
      "visual_prompt": "Terminal showing DRY_RUN=1 ~/remote-backup.sh output. Files listed as would-be-transferred. Then credential mint animation.",
      "interactive_overlay": {
        "type": "build_gate",
        "challenge": "Run: ssh-add -l | grep ed25519",
        "expected_output": "256 SHA256:... charles@lippytm.ai (ED25519)",
        "credential": "CLL-L1-B013-SSHMaster"
      },
      "duration_sec": 120
    },
    {
      "id": "B013-S06",
      "title": "Mission Complete",
      "narration": "Key pairs generated. SSH config built. rsync script written. You can now access any server on the planet securely and transfer files efficiently. The CLL-L1-B013-SSHMaster credential is yours.",
      "visual_prompt": "Credential card: CLL-L1-B013-SSHMaster minting on Base. Progress: 13/25 Linux foundations.",
      "interactive_overlay": {
        "type": "mission_complete",
        "credential_earned": "CLL-L1-B013-SSHMaster",
        "next_book": "B-014: Cron — The Machine That Never Forgets"
      },
      "duration_sec": 60
    }
  ]
}
```

---

## B-014 — Cron: The Machine That Never Forgets

```json
{
  "book_id": "B-014",
  "title": "Cron: The Machine That Never Forgets",
  "credential": "CLL-L1-B014-CronOperator",
  "total_duration_sec": 1020,
  "scenes": [
    {
      "id": "B014-S01",
      "title": "The Daemon That Wakes Up Every Minute",
      "narration": "Cron is a daemon — a background process that has been running on Unix systems since the 1970s. Every 60 seconds it wakes up, checks its schedule, and runs whatever jobs are due. It never forgets. It never gets tired. And it will happily run your backup script at 3 AM while you sleep.",
      "visual_prompt": "Clock animation showing 60-second intervals. Each tick: crond wakes, scans crontab table, runs matching jobs. Minimal terminal: three green checkmarks for three scheduled jobs firing.",
      "duration_sec": 90
    },
    {
      "id": "B014-S02",
      "title": "Reading the Crontab Syntax",
      "narration": "Five fields. Minute, hour, day of month, month, day of week — then the command. An asterisk means 'every'. A slash means 'every N'. A range means 'from–to'. Once you internalize this pattern, you can read any crontab file instantly.",
      "visual_prompt": "Animated crontab syntax diagram: five labeled boxes with arrows. Each field lights up as narration describes it. Examples animate in: */5 = every 5 min, 0 3 = 3 AM, 0 9 * * 1 = Monday 9 AM.",
      "code_block": "# m  h  dom  mon  dow  command\n*/5  *   *    *    *   /scripts/health-check.sh\n  0  3   *    *    *   /scripts/db-backup.sh\n  0  9   *    *    1   /scripts/weekly-report.sh",
      "interactive_overlay": {
        "type": "quiz",
        "question": "What does '0 3 * * *' mean?",
        "options": [
          "Every 3 minutes",
          "At 3:00 AM every day",
          "Every day at midnight for 3 days",
          "At 3:00 PM on weekdays"
        ],
        "correct": "At 3:00 AM every day",
        "explanation": "0 = minute 0, 3 = hour 3 (3 AM), * * * = every day, every month, every weekday."
      },
      "duration_sec": 180
    },
    {
      "id": "B014-S03",
      "title": "Cron Environment Gotcha",
      "narration": "The most common cron bug: your script works perfectly when you run it manually, but silently fails in cron. The reason: cron runs in a stripped-down environment with a minimal PATH. Always use full paths to commands, or set PATH explicitly at the top of your crontab.",
      "visual_prompt": "Split terminal: manual run succeeds. Cron log shows 'command not found'. Then crontab with PATH=/usr/local/bin:/usr/bin:/bin added — cron log now shows success.",
      "code_block": "# BAD — cron's PATH doesn't include /usr/bin\n0 3 * * * python3 /home/charles/backup.py\n\n# GOOD — full path\n0 3 * * * /usr/bin/python3 /home/charles/backup.py\n\n# BEST — set PATH in crontab\nPATH=/usr/local/bin:/usr/bin:/bin\n0 3 * * * python3 /home/charles/backup.py",
      "duration_sec": 150
    },
    {
      "id": "B014-S04",
      "title": "The Three-Job Build",
      "narration": "You'll build three real cron jobs: a daily database backup at 3 AM, an hourly health check, and a weekly cleanup on Sunday. All with proper logging. All with absolute paths. All tested before being added to crontab.",
      "visual_prompt": "Terminal building each script. crontab -l showing all three entries. Then time-lapse: log files growing with hourly entries, then 3 AM backup entry appearing.",
      "code_block": "# View your crontab\ncrontab -l\n\n# Edit it\ncrontab -e\n\n# Verify cron is running\nsystemctl status cron\n\n# Watch your logs\ntail -f ~/logs/cron-health.log",
      "duration_sec": 150
    },
    {
      "id": "B014-S05",
      "title": "Mission Complete",
      "narration": "Three jobs scheduled, logging correctly, running automatically. Your machine now does things while you sleep. The CLL-L1-B014-CronOperator credential is yours.",
      "visual_prompt": "Credential card: CLL-L1-B014-CronOperator minting on Base. Progress: 14/25 Linux foundations.",
      "interactive_overlay": {
        "type": "mission_complete",
        "credential_earned": "CLL-L1-B014-CronOperator",
        "next_book": "B-015: The Editor That Does Everything"
      },
      "duration_sec": 60
    }
  ]
}
```

---

## B-015 — The Editor That Does Everything

```json
{
  "book_id": "B-015",
  "title": "The Editor That Does Everything",
  "credential": "CLL-L1-B015-NeovimOperator",
  "total_duration_sec": 1200,
  "scenes": [
    {
      "id": "B015-S01",
      "title": "Why 40% of Your Work Lives Here",
      "narration": "Developers spend 40 to 60 percent of their working hours inside a text editor. The tool you choose is not a preference — it's a productivity multiplier. Neovim is the OMARCHY standard because it runs on any machine, in any terminal, over SSH to any server, and with the right configuration it is faster than VS Code by every metric.",
      "visual_prompt": "Time-lapse montage: experienced Neovim user editing a Python file — cursor jumping precisely, multi-line deletions, search/replace, split windows. Same task in VS Code shown in slow motion. Side-by-side completion time.",
      "duration_sec": 90
    },
    {
      "id": "B015-S02",
      "title": "Modal Editing — The Mental Model",
      "narration": "Neovim has modes. Normal mode is for navigation and operations — this is your default state. Insert mode is for typing text. You enter it with 'i' and leave it with Escape. Visual mode is for selecting. The key insight: you are in Normal mode most of the time. You briefly enter Insert mode, type something, then return to Normal immediately.",
      "visual_prompt": "Mode diagram animation: Normal → i → Insert → Esc → Normal. Terminal showing mode indicator in statusline. Cursor shape changes: block in Normal, beam in Insert.",
      "interactive_overlay": {
        "type": "quiz",
        "question": "What is the DEFAULT mode when you open a file in Neovim?",
        "options": ["Insert", "Visual", "Normal", "Command"],
        "correct": "Normal",
        "explanation": "Normal mode is the default. Most time is spent here navigating and operating, not typing."
      },
      "duration_sec": 120
    },
    {
      "id": "B015-S03",
      "title": "Navigation Without Arrow Keys",
      "narration": "hjkl are your arrow keys. But you rarely move one character at a time. w jumps forward a word. b jumps back. 0 goes to line start, dollar goes to line end. gg is top of file, G is bottom. These motions combine with operators — dw deletes a word, cw changes a word, yw yanks a word.",
      "visual_prompt": "Terminal with annotated Neovim. Cursor movement demonstrated for each key: h/j/k/l, w/b, 0/$, gg/G. Then operator + motion combos: dw, cw, yy, dd.",
      "code_block": "h j k l     ← ↓ ↑ →\nw / b       word forward / back\n0 / $       line start / end\ngg / G      file start / end\ndw          delete word\ncw          change word\nyy          yank (copy) line\ndd          delete line\nu / Ctrl-r  undo / redo",
      "duration_sec": 180
    },
    {
      "id": "B015-S04",
      "title": "init.lua — Your Editor, Your Rules",
      "narration": "Neovim is configured in Lua. Your init.lua lives at ~/.config/nvim/init.lua. Three categories of settings matter first: options (line numbers, tab size, clipboard), key mappings (save with Ctrl-S, run Python with Space-r), and the leader key (Space is the OMARCHY standard).",
      "visual_prompt": "init.lua file animating in sections: vim.opt block highlighted, then vim.keymap.set blocks. Each setting shows its effect in a live Neovim window on the right.",
      "code_block": "vim.opt.number = true\nvim.opt.relativenumber = true\nvim.opt.tabstop = 4\nvim.g.mapleader = \" \"\n\nvim.keymap.set({\"n\",\"i\",\"v\"}, \"<C-s>\", \"<Cmd>w<CR>\")\nvim.keymap.set(\"i\", \"jk\", \"<Esc>\")\nvim.keymap.set(\"n\", \"<leader>r\", \":!python3 %<CR>\")",
      "duration_sec": 180
    },
    {
      "id": "B015-S05",
      "title": "Build Gate — Write and Run Without Leaving Neovim",
      "narration": "The build: open a Python file in Neovim, write a script, save it with Ctrl-S, run it with Space-r, see the output in the buffer. Never touch the mouse. Never leave the terminal. This is the complete flow.",
      "visual_prompt": "Screen recording of complete Neovim workflow: nvim hello.py → i → type script → jk → Ctrl-S → Space-r → output appears. Entire workflow in under 30 seconds.",
      "interactive_overlay": {
        "type": "build_gate",
        "challenge": "Open Neovim, write print('B-015 complete'), save, and run it with <leader>r",
        "expected_output": "B-015 complete",
        "credential": "CLL-L1-B015-NeovimOperator"
      },
      "duration_sec": 150
    },
    {
      "id": "B015-S06",
      "title": "Mission Complete — 15 Books Done",
      "narration": "You have now completed 15 books in the Linux and modern-stack foundations cluster. Terminal, commands, permissions, scripting, package management, processes, networking, Git, text tools, systemd, environment variables, Docker, SSH, cron, and Neovim. You are dangerous. The CLL-L1-B015-NeovimOperator credential is yours.",
      "visual_prompt": "Progress wall showing all 15 credential cards (B-001 through B-015) glowing in sequence. Counter: 15/300. Then B-016 'Python: Your First Real Program' teaser card fades in.",
      "interactive_overlay": {
        "type": "mission_complete",
        "credential_earned": "CLL-L1-B015-NeovimOperator",
        "milestone": "Linux Foundations Cluster Complete (B-001–B-015)",
        "next_book": "B-016: Python — Your First Real Program"
      },
      "duration_sec": 120
    }
  ]
}
```

---

*Generated by HDVG Pipeline — lippytmai Narration Voice — GESN Interactive Overlay Engine*
*All 5 video scripts approved under QEP-B011-B015 G13 — Charles Earl Lipshay — 2026-08-28*

---

## Further Reading

- 📄 [`docs/P011-VIDEO-001-hd-video-generator.md`](P011-VIDEO-001-hd-video-generator.md) — HDVG pipeline architecture
- 📄 [`docs/QEP-B011-B015-phase1-batch3-quality-evidence-packet.md`](QEP-B011-B015-phase1-batch3-quality-evidence-packet.md) — Batch 3 QEP (✅ approved)
- 📄 [`docs/B-006-B010-VIDEO-scene-manifests.md`](B-006-B010-VIDEO-scene-manifests.md) — Previous batch video scripts
- 🏠 [`README.md`](../README.md) — Encyclopedia home

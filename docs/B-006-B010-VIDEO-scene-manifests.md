# B-006 through B-010 — HDVG Video Scripts (Batch 2 Scene Manifests)

## Production Index | Approved under QEP-B006-B010 | Charles G13: 2026-08-28

This file contains the condensed scene manifests for B-006 through B-010.
Full-length scene manifests follow the same format as B-001–B-005 VIDEO docs.

---

## B-006-VIDEO: The Process That Wouldn't Stop (~18 min)

```json
{
  "content_id": "B-006-VIDEO", "ebook_id": "B-006",
  "title": "The Process That Wouldn't Stop",
  "narrator_voice": "lippytmai", "total_duration_estimate_min": 18,
  "credential": "CLL-L1-B006-ProcessWrangler", "gesn_mission": "GESN-B006",
  "intro": {
    "narration": "At any given moment, hundreds of programs are running on your Linux machine — web servers, shell processes, Python scripts, background daemons. The developer who can read that chaos, find the process consuming 100% CPU at 3am, and fix it before the server crashes — that developer gets the call. This video teaches you process management: how to see what's running, how to control it, and how to write a monitor that watches for you.",
    "visual_prompt": "Server dashboard visualization: CPU graph spikes red, process list scrolls rapidly. Developer's hands type 'top' — the spike is identified as a runaway Python process. kill -9 is run. CPU drops to green. Text: 'You found it. You fixed it. In 30 seconds.'",
    "duration_sec": 50
  },
  "scenes": [
    {
      "id": "S01", "title": "What Is a Process?",
      "narration": "A process is a running instance of a program. Every terminal you open, every script you run, every server you start — each is a process with a unique PID. Linux assigns PIDs sequentially from 1. PID 1 is systemd, the parent of all other processes. Every process has a parent. Kill the parent, and orphaned children are adopted by PID 1.",
      "visual_prompt": "Animated process tree. PID 1 (systemd) at root. Branches expand: bash, python3, your script. Highlight PID, PPID relationship with connecting lines.",
      "code_block": {"language": "bash", "code": "ps aux\nps auxf\nps -u $USER"},
      "interactive_overlay": {"type": "quiz", "question": "What does PID stand for?", "options": ["Process Instruction Directory", "Process ID", "Program Interface Descriptor", "Primary Input Device"], "correct": 1, "explanation": "PID = Process ID. Every running process on Linux has a unique integer PID assigned by the kernel at creation."},
      "duration_sec": 90
    },
    {
      "id": "S02", "title": "ps, top, htop",
      "narration": "ps gives you a snapshot — a photograph of processes at this moment. top gives you a live video. htop gives you a live video with color, mouse support, and easier controls. In production, you'll use all three. ps aux piped through grep to find a specific process. top to see the overall picture. htop when you have an interactive terminal and want to click and kill.",
      "visual_prompt": "Three side-by-side panels: ps aux output (static text), top (updating every 3s), htop (colorful, sorted by CPU). Arrow shows progression from basic to powerful.",
      "code_block": {"language": "bash", "code": "ps aux | grep python\ntop\nhtop\nps aux --sort=-%cpu | head -10"},
      "interactive_overlay": null,
      "duration_sec": 100
    },
    {
      "id": "S03", "title": "kill and Signals",
      "narration": "Signals are messages you send to processes. SIGTERM — signal 15 — is a polite request to shut down. The process can catch it and clean up. SIGKILL — signal 9 — is immediate termination. The kernel delivers it; the process has no say. Rule: always try SIGTERM first. Only use kill -9 when the process refuses to die.",
      "visual_prompt": "SIGTERM animation: envelope delivered to process, process 'reads' it, closes files, exits gracefully. SIGKILL animation: lightning bolt — process vanishes instantly, files potentially corrupted. Big text: 'SIGTERM first. SIGKILL last resort.'",
      "code_block": {"language": "bash", "code": "kill 1234\nkill -9 1234\npkill python3\nkillall node"},
      "interactive_overlay": {"type": "quiz", "question": "Which signal cannot be caught or ignored by a process?", "options": ["SIGTERM (15)", "SIGHUP (1)", "SIGKILL (9)", "SIGINT (2)"], "correct": 2, "explanation": "SIGKILL (9) is delivered directly by the kernel and cannot be caught, blocked, or ignored by the process. It is guaranteed to terminate the process immediately."},
      "duration_sec": 90
    },
    {
      "id": "S04", "title": "Background Jobs",
      "narration": "Append an ampersand to run any command in the background. jobs lists your background jobs. fg brings one forward. Ctrl-Z pauses a foreground job; bg sends it to the background. nohup lets a process survive after you close your terminal.",
      "visual_prompt": "Split terminal: left shows foreground command blocking. Right shows same command with & — prompt returns immediately, job number shown. fg and bg controls animate the job switching between states.",
      "code_block": {"language": "bash", "code": "python3 server.py &\njobs\nfg 1\nnohup python3 server.py > server.log 2>&1 &"},
      "interactive_overlay": null,
      "duration_sec": 80
    },
    {
      "id": "S05", "title": "Build — process-monitor.sh",
      "narration": "Build the process monitor script from the book. It checks for CPU-intensive processes, reads system load and memory from /proc, and logs everything. Run it with a low threshold so you see output immediately.",
      "visual_prompt": "Script building in terminal. Each function highlighted as it's added. Final run shows log output with CPU readings. Green status when all processes are below threshold, red alert when one exceeds it.",
      "code_block": {"language": "bash", "code": "chmod +x ~/process-monitor.sh\nCPU_THRESHOLD=10 ~/process-monitor.sh\ntail -f ~/developer-workspace/logs/process-monitor.log"},
      "interactive_overlay": {"type": "build_gate", "prompt": "Run process-monitor.sh with CPU_THRESHOLD=10. Verify the log file exists and contains at least one INFO entry. Mark complete to earn badge.", "xp_reward": 200, "unlocks_credential": "CLL-L1-B006-ProcessWrangler"},
      "duration_sec": 150
    },
    {
      "id": "S06", "title": "Outro",
      "narration": "In B-007 you'll use curl to make real API calls from the terminal — the same skill that lets you query blockchain nodes, GitHub APIs, and AI inference endpoints. See you there.",
      "visual_prompt": "GESN mission complete. Badge: CLL-L1-B006-ProcessWrangler. XP: +225. Skill tree: 'Process Management' node lights up. B-007 preview.",
      "interactive_overlay": {"type": "mission_complete", "badge": "CLL-L1-B006-ProcessWrangler", "xp_total": 225, "next_mission": "B-007-VIDEO"},
      "duration_sec": 40
    }
  ]
}
```

---

## B-007-VIDEO: The Network That Connected Everything (~20 min)

```json
{
  "content_id": "B-007-VIDEO", "ebook_id": "B-007",
  "title": "The Network That Connected Everything",
  "narrator_voice": "lippytmai", "total_duration_estimate_min": 20,
  "credential": "CLL-L1-B007-NetworkNavigator", "gesn_mission": "GESN-B007",
  "intro": {
    "narration": "Every blockchain node, every REST API, every AI inference server — they're all just computers waiting for other computers to talk to them. The language they speak is HTTP. The address they live at is an IP address and port. Once you understand that, you can talk to any of them from your terminal using curl. That's what this video teaches.",
    "visual_prompt": "Globe animation: data packets fly between continents. Zoom in on one packet: IP header visible, port number glowing, HTTP method labeled. Terminal appears: curl command runs, response returns. Text: 'You just spoke to a server on the other side of the world.'",
    "duration_sec": 45
  },
  "scenes": [
    {
      "id": "S01", "title": "IP, Ports, and Protocols",
      "narration": "An IP address is your computer's address on a network — like a street address. A port is the apartment number — which service to talk to. Port 22 is SSH. 80 is HTTP. 443 is HTTPS. 5432 is PostgreSQL. 8545 is an Ethereum node. When you type a URL, your computer resolves the domain name to an IP, then connects to port 443 for HTTPS.",
      "visual_prompt": "Building metaphor: IP address = building, port = apartment. Doors labeled with service names. Visitor (browser) arrives at IP, knocks on door 443. HTTPS opens the door. Other doors: SSH (22), Postgres (5432), Ethereum (8545).",
      "interactive_overlay": {"type": "quiz", "question": "What port does HTTPS use by default?", "options": ["80", "8080", "443", "22"], "correct": 2, "explanation": "HTTPS (HTTP Secure) uses port 443. HTTP uses port 80. Browsers default to 443 when you type https:// and 80 for http://. Many dev servers use 3000 or 8080 but those are conventions, not standards."},
      "duration_sec": 85
    },
    {
      "id": "S02", "title": "ping, traceroute, dig",
      "narration": "Three diagnostic tools. ping tells you if a host is reachable and how long packets take to get there. traceroute shows every router hop between you and the destination. dig resolves domain names to IP addresses — essential for debugging DNS problems.",
      "code_block": {"language": "bash", "code": "ping -c 4 google.com\ntraceroute google.com\ndig +short github.com\ndig github.com MX"},
      "interactive_overlay": null,
      "duration_sec": 80
    },
    {
      "id": "S03", "title": "curl — Every HTTP Request",
      "narration": "curl is the terminal's HTTP client. GET, POST, PUT, DELETE — curl does all of it. Add headers with -H. Send a body with -d. Follow redirects with -L. See headers with -i. See everything with -v. Once you're fluent with curl, you can test any API in the world without writing a single line of code.",
      "code_block": {"language": "bash", "code": "curl https://api.github.com/users/lippytm\ncurl -i https://api.github.com\ncurl -X POST -H 'Content-Type: application/json' -d '{\"key\":\"value\"}' https://httpbin.org/post\ncurl -H 'Authorization: ******' https://api.github.com/user"},
      "interactive_overlay": {"type": "quiz", "question": "What does curl -i do?", "options": ["Runs curl in interactive mode", "Includes the HTTP response headers in the output", "Sets the request method to INCLUDE", "Ignores SSL certificate errors"], "correct": 1, "explanation": "curl -i (or --include) outputs the HTTP response headers followed by the response body. This lets you see the status code, content-type, rate limit headers, etc. Essential for debugging API responses."},
      "duration_sec": 100
    },
    {
      "id": "S04", "title": "jq — JSON on the Terminal",
      "narration": "APIs return JSON. jq parses and queries JSON from the command line. Dot accesses fields. Brackets access array elements. Pipe chains operations. Map transforms arrays. Once you have curl plus jq, you have a complete API client in the terminal — no GUI, no Postman, no code needed.",
      "code_block": {"language": "bash", "code": "curl -s https://api.github.com/users/lippytm | jq .\ncurl -s https://api.github.com/users/lippytm | jq '.public_repos'\ncurl -s 'https://api.github.com/users/lippytm/repos' | jq '.[].name'"},
      "interactive_overlay": null,
      "duration_sec": 90
    },
    {
      "id": "S05", "title": "Build — api-client.sh",
      "narration": "Follow along building the GitHub API client script. It calls the API, extracts user info and top repos using jq, and logs everything. Run it against two different usernames to see the difference.",
      "code_block": {"language": "bash", "code": "chmod +x ~/api-client.sh\n~/api-client.sh lippytm\n~/api-client.sh torvalds"},
      "interactive_overlay": {"type": "build_gate", "prompt": "Run api-client.sh against any GitHub username. Verify the output shows name, repo count, and top repos. Mark complete to earn badge.", "xp_reward": 200, "unlocks_credential": "CLL-L1-B007-NetworkNavigator"},
      "duration_sec": 140
    },
    {
      "id": "S06", "title": "Outro",
      "narration": "You can now talk to any server on the internet from your terminal. In B-008 you'll learn Git — the version control system that uses these same network protocols to synchronize code between your machine and GitHub. See you there.",
      "interactive_overlay": {"type": "mission_complete", "badge": "CLL-L1-B007-NetworkNavigator", "xp_total": 250, "next_mission": "B-008-VIDEO"},
      "duration_sec": 40
    }
  ]
}
```

---

## B-008-VIDEO: Files That Never Get Lost (~25 min)

```json
{
  "content_id": "B-008-VIDEO", "ebook_id": "B-008",
  "title": "Files That Never Get Lost",
  "subtitle": "Git — Version Control from Zero to First Pull Request",
  "narrator_voice": "lippytmai", "total_duration_estimate_min": 25,
  "credential": "CCSLL-L0-B008-GitPilot", "gesn_mission": "GESN-B008",
  "intro": {
    "narration": "Git is a time machine for your code. Every commit is a snapshot. Every branch is an alternate timeline. Every merge is two timelines becoming one. Without Git, there is no professional software development. With Git, you can experiment freely, collaborate without conflict, and recover from any mistake in seconds. This video takes you from git init to your first pull request.",
    "visual_prompt": "Time-travel visualization: code history shown as a glowing timeline. Branches split off and rejoin. A mistake is made — viewer watches a 'git revert' restore the timeline. Text: 'Nothing is ever truly broken if you committed it.'",
    "duration_sec": 50
  },
  "scenes": [
    {
      "id": "S01", "title": "The Four Areas",
      "narration": "Git has four areas. Working directory: your actual files. Staging area: what you've marked for the next commit. Local repository: your complete history in .git/. Remote repository: a copy on GitHub. Data flows one direction: working directory → staging → local repo → remote. To get changes back, you pull from the remote.",
      "visual_prompt": "Four-stage pipeline animation. Files flow left to right: working dir → git add → staging → git commit → local repo → git push → remote (GitHub). Reverse arrow: git pull. Color coding: orange=unstaged, yellow=staged, green=committed, blue=remote.",
      "interactive_overlay": {"type": "quiz", "question": "What does 'git add .' do?", "options": ["Commits all files with a message '.'", "Stages ALL changed files in the current directory for the next commit", "Adds a new remote called '.'", "Initializes a new repository"], "correct": 1, "explanation": "git add . stages all modified and new files in the current directory (and subdirectories) for the next commit. It does NOT commit — staging is a separate step from committing."},
      "duration_sec": 90
    },
    {
      "id": "S02", "title": "init, add, commit, log",
      "narration": "Four commands for the core workflow. git init creates the .git/ folder — that's all a repository is. git add stages changes. git commit -m records a snapshot with a message. git log shows your history. The commit message matters — it's how you (and your team) understand what changed and why months from now.",
      "code_block": {"language": "bash", "code": "git init\ngit add README.md\ngit add .\ngit commit -m 'feat: initial developer workspace'\ngit log --oneline\ngit status"},
      "interactive_overlay": null,
      "duration_sec": 100
    },
    {
      "id": "S03", "title": "Branches",
      "narration": "A branch is a parallel version of your code. Main is the stable, deployable version. Feature branches are where you experiment. Create a branch, make changes, test them, then merge back to main. If the experiment fails, delete the branch — main is untouched. This is the single most important workflow in professional software development.",
      "code_block": {"language": "bash", "code": "git switch -c feature/add-logging\ngit add .\ngit commit -m 'feat: add structured logging'\ngit switch main\ngit merge feature/add-logging\ngit branch -d feature/add-logging"},
      "interactive_overlay": {"type": "quiz", "question": "Why do developers use branches instead of committing directly to main?", "options": ["Branches are required by GitHub", "To experiment safely without affecting the stable main codebase", "Branches are faster than main", "To avoid merge conflicts entirely"], "correct": 1, "explanation": "Branches let you work on features, fixes, or experiments in isolation. If the work is good, merge it. If not, delete the branch — main is unchanged. This is the foundation of safe collaborative development."},
      "duration_sec": 100
    },
    {
      "id": "S04", "title": "Push to GitHub + SSH Keys",
      "narration": "To push your commits to GitHub, you need to authenticate. The modern, secure way is SSH keys. You generate a key pair — private key stays on your machine, public key goes to GitHub. When you push, GitHub verifies your identity using the key pair. No passwords. No tokens. Just cryptography.",
      "code_block": {"language": "bash", "code": "ssh-keygen -t ed25519 -C 'charles@lippytm.ai'\ncat ~/.ssh/id_ed25519.pub\nssh -T git@github.com\ngit remote add origin git@github.com:USERNAME/REPO.git\ngit push -u origin main"},
      "interactive_overlay": null,
      "duration_sec": 100
    },
    {
      "id": "S05", "title": "Build — First GitHub Repository",
      "narration": "Follow along: initialize your developer-workspace as a Git repo, make commits for each project you've built in B-001 through B-007, add a .gitignore, and push to GitHub. This is your first real open source presence.",
      "code_block": {"language": "bash", "code": "cd ~/developer-workspace\ngit init\necho 'venv/\\n__pycache__/\\n*.log\\n.env\\n*.secret' > .gitignore\ngit add README.md .gitignore\ngit commit -m 'chore: initialize workspace'\ngit add project-alpha/ project-beta/ project-gamma/\ngit commit -m 'feat: add three project scaffolds'\ngit log --oneline"},
      "interactive_overlay": {"type": "build_gate", "prompt": "Initialize developer-workspace as a Git repo with at least 2 commits. Run 'git log --oneline' — both commits must be visible. Mark complete to earn badge.", "xp_reward": 250, "unlocks_credential": "CCSLL-L0-B008-GitPilot"},
      "duration_sec": 170
    },
    {
      "id": "S06", "title": "Outro",
      "narration": "You now have a Git repository on GitHub. Everything you build from here goes into version control — nothing is ever lost. In B-009 you'll learn text processing: grep, sed, awk, and cut — the tools for turning raw log files into useful data. See you there.",
      "interactive_overlay": {"type": "mission_complete", "badge": "CCSLL-L0-B008-GitPilot", "xp_total": 300, "next_mission": "B-009-VIDEO"},
      "duration_sec": 40
    }
  ]
}
```

---

## B-009-VIDEO: Working with Text Like a Pro (~20 min)

```json
{
  "content_id": "B-009-VIDEO", "ebook_id": "B-009",
  "title": "Working with Text Like a Pro",
  "subtitle": "grep, sed, awk, cut — The Terminal Text Processing Toolkit",
  "narrator_voice": "lippytmai", "total_duration_estimate_min": 20,
  "credential": "CLL-L1-B009-TextMaster", "gesn_mission": "GESN-B009",
  "intro": {
    "narration": "All data is text. Log files, API responses, CSVs, config files, source code — at the deepest level it's all characters in a stream. Four tools — grep, sed, awk, and cut — are your scalpels for that stream. They can find a specific error in a 10-million-line log file in under a second, transform a CSV into a JSON in three commands, and extract exactly the data you need from any text source.",
    "visual_prompt": "Data stream visualization: raw log file text flows as a river. grep acts as a filter — only matching lines pass through. sed acts as a transformer — text mutates as it flows. awk acts as a columnar processor — data splits into organized columns. Final output: clean structured data.",
    "duration_sec": 45
  },
  "scenes": [
    {
      "id": "S01", "title": "grep — Find the Lines",
      "narration": "grep takes a pattern and a file — or a pipe — and prints every line that matches. With -r it searches recursively. With -i it ignores case. With -n it shows line numbers. With -E it accepts extended regex patterns. And -o shows only the matching text, not the whole line.",
      "code_block": {"language": "bash", "code": "grep 'ERROR' app.log\ngrep -rn 'TODO' ./src/\ngrep -E 'error|warning|critical' app.log\ngrep -c '404' access.log\ngrep -o 'PID:[0-9]*' app.log"},
      "interactive_overlay": {"type": "quiz", "question": "What does grep -v do?", "options": ["Verbose mode — show all lines", "Invert match — show lines that do NOT match", "Version information", "Validate the regex pattern"], "correct": 1, "explanation": "grep -v (invert) shows lines that do NOT contain the pattern. Useful for filtering out noise: grep -v DEBUG app.log shows everything except DEBUG lines."},
      "duration_sec": 90
    },
    {
      "id": "S02", "title": "sed — Transform the Stream",
      "narration": "sed is a stream editor. Its most common use is substitution: s-slash-old-slash-new-slash-g to replace all occurrences globally. With -i it edits files in place — always make a backup first with -i.bak. You can also delete lines with d and print specific lines with p.",
      "code_block": {"language": "bash", "code": "sed 's/error/ERROR/g' app.log\nsed -i.bak 's/localhost/0.0.0.0/g' config.json\nsed '/^#/d' config.txt\nsed '/^$/d' config.txt"},
      "interactive_overlay": null,
      "duration_sec": 85
    },
    {
      "id": "S03", "title": "awk — Columns and Arithmetic",
      "narration": "awk treats each line as fields separated by whitespace. Dollar-1 is field 1, dollar-2 is field 2. Dollar-NF is the last field. You can use -F to change the delimiter. awk can do arithmetic — sum a column, average values, count occurrences. It's essentially a small programming language embedded in your terminal.",
      "code_block": {"language": "bash", "code": "awk '{print $1}' data.txt\nawk -F: '{print $1}' /etc/passwd\nawk '{sum += $5} END {print sum}' data.txt\nawk '$3 > 100 {print NR, $0}' data.txt\nawk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10"},
      "interactive_overlay": {"type": "quiz", "question": "In awk, what does $NF refer to?", "options": ["The number of fields on the current line", "The last field on the current line", "The first field on the current line", "The null field (empty fields)"], "correct": 1, "explanation": "NF is awk's built-in variable for the Number of Fields on the current line. $NF means 'the field at position NF' — which is always the last field. Useful when lines have variable numbers of columns."},
      "duration_sec": 95
    },
    {
      "id": "S04", "title": "Build — log-parser.sh",
      "narration": "Build the log parser: create the sample access log, then run the parser script that uses grep, awk, and sort to produce a summary report. Requests by status code, top IPs, top endpoints, error list.",
      "code_block": {"language": "bash", "code": "chmod +x ~/log-parser.sh\n~/log-parser.sh ~/developer-workspace/logs/sample-access.log\ncat ~/developer-workspace/logs/log-report.txt"},
      "interactive_overlay": {"type": "build_gate", "prompt": "Run log-parser.sh and verify the report shows request summary, top IPs, and top paths. Mark complete to earn badge.", "xp_reward": 200, "unlocks_credential": "CLL-L1-B009-TextMaster"},
      "duration_sec": 140
    },
    {
      "id": "S05", "title": "Outro",
      "narration": "In B-010 you'll learn systemd — how to make any script run as an always-on Linux service. That's the final Linux foundation book before we move to environment variables, Docker, SSH, and the full modern development stack.",
      "interactive_overlay": {"type": "mission_complete", "badge": "CLL-L1-B009-TextMaster", "xp_total": 225, "next_mission": "B-010-VIDEO"},
      "duration_sec": 35
    }
  ]
}
```

---

## B-010-VIDEO: The Service That Started Itself (~22 min)

```json
{
  "content_id": "B-010-VIDEO", "ebook_id": "B-010",
  "title": "The Service That Started Itself",
  "subtitle": "systemd — Linux Service Management, Autostart, and Boot",
  "narrator_voice": "lippytmai", "total_duration_estimate_min": 22,
  "credential": "CLL-L1-B010-SystemdOperator", "gesn_mission": "GESN-B010",
  "intro": {
    "narration": "Every production application — your web server, your database, your blockchain node, your AI inference server — runs as a systemd service. That means it starts automatically when the machine boots, restarts automatically if it crashes, and writes all its output to a searchable journal. In this video you'll go from 'what is systemd' to writing and deploying your own service unit file.",
    "visual_prompt": "Server boots: BIOS screen → Linux kernel loads → systemd PID 1 appears → services fan out like a startup sequence: network, PostgreSQL, nginx, your-app.service. Each service lights up green as it starts.",
    "duration_sec": 50
  },
  "scenes": [
    {
      "id": "S01", "title": "systemd and PID 1",
      "narration": "systemd is PID 1 — the first process the kernel starts. Everything else is its child or grandchild. systemd manages services using unit files: text config files that tell it what to run, when to run it, and what to do if it crashes. There are three unit types we care about: service (runs a program), timer (schedules a service), and socket (activates on incoming connections).",
      "interactive_overlay": {"type": "quiz", "question": "What process is always PID 1 on a modern Linux system?", "options": ["bash", "init", "systemd", "kernel"], "correct": 2, "explanation": "systemd is PID 1 on Ubuntu, Arch, Fedora, Debian, and most modern Linux distributions. It is the first userspace process started by the kernel and is the parent of all other processes."},
      "duration_sec": 80
    },
    {
      "id": "S02", "title": "systemctl — Control Interface",
      "narration": "systemctl is how you talk to systemd. Start, stop, restart, reload, enable, disable, status. The status command is the most useful: it shows whether a service is running, its last few log lines, and its PID. Enable makes a service start at boot. Disable removes that auto-start. Enable --now does both at once.",
      "code_block": {"language": "bash", "code": "sudo systemctl status nginx\nsudo systemctl start nginx\nsudo systemctl stop nginx\nsudo systemctl enable --now nginx\nsystemctl list-units --type=service --state=active\nsystemctl list-units --type=service --state=failed"},
      "interactive_overlay": null,
      "duration_sec": 90
    },
    {
      "id": "S03", "title": "journalctl — The System Journal",
      "narration": "systemd collects all service logs in a central binary journal. journalctl reads that journal. Follow a service's logs in real time with -u servicename -f. Filter by time with --since. Show only errors with -p err. This is how you debug a service that isn't behaving: journalctl -u servicename -n 50.",
      "code_block": {"language": "bash", "code": "journalctl -u backup.service\njournalctl -u backup.service -f\njournalctl --since '1 hour ago'\njournalctl -p err\njournalctl -b"},
      "interactive_overlay": {"type": "quiz", "question": "Which journalctl flag follows a service's logs in real time?", "options": ["-r (realtime)", "-f (follow)", "-t (tail)", "-w (watch)"], "correct": 1, "explanation": "journalctl -f follows the journal in real time, like 'tail -f' for a log file. Combined with -u: journalctl -u nginx -f shows only nginx logs as they arrive."},
      "duration_sec": 80
    },
    {
      "id": "S04", "title": "Writing a Service Unit File",
      "narration": "A service unit file has three sections. Unit: description and ordering (After= tells systemd what must start first). Service: what to run (ExecStart), what user to run it as, and how to handle crashes (Restart=on-failure). Install: which target activates this service at boot. Write it to /etc/systemd/system/, run daemon-reload, then start it.",
      "code_block": {"language": "ini", "code": "[Unit]\nDescription=Developer Workspace Backup\nAfter=local-fs.target\n\n[Service]\nType=oneshot\nUser=charles\nExecStart=/home/charles/backup.sh\n\n[Install]\nWantedBy=multi-user.target"},
      "interactive_overlay": null,
      "duration_sec": 100
    },
    {
      "id": "S05", "title": "Build — backup.service + backup.timer",
      "narration": "Follow along creating backup.service and backup.timer. The timer uses OnCalendar to run nightly at 2am. Persistent=true catches up on missed runs. After enabling the timer, systemctl list-timers shows it scheduled and ready.",
      "code_block": {"language": "bash", "code": "sudo systemctl daemon-reload\nsudo systemctl enable --now backup.timer\nsystemctl list-timers\njournalctl -u backup.service -n 5"},
      "interactive_overlay": {"type": "build_gate", "prompt": "Create backup.service and backup.timer. Run 'systemctl list-timers' — backup.timer must appear with a next-run time. Mark complete to earn badge.", "xp_reward": 225, "unlocks_credential": "CLL-L1-B010-SystemdOperator"},
      "duration_sec": 160
    },
    {
      "id": "S06", "title": "Outro — 10 Books Complete",
      "narration": "You've completed 10 books and 10 percent of the Beginner series. You have the complete Linux foundation: terminal, commands, permissions, scripting, Python environment, processes, networking, Git, text processing, and service management. In B-011, we start the modern developer stack: environment variables, secrets management, and the .env pattern. See you there.",
      "visual_prompt": "GESN mission complete. Badge: CLL-L1-B010. XP: +250. Series progress bar: 10/100 complete — milestone celebration animation. Skill tree shows first cluster fully lit: 'Linux Foundations'. B-011 preview.",
      "interactive_overlay": {"type": "mission_complete", "badge": "CLL-L1-B010-SystemdOperator", "xp_total": 250, "series_milestone": "10/100 Beginner — Linux Foundations Complete", "next_mission": "B-011-VIDEO"},
      "duration_sec": 50
    }
  ]
}
```

---

*All 5 video scripts approved under QEP-B006-B010. Charles G13: 2026-08-28.*
*Production: narration (lippytmai voice) + visuals (AI-generated) + interactive overlays → FFmpeg compose → MP4/WebM/HLS*

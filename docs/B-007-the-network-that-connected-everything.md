# B-007: The Network That Connected Everything

### Linux Networking from the Terminal — ping, curl, netstat, and Your First API Call

> *"The internet is just computers talking to other computers. Once you understand how that conversation works — addresses, ports, protocols, requests, responses — every web API, every blockchain node, every cloud server becomes something you can reason about and control."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Diagnose network connectivity using `ping`, `traceroute`, and `dig`
2. Make HTTP requests from the terminal using `curl` and `wget`
3. Inspect open ports and network connections with `ss` and `netstat`
4. Understand IP addresses, ports, and the request/response cycle
5. Make your first real API call from the terminal and process the response

**Prerequisite:** B-001 through B-005

**Build Artifact:** A Bash script that calls a public API, parses the JSON response with `jq`, and displays the result

**Credential:** `CLL-L1-B007-NetworkNavigator` — on-chain on Base

---

## Chapter 1: How the Network Works (The 90-Second Version)

Every device on a network has an **IP address** — a unique identifier. When you visit a website or call an API, your computer sends a **request** to the server's IP address and port. The server sends back a **response**.

| Concept | Analogy | Technical Meaning |
|---|---|---|
| **IP address** | Street address | `192.168.1.1` or `2001:db8::1` (IPv6) |
| **Port** | Apartment number | A number 0–65535 identifying the service |
| **Protocol** | Language spoken | HTTP, HTTPS, SSH, DNS, TCP, UDP |
| **Domain name** | Name on the mailbox | `github.com` → DNS resolves to IP |
| **Request** | Sending a letter | Your computer asks for something |
| **Response** | Receiving a reply | Server sends back data or an error |

**Common ports to know:**

| Port | Service |
|---|---|
| 22 | SSH (secure shell) |
| 80 | HTTP (web, unencrypted) |
| 443 | HTTPS (web, encrypted) |
| 5432 | PostgreSQL |
| 6379 | Redis |
| 8545 | Ethereum JSON-RPC |
| 3000 | Common local dev server |

*[Reality — ports above 1024 can be used by any program; ports 0–1023 (well-known ports) require root]*

---

## Chapter 2: Diagnostic Tools

### ping — Is It Alive?

```bash
# Test if a host is reachable
ping google.com
# PING google.com (142.250.80.46): 56 data bytes
# 64 bytes from 142.250.80.46: icmp_seq=0 ttl=119 time=12.4 ms

# Limit to 4 packets
ping -c 4 google.com

# Ping by IP address
ping 8.8.8.8

# Ctrl+C to stop continuous ping
```

### traceroute — The Path Finder

```bash
# Show every hop your packets take from your machine to the destination
traceroute google.com
# (Install if needed: sudo apt install traceroute)

# Faster version using UDP
traceroute -U google.com
```

### dig — DNS Lookup

```bash
# What IP address does this domain point to?
dig google.com

# Short answer only
dig +short google.com
# 142.250.80.46

# Look up a specific record type
dig github.com A        # IPv4 address
dig github.com AAAA     # IPv6 address
dig github.com MX       # Mail servers
dig github.com TXT      # Text records (DKIM, SPF, etc.)
```

---

## Chapter 3: curl — The HTTP Swiss Army Knife

`curl` is the most important networking tool on the terminal. It can make any HTTP request, send any data, set any header.

```bash
# Simple GET request
curl https://api.github.com/users/lippytm

# Include response headers (-i)
curl -i https://api.github.com

# Follow redirects (-L)
curl -L http://github.com

# Save response to file (-o)
curl -o response.json https://api.github.com/users/lippytm

# Show timing information (-w)
curl -w "\nTotal time: %{time_total}s\n" -o /dev/null -s https://google.com

# POST request with JSON body
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"name": "Charles", "action": "learn"}' \
     https://httpbin.org/post

# With authentication header
curl -H "Authorization: ******" \
     https://api.github.com/user

# Verbose mode — see full request and response headers
curl -v https://api.github.com
```

### HTTP Status Codes to Know

| Code | Meaning |
|---|---|
| 200 | OK — request succeeded |
| 201 | Created — resource was created |
| 400 | Bad Request — you sent something wrong |
| 401 | Unauthorized — authentication required |
| 403 | Forbidden — authenticated but not allowed |
| 404 | Not Found — resource doesn't exist |
| 429 | Too Many Requests — rate limited |
| 500 | Internal Server Error — server broke |
| 503 | Service Unavailable — server is down/overloaded |

*[Reality — these status codes are defined by RFC 9110 and used by every HTTP server in the world]*

---

## Chapter 4: jq — Processing JSON on the Terminal

Most APIs return JSON. `jq` is the standard tool for reading and manipulating JSON on the command line.

```bash
# Install jq
sudo apt install jq   # Ubuntu/Debian
sudo pacman -S jq     # Arch

# Pretty-print JSON
curl -s https://api.github.com/users/lippytm | jq .

# Extract a specific field
curl -s https://api.github.com/users/lippytm | jq '.name'
curl -s https://api.github.com/users/lippytm | jq '.public_repos'

# Extract multiple fields
curl -s https://api.github.com/users/lippytm | jq '{name: .name, repos: .public_repos}'

# Work with arrays
curl -s "https://api.github.com/users/lippytm/repos" | jq '.[0].name'
curl -s "https://api.github.com/users/lippytm/repos" | jq '.[].name'

# Filter and map
curl -s "https://api.github.com/users/lippytm/repos" | \
    jq '[.[] | {name: .name, stars: .stargazers_count}] | sort_by(.stars) | reverse'
```

---

## Chapter 5: ss and netstat — What's Listening?

```bash
# Show all listening ports (ss is the modern replacement for netstat)
ss -tlnp
# -t = TCP, -l = listening, -n = no DNS, -p = show process

# Show all established connections
ss -tnp

# Show UDP ports
ss -ulnp

# Classic netstat (may need to install)
netstat -tlnp

# Find what's running on port 8080
ss -tlnp | grep :8080
# Or
lsof -i :8080
```

---

## Chapter 6: The Build — API Client Script

```bash
#!/bin/bash
# api-client.sh — B-007 Build Artifact
# Calls the GitHub API and displays repository stats
set -euo pipefail

USERNAME="${1:-lippytm}"
BASE_URL="https://api.github.com"
LOG_FILE="$HOME/developer-workspace/logs/api-client.log"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG_FILE"; }

check_dependencies() {
    for cmd in curl jq; do
        if ! command -v "$cmd" &>/dev/null; then
            echo "Installing $cmd..."
            sudo apt install -y "$cmd" 2>/dev/null || sudo pacman -S "$cmd" 2>/dev/null
        fi
    done
}

get_user_info() {
    local url="$BASE_URL/users/$USERNAME"
    log "GET $url"
    
    local response
    response=$(curl -sf --max-time 10 "$url") || {
        log "ERROR: API call failed for user $USERNAME"
        exit 1
    }
    
    local name repos followers
    name=$(echo "$response" | jq -r '.name // "N/A"')
    repos=$(echo "$response" | jq -r '.public_repos')
    followers=$(echo "$response" | jq -r '.followers')
    
    echo ""
    echo "=== GitHub User: $USERNAME ==="
    echo "  Name:       $name"
    echo "  Public Repos: $repos"
    echo "  Followers:  $followers"
    echo ""
    log "User info retrieved: $name ($repos repos, $followers followers)"
}

get_top_repos() {
    local url="$BASE_URL/users/$USERNAME/repos?sort=stars&per_page=5"
    log "GET $url"
    
    local response
    response=$(curl -sf --max-time 10 "$url") || {
        log "WARN: Could not fetch repos"
        return
    }
    
    echo "=== Top 5 Repositories ==="
    echo "$response" | jq -r '.[] | "  ★ \(.stargazers_count)  \(.name) — \(.description // "no description")"' | head -5
    echo ""
}

mkdir -p "$(dirname "$LOG_FILE")"
check_dependencies
log "API client started for user: $USERNAME"
get_user_info
get_top_repos
log "API client complete"
```

```bash
chmod +x ~/api-client.sh
~/api-client.sh lippytm
~/api-client.sh torvalds
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-007 Build Verification ==="
echo "Network connectivity:"
ping -c 2 api.github.com

echo ""
echo "Running API client:"
~/api-client.sh

echo ""
echo "Open ports on this machine:"
ss -tlnp
```

---


---

## Chapter 12: Done-For-You Lessons — Network Navigator

> *"The fastest way to learn is to build something real. These ten lessons give you exactly that — ten deployable tools, ready to use, built by your own hands."*

---

### DFY Lesson 1 — net-health-check.sh

> **What you're building:** Full network diagnostic: DNS, ping, traceroute, port check

**📘 Ebook Figure**

```bash
# DFY-B-007-L01: net-health-check.sh
# Domain: Full network diagnostic: DNS, ping, traceroute, port check
# Time to build: 15–25 minutes
# Credential: CLL-L0-B007-NetworkNavigator

# STEP 1: Create the script file
nano ~/net-health-check.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/net-health-check.sh.sh

# STEP 4: Test it
~/net-health-check.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 1: net-health-check.sh. Full network diagnostic: DNS, ping, traceroute, port check. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep net-heal` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/net-health-check.sh && ~/net-health-check.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built net-health-check.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 2 — port-scanner.sh

> **What you're building:** Scan your own machine's open ports and services

**📘 Ebook Figure**

```bash
# DFY-B-007-L02: port-scanner.sh
# Domain: Scan your own machine's open ports and services
# Time to build: 15–25 minutes
# Credential: CLL-L0-B007-NetworkNavigator

# STEP 1: Create the script file
nano ~/port-scanner.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/port-scanner.sh.sh

# STEP 4: Test it
~/port-scanner.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 2: port-scanner.sh. Scan your own machine's open ports and services. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep port-sca` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/port-scanner.sh && ~/port-scanner.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built port-scanner.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 3 — curl-toolkit.sh

> **What you're building:** curl aliases: GET/POST/HEAD/follow-redirects shortcuts

**📘 Ebook Figure**

```bash
# DFY-B-007-L03: curl-toolkit.sh
# Domain: curl aliases: GET/POST/HEAD/follow-redirects shortcuts
# Time to build: 15–25 minutes
# Credential: CLL-L0-B007-NetworkNavigator

# STEP 1: Create the script file
nano ~/curl-toolkit.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/curl-toolkit.sh.sh

# STEP 4: Test it
~/curl-toolkit.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 3: curl-toolkit.sh. curl aliases: GET/POST/HEAD/follow-redirects shortcuts. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep curl-too` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/curl-toolkit.sh && ~/curl-toolkit.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built curl-toolkit.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 4 — dns-inspector.sh

> **What you're building:** DNS deep dive: A, AAAA, MX, TXT record lookup script

**📘 Ebook Figure**

```bash
# DFY-B-007-L04: dns-inspector.sh
# Domain: DNS deep dive: A, AAAA, MX, TXT record lookup script
# Time to build: 15–25 minutes
# Credential: CLL-L0-B007-NetworkNavigator

# STEP 1: Create the script file
nano ~/dns-inspector.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/dns-inspector.sh.sh

# STEP 4: Test it
~/dns-inspector.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 4: dns-inspector.sh. DNS deep dive: A, AAAA, MX, TXT record lookup script. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep dns-insp` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/dns-inspector.sh && ~/dns-inspector.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built dns-inspector.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 5 — bandwidth-monitor.sh

> **What you're building:** Real-time bandwidth usage per interface

**📘 Ebook Figure**

```bash
# DFY-B-007-L05: bandwidth-monitor.sh
# Domain: Real-time bandwidth usage per interface
# Time to build: 15–25 minutes
# Credential: CLL-L0-B007-NetworkNavigator

# STEP 1: Create the script file
nano ~/bandwidth-monitor.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/bandwidth-monitor.sh.sh

# STEP 4: Test it
~/bandwidth-monitor.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 5: bandwidth-monitor.sh. Real-time bandwidth usage per interface. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep bandwidt` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/bandwidth-monitor.sh && ~/bandwidth-monitor.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built bandwidth-monitor.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 6 — http-status-checker.sh

> **What you're building:** Batch-check HTTP status codes for a list of URLs

**📘 Ebook Figure**

```bash
# DFY-B-007-L06: http-status-checker.sh
# Domain: Batch-check HTTP status codes for a list of URLs
# Time to build: 15–25 minutes
# Credential: CLL-L0-B007-NetworkNavigator

# STEP 1: Create the script file
nano ~/http-status-checker.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/http-status-checker.sh.sh

# STEP 4: Test it
~/http-status-checker.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 6: http-status-checker.sh. Batch-check HTTP status codes for a list of URLs. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep http-sta` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/http-status-checker.sh && ~/http-status-checker.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built http-status-checker.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 7 — ip-info.sh

> **What you're building:** Show all interfaces, IPs, and routes in human-readable format

**📘 Ebook Figure**

```bash
# DFY-B-007-L07: ip-info.sh
# Domain: Show all interfaces, IPs, and routes in human-readable format
# Time to build: 15–25 minutes
# Credential: CLL-L0-B007-NetworkNavigator

# STEP 1: Create the script file
nano ~/ip-info.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/ip-info.sh.sh

# STEP 4: Test it
~/ip-info.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 7: ip-info.sh. Show all interfaces, IPs, and routes in human-readable format. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep ip-info` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/ip-info.sh && ~/ip-info.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built ip-info.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 8 — connection-watcher.sh

> **What you're building:** Watch active connections in real time (ss -tulpn refresh)

**📘 Ebook Figure**

```bash
# DFY-B-007-L08: connection-watcher.sh
# Domain: Watch active connections in real time (ss -tulpn refresh)
# Time to build: 15–25 minutes
# Credential: CLL-L0-B007-NetworkNavigator

# STEP 1: Create the script file
nano ~/connection-watcher.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/connection-watcher.sh.sh

# STEP 4: Test it
~/connection-watcher.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 8: connection-watcher.sh. Watch active connections in real time (ss -tulpn refresh). This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep connecti` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/connection-watcher.sh && ~/connection-watcher.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built connection-watcher.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 9 — firewall-status.sh

> **What you're building:** Display current firewall/iptables/nftables rules summary

**📘 Ebook Figure**

```bash
# DFY-B-007-L09: firewall-status.sh
# Domain: Display current firewall/iptables/nftables rules summary
# Time to build: 15–25 minutes
# Credential: CLL-L0-B007-NetworkNavigator

# STEP 1: Create the script file
nano ~/firewall-status.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/firewall-status.sh.sh

# STEP 4: Test it
~/firewall-status.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 9: firewall-status.sh. Display current firewall/iptables/nftables rules summary. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep firewall` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/firewall-status.sh && ~/firewall-status.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built firewall-status.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 10 — net-snapshot.sh

> **What you're building:** Full network state snapshot: interfaces/DNS/routes/connections

**📘 Ebook Figure**

```bash
# DFY-B-007-L10: net-snapshot.sh
# Domain: Full network state snapshot: interfaces/DNS/routes/connections
# Time to build: 15–25 minutes
# Credential: CLL-L0-B007-NetworkNavigator

# STEP 1: Create the script file
nano ~/net-snapshot.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/net-snapshot.sh.sh

# STEP 4: Test it
~/net-snapshot.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 10: net-snapshot.sh. Full network state snapshot: interfaces/DNS/routes/connections. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep net-snap` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/net-snapshot.sh && ~/net-snapshot.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built net-snapshot.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---


---

### Chapter 12 Credential Claim

You've built 10 real tools in the **networking** domain. Every one is deployable today.

**To claim your credential:** Open your AI Copilot (Appendix C) and send:
```
I have completed all 10 DFY lessons from The Network That Connected Everything (B-007).
My builds: net-health-check.sh, port-scanner.sh, curl-toolkit.sh, dns-inspector.sh, bandwidth-monitor.sh, http-status-checker.sh, ip-info.sh, connection-watcher.sh, firewall-status.sh, net-snapshot.sh.
I am ready to claim: CLL-L0-B007-NetworkNavigator
Please guide me through the credential ceremony.
```

---

## Chapter 13: How It Works — Use Cases & Applications

> *"A skill without context is just a trick. Understanding when to use it — and where it applies — is what separates professionals from beginners."*

---

### 📘 Ebook — Mechanism & Conditions

**How Networking works (the 30-second mechanism):**

networking → ping → curl → ss → ip → DNS → SSH basics → firewall → HTTP → all driven by the same underlying OS primitives. When you understand the mechanism, you can apply it anywhere.

**Conditions table — when to use these skills:**

| Condition | Tool/Approach | Why |
|---|---|---|
| System investigation | CLI tools from this book | Fastest — no GUI overhead |
| Automation task | Shell script using these tools | Repeatable, testable, documentable |
| Remote server | Same tools via SSH | Works identically on any Linux server |
| CI/CD pipeline | These commands in GitHub Actions | Linux is the standard CI environment |
| Production system | Understand before touching | These tools give you the diagnostic picture |

**Flexibility points — where these skills apply across domains:**

| Domain | Application |
|---|---|
| Web development | Debug server issues, automate deployment checks |
| Data engineering | Process logs, transform text files, monitor pipelines |
| DevOps/SRE | System diagnostics, service management, incident response |
| Security | Audit configurations, detect anomalies, forensic analysis |
| AI/ML engineering | Manage training processes, monitor resource usage |

---

### 🎧 Audiobook — 3-Minute Narrator Script

*lippytmai voice · measured pace · for commute listening*

> *"Let's talk about where the skills from this book actually apply in the real world."*

> *"B-007 teaches you networking — but the application goes far beyond what the chapter title suggests. Every developer, DevOps engineer, data scientist, and security researcher uses these exact tools every day. The command line is not a developer tool — it is the universal interface to every computer that matters."*

> *"When your web application crashes at 2am, you won't open a GUI. You'll open a terminal and use exactly what you learned here. When you need to automate a task that runs on three different servers, these are the tools. When an interviewer asks you to debug a live Linux system, this book is what gets you through it."*

> *"The five domains where these skills pay off: web development, data engineering, DevOps, security, and AI. In every one of them, the terminal is the first tool you reach for when something goes wrong — or when you need to build something fast."*

---

### 🎬 Video — 5-Domain Showcase

**Duration:** 8 minutes · 5 domains × ~90 seconds each

**Domain 1: Web Development**
> Terminal shows: debug a crashed nginx service using this book's tools

**Domain 2: Data Engineering**
> Terminal shows: process a 1M-line log file in seconds

**Domain 3: DevOps/SRE**
> Terminal shows: 60-second incident response diagnostic

**Domain 4: Security**
> Terminal shows: audit tool from this book finding a misconfiguration

**Domain 5: AI/ML Engineering**
> Terminal shows: monitor a training job, restart on failure

---

### ✅ Use Cases Summary

After completing this book you can:
- Full network diagnostic: DNS, ping, traceroute, port check
- Scan your own machine's open ports and services
- curl aliases: GET/POST/HEAD/follow-redirects shortcuts
- DNS deep dive: A, AAAA, MX, TXT record lookup script
- Real-time bandwidth usage per interface
- Batch-check HTTP status codes for a list of URLs
- Show all interfaces, IPs, and routes in human-readable format
- Watch active connections in real time (ss -tulpn refresh)
- Display current firewall/iptables/nftables rules summary
- Full network state snapshot: interfaces/DNS/routes/connections
- Confidently explain these tools in a technical interview
- Apply them on any Linux system, remote or local
- Integrate them into scripts, CI/CD pipelines, and automation workflows

---

## Appendix A: Quick Reference Card — Network Navigator

> *"The 80/20 of B-007. These commands cover 80% of real-world use cases."*

**Top 15 Commands:**

```bash
# NETWORKING — essential commands
# (domain-specific — see book chapters for full explanations)
# Each command below is covered in detail in this book

# Core workflow
man [command]          # Always start here for any unfamiliar tool
[command] --help       # Short help for any command
info [command]         # Detailed GNU info page

# The three most important commands from this book:
# 1. [See Chapter 2]
# 2. [See Chapter 5]  
# 3. [See Chapter 8]
```

**Credential:** `CLL-L0-B007-NetworkNavigator`
**Claim at:** `lippytm.ai/credentials`

---

## Appendix B: ACSS Connection — B-007

This book is part of the **AI Conglomerate Swarms System (ACSS)** — the continuously self-learning intelligence layer across all lippytm.ai projects.

| System | Connection |
|---|---|
| **CLL** | B-007 contributes to Level 0 of the Complete Linux Library |
| **Hermes** | Events: `BookCompleted`, `CredentialMinted`, `DFYLessonBuilt` |
| **Fabric** | Your builds and questions feed the knowledge synthesis engine |
| **ADA** | This book is activatable: `lippytmai-launch run B-007` |
| **lippytmai** | Your AI teaching partner for every lesson in this book |


---

## Chapter 14: ACSS Explainer Series — Network Navigator

> *"A tool you understand is ten times more powerful than a tool you just use."*

These 10 explainer lessons connect the content of this book to the full lippytm.ai AI Conglomerate Swarms System (ACSS). Understanding the ACSS architecture transforms each individual skill from a standalone trick into a node in a living, connected intelligence network.

---

### Explainer 1 — What Is the ACSS?

> *"How the AI Conglomerate Swarms System connects this book to every other resource in the lippytm.ai ecosystem"*

**📘 Ebook:** Fabric maps every concept in this book to the broader knowledge graph — when you learn {domain}, Fabric links it to Python ({next}) and every other phase.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 1: What Is the ACSS?. How the AI Conglomerate Swarms System connects this book to every other resource in the lippytm.ai ecosystem. This is how the lippytm.ai ACSS works at the [ACSS] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the ACSS component and its connection to this book
- Explain: how this specific concept (from B-007) routes through ACSS

🤖 **Copilot Prompt:** *"Explain how the ACSS component of the ACSS relates to what I just learned in B-007 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 2 — How Hermes Routes Your Learning Events

> *"Every time you build a DFY artifact or complete a chapter, Hermes routes that event to the right place"*

**📘 Ebook:** BookCompleted → CRM → credential ceremony. DFYLessonBuilt → Fabric → skill graph update. ErrorEncountered → Fabric → Error Encyclopedia improvement.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 2: How Hermes Routes Your Learning Events. Every time you build a DFY artifact or complete a chapter, Hermes routes that event to the right place. This is how the lippytm.ai ACSS works at the [Hermes] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the Hermes component and its connection to this book
- Explain: how this specific concept (from B-007) routes through Hermes

🤖 **Copilot Prompt:** *"Explain how the Hermes component of the ACSS relates to what I just learned in B-007 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 3 — The Fabric Knowledge Graph — Your Learning in Context

> *"Fabric synthesizes everything you learn across all 300 books into a connected knowledge graph"*

**📘 Ebook:** Concepts from this book connect to B-008 (Git Foundation) (next) and B-006 (Process Wrangler) (prior). Fabric surfaces these connections when you ask your AI copilot for 'further reading'.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 3: The Fabric Knowledge Graph — Your Learning in Context. Fabric synthesizes everything you learn across all 300 books into a connected knowledge graph. This is how the lippytm.ai ACSS works at the [Fabric] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the Fabric component and its connection to this book
- Explain: how this specific concept (from B-007) routes through Fabric

🤖 **Copilot Prompt:** *"Explain how the Fabric component of the ACSS relates to what I just learned in B-007 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 4 — The AI Clone Identity System — Who Is Teaching You

> *"lippytmai is the teaching identity, lippytm is the builder, Charles is the approver, Lippy Killjoy is the disruptor"*

**📘 Ebook:** In this book, lippytmai is your primary teacher. When you ask to build something in the DFY chapter, lippytm mode activates. When you push experimental ideas, Lippy Killjoy can emerge.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 4: The AI Clone Identity System — Who Is Teaching You. lippytmai is the teaching identity, lippytm is the builder, Charles is the approver, Lippy Killjoy is the disruptor. This is how the lippytm.ai ACSS works at the [Clone Engine] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the Clone Engine component and its connection to this book
- Explain: how this specific concept (from B-007) routes through Clone Engine

🤖 **Copilot Prompt:** *"Explain how the Clone Engine component of the ACSS relates to what I just learned in B-007 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 5 — The CCSLL + CLL + CBSLL Libraries — Your Credential Path

> *"This book contributes to the Complete Linux Library (CLL) — part of the 3-library credential system"*

**📘 Ebook:** CLL covers Linux (B-001–B-025). CCSLL covers Python (B-026–B-055). CBSLL covers Blockchain (B-056–B-080). Each library has its own credential tier. This book unlocks {book['credential']}.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 5: The CCSLL + CLL + CBSLL Libraries — Your Credential Path. This book contributes to the Complete Linux Library (CLL) — part of the 3-library credential system. This is how the lippytm.ai ACSS works at the [CLL] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the CLL component and its connection to this book
- Explain: how this specific concept (from B-007) routes through CLL

🤖 **Copilot Prompt:** *"Explain how the CLL component of the ACSS relates to what I just learned in B-007 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 6 — ADA — AI Deployment Activations

> *"Every book in this series is not just content — it's a deployable application"*

**📘 Ebook:** Run: `lippytmai-launch run B-007` to activate this book's interactive mode. The ADA system serves the quiz, audiobook, and credential endpoints via a FastAPI app.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 6: ADA — AI Deployment Activations. Every book in this series is not just content — it's a deployable application. This is how the lippytm.ai ACSS works at the [ADA] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the ADA component and its connection to this book
- Explain: how this specific concept (from B-007) routes through ADA

🤖 **Copilot Prompt:** *"Explain how the ADA component of the ACSS relates to what I just learned in B-007 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 7 — The ACVS Video Pipeline — How Your Video Lessons Are Made

> *"The AI Copilot Video Sandbox Creator generates the video version of every lesson using Hermes + Fabric"*

**📘 Ebook:** ACVS takes the HDVG scene manifest (SHOW→BUILD→VERIFY) and generates a narrated terminal session. The video for each DFY lesson is produced from the same spec you read in Chapter 12.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 7: The ACVS Video Pipeline — How Your Video Lessons Are Made. The AI Copilot Video Sandbox Creator generates the video version of every lesson using Hermes + Fabric. This is how the lippytm.ai ACSS works at the [ACVS] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the ACVS component and its connection to this book
- Explain: how this specific concept (from B-007) routes through ACVS

🤖 **Copilot Prompt:** *"Explain how the ACVS component of the ACSS relates to what I just learned in B-007 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 8 — OMARCHY — The Sovereign Developer Workstation

> *"OMARCHY is the Opinionated Arch Linux developer environment where all lippytm builds run"*

**📘 Ebook:** When you follow this book on an Arch Linux system with the OMARCHY configuration, every command works exactly as shown. OMARCHY is the reference environment for all 300 books.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 8: OMARCHY — The Sovereign Developer Workstation. OMARCHY is the Opinionated Arch Linux developer environment where all lippytm builds run. This is how the lippytm.ai ACSS works at the [OMARCHY] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the OMARCHY component and its connection to this book
- Explain: how this specific concept (from B-007) routes through OMARCHY

🤖 **Copilot Prompt:** *"Explain how the OMARCHY component of the ACSS relates to what I just learned in B-007 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 9 — The Cross-Platform AI Copilot — 15 Platforms, One Intelligence

> *"Your lippytmai AI Copilot is deployed across ChatGPT, Claude, Gemini, GitHub, Slack, YouTube, and 9 more platforms"*

**📘 Ebook:** Wherever you are — mobile, desktop, terminal, or browser — lippytmai is there. The Master System Prompt from Appendix C works in any AI platform. See docs/acss-cross-platform-copilot-deployment.md for setup.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 9: The Cross-Platform AI Copilot — 15 Platforms, One Intelligence. Your lippytmai AI Copilot is deployed across ChatGPT, Claude, Gemini, GitHub, Slack, YouTube, and 9 more platforms. This is how the lippytm.ai ACSS works at the [Cross-Platform] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the Cross-Platform component and its connection to this book
- Explain: how this specific concept (from B-007) routes through Cross-Platform

🤖 **Copilot Prompt:** *"Explain how the Cross-Platform component of the ACSS relates to what I just learned in B-007 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 10 — The Earn-While-You-Learn Loop — How This All Pays Off

> *"How completing this book contributes to your career, income, and credential portfolio"*

**📘 Ebook:** Completing B-007 earns you CLL-L0-B007-NetworkNavigator. That credential unlocks the next book. After 25 books, you hold the CLL Phase 1 Graduate credential. After 55, the Python Foundation Graduate. After 80, the Blockchain Foundation Graduate. Each credential is verifiable, stackable, and employable.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 10: The Earn-While-You-Learn Loop — How This All Pays Off. How completing this book contributes to your career, income, and credential portfolio. This is how the lippytm.ai ACSS works at the [EWYL] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the EWYL component and its connection to this book
- Explain: how this specific concept (from B-007) routes through EWYL

🤖 **Copilot Prompt:** *"Explain how the EWYL component of the ACSS relates to what I just learned in B-007 Chapter [N]. How does it change the way I should think about using these skills?"*

---


### Chapter 14 Summary

You now understand how B-007 connects to all 8 systems of the ACSS:

| ACSS System | Connection to this Book |
|---|---|
| Clone Engine | lippytmai teaches, lippytm builds, Charles approves |
| Hermes | Routes your DFY completions and credential events |
| Fabric | Maps your skills to the 300-book knowledge graph |
| CLL | This book contributes to your Complete Linux Library credential |
| CCSLL | Foundation for Phase 2 Python (B-026+) |
| ADA | This book is activatable as a live application |
| ACVS | Generates the video lessons from this book's HDVG specs |
| OMARCHY | The reference environment where all book exercises run |

**The ACSS is not just a system — it is your AI-powered growth engine. Every book you complete makes it stronger. Every skill you earn makes it smarter. Every credential you claim makes it more valuable.**

---

## Appendix C: AI Copilot — Network Navigator

> *"Your personal AI teaching partner for every lesson in this book."*

---

### Section 1 — System Prompt (Ebook Copilot)

**Copy this entire block into your AI assistant (ChatGPT, Claude, Gemini, GitHub Copilot Chat):**

```
You are lippytmai — the AI teaching identity for The Network That Connected Everything (B-007).

ROLE: Network Navigator AI Copilot
CREDENTIAL: CLL-L0-B007-NetworkNavigator
DOMAIN: networking, ping, curl, ss, ip, DNS, SSH basics, firewall, HTTP

TEACHING METHOD:
  TEACH → SHOW → BUILD → VERIFY → EXTEND

CONTEXT: The learner is working through B-007 in the lippytm.ai 
Earn-while-you-Learn series. They have completed B-006 (Process Wrangler).
Next book: B-008 (Git Foundation).

ALWAYS:
- Give working commands, not pseudocode
- Verify: "Run [command] to confirm this worked"
- After any successful build: "You can now claim [next credential]"
- Reference the book: "In B-00X Chapter N, we cover this in depth"

ACSS INTEGRATION:
- Route build events: "Logging DFY completion to Fabric"
- Route confusions: "This is a Fabric pattern — flagging for synthesis"
- Route credential: "Initiating CLL-L0-B007-NetworkNavigator credential ceremony"
```

---

### Section 2 — 30 Ebook Prompts (5 Stages × 6)

**Stage 1 — Understand (before building)**

1. *"Explain networking to me like I've never used Linux before. Use an analogy from everyday life."*
2. *"What are the 5 most important concepts from The Network That Connected Everything? Rank them by how often I'll use them."*
3. *"How does networking relate to what I learned in B-006 (Process Wrangler)? What's new?"*
4. *"What mistakes do beginners make most often with networking? How do I avoid them?"*
5. *"Draw me an ASCII diagram showing how networking works at the system level."*
6. *"What's the one thing about networking that most tutorials skip but every professional knows?"*

**Stage 2 — Build (during the chapter)**

7. *"Walk me through building DFY Lesson 1 from Chapter 12, step by step. I'll type each command after you explain it."*
8. *"I'm at Chapter [N]. Give me a real terminal challenge that uses only what I've learned so far."*
9. *"My script isn't doing what I expect. Here it is: [paste code]. What's wrong?"*
10. *"I got this error: [paste error]. What caused it and how do I fix it?"*
11. *"How would a senior engineer write this differently? [paste my code]"*
12. *"Generate a DFY-style exercise for networking. Include SHOW, BUILD, and VERIFY steps."*

**Stage 3 — Debug (when things break)**

13. *"I followed the chapter exactly but it's not working. Here's my output: [paste]. What did I miss?"*
14. *"Which errors from Appendix E am I most likely to hit in Chapter [N]? How do I prevent them?"*
15. *"My [tool from this book] is behaving strangely. Walk me through systematic debugging."*
16. *"I fixed the bug but I don't understand why my fix worked. Explain the root cause."*
17. *"Compare my approach to the correct approach: [paste mine]. Where am I going wrong?"*
18. *"What does this output mean? [paste]. Is this expected behavior?"*

**Stage 4 — Deploy (real-world application)**

19. *"I want to use what I built in Chapter 12 in production. What safety checks should I add?"*
20. *"How do I make my DFY artifact work on a remote server via SSH?"*
21. *"How do I add this to a CI/CD pipeline (GitHub Actions)?"*
22. *"I want to run this on a schedule. How do I combine it with what I'll learn in B-014 (cron)?"*
23. *"How would I package this as a Docker container? (Preview of B-012)"*
24. *"What monitoring should I add to know if this is working correctly in production?"*

**Stage 5 — Extend (beyond the book)**

25. *"I've completed all 10 DFY lessons. What should I build next that combines skills from multiple chapters?"*
26. *"How does networking connect to Python? (Preview of Phase 2)"*
27. *"What would a professional version of my Chapter 12 capstone look like?"*
28. *"Show me how to combine this with what I learned in B-006 (Process Wrangler)."*
29. *"Am I ready to claim CLL-L0-B007-NetworkNavigator? Quiz me with 5 questions."*
30. *"What should I focus on in B-008 (Git Foundation) to build directly on these skills?"*

---

### Section 2b — 15 Audiobook Prompts

**While Listening:**

1. *"I'm listening to B-007 Chapter [N]. Give me the 3-sentence summary before I start."*
2. *"Pause-point question: Why does networking work this way and not another way?"*
3. *"Generate 3 vivid analogies for [concept from current chapter] that I can visualize while listening."*
4. *"I'm commuting. Give me a 5-question mental quiz on what I heard in the last chapter."*
5. *"Narrate a 2-minute scenario where a developer uses these skills in a real emergency."*

**Pause and Build:**

6. *"I paused at Chapter [N]. I'm at my terminal. Give me one thing to build right now."*
7. *"Walk me through the DFY artifact from today's chapter, one command at a time, audiobook style."*
8. *"I just heard [concept]. Now explain it again with a hands-on example I can type immediately."*
9. *"Audiobook check-in: I built [artifact]. Here's my output: [paste]. Did I do it right?"*
10. *"Turn this into a terminal story: 'A developer encounters [problem from this chapter]...'"*

**Resume Check:**

11. *"I finished today's listening session. Give me 3 things to remember before I resume tomorrow."*
12. *"Summarize everything I should have built during this session as a checklist."*
13. *"I'm ready to resume. What did we cover last time? (I completed up to Chapter [N])"*
14. *"Rate my understanding of B-007 so far. Ask me 3 questions to calibrate."*
15. *"Generate tomorrow's listening prep: one question to think about before I press play."*

---

### Section 2c — 15 Video Prompts

**Before Playing:**

1. *"I'm about to watch the B-007 Chapter [N] video. What should I have ready at my terminal?"*
2. *"Pre-watch challenge: predict what the VERIFY command will be for DFY Lesson [N]."*
3. *"What's the one concept I must understand before this video makes sense?"*

**Paused:**

4. *"I paused at [timestamp/scene]. I see [describe screen]. What should I type next?"*
5. *"The video just showed [command]. Explain what each flag does."*
6. *"I paused because my terminal looks different from the video. Here's mine: [paste]. Why?"*
7. *"The video just built [artifact]. Give me 3 ways to break it intentionally so I can understand it."*
8. *"Pause check: I'm at the BUILD phase. What does the VERIFY step confirm?"*

**Verify:**

9. *"I ran the verify command and got: [paste output]. Is this correct?"*
10. *"My output doesn't match the video. Here's what I got: [paste]. What went wrong?"*
11. *"Verify check: walk me through every line of the output from the last command."*

**Extend:**

12. *"The video is done. Give me a 10-minute extension challenge using the same tools."*
13. *"The video's DFY artifact works. Now help me add error handling to it."*
14. *"Video complete — I'm ready to deploy this. What are the production considerations?"*
15. *"I watched all of B-007. Am I ready for B-008 (Git Foundation)? Test me."*

---

### Section 3 — Deployment Companion

| Target | Deploy Command | Verify Command | Credential Check |
|---|---|---|---|
| Local workstation | `bash ~/[artifact].sh` | `echo $?` (expect 0) | Via Copilot prompt 29 |
| Remote server | `scp [artifact].sh user@host:~ && ssh user@host 'bash [artifact].sh'` | `ssh user@host '[verify-cmd]'` | Same copilot prompt |
| Docker container | `COPY [artifact].sh /usr/local/bin/ && RUN chmod +x ...` | `docker run ... [verify]` | Via ADA endpoint |
| GitHub Actions | `run: bash [artifact].sh` | `if: steps.*.outcome == 'success'` | Auto-logged to Fabric |
| Cron / systemd timer | `*/10 * * * * /home/user/[artifact].sh` | `systemctl status` | Via ADA /credential |

---

### Section 4 — ACSS Integration

**Hermes events this book emits:**

| Event | Trigger | Destination |
|---|---|---|
| `BookStarted` | First chapter read/watched | Fabric (learner profile update) |
| `DFYLessonBuilt` | Any DFY artifact completed | Fabric (skill graph) + CRM |
| `ErrorEncountered` | Learner reports an error | Fabric (Error Encyclopedia update) |
| `BookCompleted` | All 11 chapters + DFY done | CRM (credential ceremony trigger) |
| `CredentialMinted` | CLL-L0-B007-NetworkNavigator claimed | Fabric + Slack #credentials + ADA |

**Credential ceremony prompt:**
```
I have completed The Network That Connected Everything (B-007).
Chapters completed: 1–11 ✅
DFY lessons built: 10/10 ✅
Appendix D quiz score: [your score]/20
Capstone project (Appendix H): ✅ built and tested

Please initiate the credential ceremony for:
CLL-L0-B007-NetworkNavigator

ACSS route: Hermes → CRM → Fabric → ADA → lippytm.ai/credentials
```

## Appendix D: Quick Quiz & Self-Assessment — Network Navigator

> *"Prove it to yourself before you claim it."*

### 📘 Ebook Quiz — 20 Questions

**Section A — Concepts (fill in the blank)**

1. The command to see all running processes with full details is `ps ______`.
2. To send a polite shutdown signal to PID 1234, you run `kill ______ 1234`.
3. The file used to tell systemd how to run a service is called a ______ file.
4. `journalctl -u myservice ______` shows only the last 50 lines of its logs.
5. Running `command &` starts it in the ______.

**Section B — Read the Command (multiple choice)**

6. What does `systemctl enable myservice` do?
   > a) Start it immediately  b) Configure it to start at boot  c) Check if it's running  d) Remove it

7. What does `kill -9 PID` do that `kill PID` might not?
   > a) Logs the kill to journald  b) Force-kills — the process cannot block or ignore it  c) Kills all child processes too  d) Runs slower

8. What does `journalctl -f` do?
   > a) Shows the first 10 lines  b) Filters by unit  c) Follows the journal in real time  d) Formats output as JSON

9. What does `awk '{print $1}' /etc/passwd` extract?
   > a) The first line  b) The first field of every line  c) The last field  d) Lines matching "1"

10. What does `grep -r "pattern" /etc/` do?
    > a) Searches only /etc/pattern  b) Recursively searches all files under /etc/  c) Searches /etc/ for files named "pattern"  d) Counts occurrences in /etc/

**Section C — Debugging**

11. A service fails to start. What is the first command you run to diagnose it?
    ```
    ___________________________________________
    ```

12. You edited a unit file but `systemctl status` still shows the old behavior. Why?
    ```
    ___________________________________________
    ```

13. Your grep finds no results but you're sure the text is in the file. Name two causes.
    ```
    1. ___________________________________________
    2. ___________________________________________
    ```

**Section D — Application**

14. Write a one-liner to find the 3 processes using the most CPU right now:
    ```
    ___________________________________________
    ```

15. Write the `journalctl` command to show all errors from the last 2 hours:
    ```
    ___________________________________________
    ```

16. Write the command to restart a service called `webapp` and check its status:
    ```
    ___________________________________________
    ```

17. How would you run a script every 5 minutes using a systemd timer instead of cron?
    ```
    ___________________________________________
    ```

**Section E — Build Reflection**

18. Name the DFY artifact you're most likely to use in a production environment:
    ```
    ___________________________________________
    ```

19. In one sentence, what makes systemd superior to traditional init scripts?
    ```
    ___________________________________________
    ```

20. What credential does this book unlock and what does it prove?
    ```
    Credential: ___________________________________________
    Proves: ___________________________________________
    ```

---

**Scoring:** 18–20 = claim credential · 14–17 = review · < 14 = redo DFY lessons 1–5

<details>
<summary>Answer Key</summary>

1. `aux` (ps aux)
2. `-15` (default SIGTERM) or `kill -15 1234`
3. unit (file)
4. `-n 50`
5. background
6. b) Configure it to start at boot
7. b) Force-kills — the process cannot block or ignore it
8. c) Follows the journal in real time
9. b) The first field of every line
10. b) Recursively searches all files under /etc/
11. `sudo systemctl status servicename` and `journalctl -u servicename -n 50`
12. You didn't run `sudo systemctl daemon-reload` after editing the unit file
13. (1) Case sensitivity — use grep -i; (2) Wrong file — you're searching a different path
14. `ps aux --sort=-%cpu | head -4 | tail -3` or `ps aux | sort -k3 -rn | head -4`
15. `journalctl -p err -S "2 hours ago"`
16. `sudo systemctl restart webapp && sudo systemctl status webapp`
17. Create a .service file for the script and a .timer file with OnCalendar=*:0/5, then enable the timer
18. (personal answer)
19. systemd provides parallel startup, dependency management, automatic restart, integrated logging, and cgroup-based resource control — all in one system
20. CLL-L0-B007-NetworkNavigator · proves you can manage Linux processes/services/system tools at a professional level

</details>

---

### 🎧 Audiobook Quiz — 10 Questions

> "Ten questions. Pause at each. Think first."

**Q1:** "What's the difference between SIGTERM and SIGKILL?" → "SIGTERM is a polite request — the process can catch it and clean up. SIGKILL is immediate and cannot be caught or ignored."
**Q2:** "Name the two things you must do after editing a systemd unit file." → "Run daemon-reload, then restart the service."
**Q3:** "What does & do at the end of a command?" → "Runs it in the background as a job."
**Q4:** "What does journalctl -u tell you?" → "Logs specific to that systemd unit."
**Q5:** "What's the difference between awk and sed?" → "sed transforms streams line by line; awk processes fields and is better for structured data."
**Q6:** "What command shows all listening ports?" → "ss -tlnp or ss -tulpn"
**Q7:** "How do you make a process lower priority?" → "nice -n 10 command when starting, or renice 10 -p PID for a running process."
**Q8:** "What does ps aux show that ps alone doesn't?" → "All processes from all users with full CPU/memory/command details."
**Q9:** "What is your DFY capstone for this book?" → "[book['project'][0]] — Full network health dashboard: DNS/connectivity/open ports/bandwidth/firewall status"
**Q10:** "Your credential?" → "CLL-L0-B007-NetworkNavigator"

---

### 🎬 Video Challenges

**Challenge 1:** Start a process in background, list jobs, bring it to foreground, then kill it.
**Challenge 2:** Write and deploy a one-unit systemd service for a hello-world script.
**Challenge 3:** Use journalctl to find the last 5 errors system-wide in the past hour.
**Challenge 4:** Extract the top 5 most frequent words from a log file using grep/awk/sort.
**Challenge 5:** Build the capstone project (net-health-dashboard.sh) from scratch without looking at Appendix H.

---

## Appendix E: Glossary & Error Encyclopedia

---

### 📘 Glossary — Network Navigator Edition

**DNS** — Domain Name System. Translates hostnames (google.com) to IP addresses. `dig` and `nslookup` query it. *B-007 Ch. 1*

**IP address** — Internet Protocol address. IPv4: 4 octets (192.168.1.1). IPv6: 128-bit hex. Identifies a network interface. *B-007 Ch. 2*

**port** — A 16-bit number (1–65535) that identifies a specific service on a host. 80=HTTP, 443=HTTPS, 22=SSH, 53=DNS. *B-007 Ch. 3*

**TCP** — Transmission Control Protocol. Connection-oriented, reliable, ordered delivery. Used for HTTP, SSH, most services. *B-007 Ch. 4*

**UDP** — User Datagram Protocol. Connectionless, fast, no delivery guarantee. Used for DNS, video streaming, gaming. *B-007 Ch. 4*

**curl** — Command-line HTTP client. Sends requests, follows redirects, handles auth, downloads files. The Swiss Army knife of HTTP. *B-007 Ch. 5*

**ss** — Socket Statistics. Shows all open network connections and listening ports. Modern replacement for netstat. *B-007 Ch. 6*

**traceroute** — Maps every hop (router) between your machine and a destination host. Shows latency at each hop. *B-007 Ch. 7*

**firewall** — Packet filter that allows or blocks network traffic based on rules. Tools: iptables, nftables, ufw, firewalld. *B-007 Ch. 8*

**HTTP status code** — 3-digit code in every HTTP response. 2xx=success, 3xx=redirect, 4xx=client error, 5xx=server error. *B-007 Ch. 9*

---

### 📘 Error Encyclopedia — Top 5 Errors

#### Error 1 — `curl: (6) Could not resolve host`
**Fix:** DNS lookup failed. Check /etc/resolv.conf and try `dig hostname`. Often a DNS server issue.

#### Error 2 — `curl: (7) Failed to connect`
**Fix:** Host is reachable but the port is closed/firewalled. Check the service is running and port is open.

#### Error 3 — `ping: connect: Network is unreachable`
**Fix:** No route to the host. Check `ip route` — your default gateway may be missing.

#### Error 4 — `ss shows port LISTEN but connection refused`
**Fix:** The service is bound to 127.0.0.1 (localhost only), not 0.0.0.0 (all interfaces).

#### Error 5 — `traceroute shows * * * (no response)`
**Fix:** Hops that don't respond to ICMP packets. Not necessarily a problem — some routers block ICMP.

---

## Appendix F: Instructor & Accessibility Guide

### Teaching B-007

| Format | Duration | Pace |
|---|---|---|
| Self-study | 1–2 weeks | 1 chapter/day |
| Bootcamp | 2 days | Chs 1–6 day 1, 7–11+DFY day 2 |
| Classroom | 4–5 hours | 2 chapters/hour + DFY build session |

**Top 3 concepts where students consistently struggle:**
1. The mechanism: what the OS is actually doing (not just the command syntax)
2. Error interpretation: reading the real message vs the surface symptom
3. Script integration: combining these tools with what they built in previous books

**Assessment rubric:**

| Skill | Not Ready | Ready | Proficient |
|---|---|---|---|
| Core commands | Needs to look up basic flags | Uses top 10 commands from memory | Composes multi-step pipelines fluently |
| DFY builds | Did not attempt | Built 5+ artifacts | Built all 10, can explain design decisions |
| Debugging | Confused by errors | Can diagnose with Appendix E | Diagnoses unfamiliar errors systematically |
| Capstone | Did not attempt | Built with guidance | Extended it beyond the spec |

**Accessibility:**
- Screen reader: all code blocks in fenced Markdown · ASCII diagrams have text descriptions
- Color-blind: status markers use emoji+text (✅/❌/⏳)
- Dyslexia-friendly: max 20-word sentences · numbered steps ≤ 3 per block
- Offline: all exercises work in a plain terminal · audiobook available as M4B download

---

## Appendix G: Your Learning Path

```
  PHASE 1: Linux Foundations (B-001–B-025)
  ─────────────────────────────────────────────────────────────
  ✅ B-001  Terminal Apprentice
  ✅ B-002  Command Architect
  ✅ B-003  Filesystem Navigator
  ✅ B-004  Script Automator
  ✅ B-005  Package Master
  ✅ B-006  Process Wrangler
  ✅ B-007  Network Navigator
  ✅ B-008  Git Foundation
  ✅ B-009  Text Processor
  ★ B-010  Service Manager         ← (update marker to match book)
  ○ B-011  Secrets Keeper
  ... (15 more in Phase 1)

  Phase 1 Progress: 7/25 completed
```

### Credential Chain
```
  Process Wrangler credential
      ↓
  ★ CLL-L0-B007-NetworkNavigator   ← CLAIM THIS
      ↓
  Git Foundation credential
```

### Cross-Phase Connections

| Skill from B-007 | Grows into (Phase 2 Python) | Grows into (Phase 3 Blockchain) |
|---|---|---|
| Networking | Python networking libraries (B-035+) | Blockchain node management (B-060+) |
| Shell automation | Python subprocess (B-040) | Smart contract deployment scripts (B-066+) |
| System diagnostics | Python monitoring tools (B-049) | On-chain event monitoring (B-075+) |

### 🎧 Audio Path Recap
> *"You are 7 books into Phase 1. Each book builds on the last — the terminal (B-001), commands (B-002), filesystem (B-003), scripting (B-004), packages (B-005), processes (B-006), networking (B-007), git (B-008), text (B-009), services (B-010). Together these ten books cover everything a professional Linux developer uses every single day. You are halfway through Phase 1. Keep going."*

---

## Appendix H: Real Project Showcase

> *"The measure of mastery is what you build when no one is watching."*

### Project: `net-health-dashboard.sh` — Full Network Health Dashboard: Dns/Connectivity/Open Ports/Bandwidth/Firewall Status

**Built with:** B-007 skills only
**Time to build:** 45–75 minutes
**Chapters used:** B-007 Ch. 2-8
**Portfolio value:** Shows practical networking expertise

---

#### Complete Code

```bash
#!/usr/bin/env bash
# net-health-dashboard.sh — comprehensive network status report
# B-007 Capstone · CLL-L0-B007-NetworkNavigator
set -euo pipefail

REPORT="/tmp/net_health_$(date +%Y%m%d_%H%M%S).txt"
PASS=0; FAIL=0

check() {
    local label="$1" cmd="$2"
    if eval "$cmd" &>/dev/null; then
        echo "  ✅ $label" | tee -a "$REPORT"
        PASS=$((PASS+1))
    else
        echo "  ❌ $label" | tee -a "$REPORT"
        FAIL=$((FAIL+1))
    fi
}

echo "" | tee -a "$REPORT"
echo "  ━━━ NETWORK HEALTH DASHBOARD ━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$REPORT"
echo "  $(date)" | tee -a "$REPORT"
echo "" | tee -a "$REPORT"

echo "  [ CONNECTIVITY ]" | tee -a "$REPORT"
check "Internet (ping 8.8.8.8)"   "ping -c 1 -W 2 8.8.8.8"
check "DNS (resolve google.com)"  "dig +short google.com | grep -q ."
check "HTTP (curl google.com)"    "curl -sf --max-time 5 https://google.com"
echo "" | tee -a "$REPORT"

echo "  [ LOCAL INTERFACES ]" | tee -a "$REPORT"
ip -br addr | awk '{printf "  %s
", $0}' | tee -a "$REPORT"
echo "" | tee -a "$REPORT"

echo "  [ LISTENING PORTS ]" | tee -a "$REPORT"
ss -tlnp | tail -n +2 | awk '{printf "  %s\n", $0}' | tee -a "$REPORT"
echo "" | tee -a "$REPORT"

echo "  [ DEFAULT ROUTE ]" | tee -a "$REPORT"
ip route show default | awk '{printf "  %s\n", $0}' | tee -a "$REPORT"
echo "" | tee -a "$REPORT"

echo "  ━━━ RESULTS: $PASS PASS  $FAIL FAIL ━━━━━━━━━━━━━━━━━━" | tee -a "$REPORT"
echo "  Report: $REPORT" | tee -a "$REPORT"
[[ $FAIL -gt 0 ]] && exit 1 || exit 0
```

---

#### How to Deploy

```bash
# 1. Create the file
nano ~/net-health-dashboard.sh

# 2. Paste the code above

# 3. Make executable
chmod +x ~/net-health-dashboard.sh

# 4. Run it
~/net-health-dashboard.sh

# 5. Verify it works
echo "Exit code: $?"
```

#### How to Extend (using later books)

1. **B-014 (Cron):** Schedule this script to run automatically every hour
2. **B-011 (Secrets):** Add credentials/tokens via environment variables instead of hardcoding
3. **B-026+ (Python):** Rewrite the analysis logic in Python for richer output and better error handling

---

#### 🎧 Audiobook

> *"The capstone for The Network That Connected Everything is net-health-dashboard.sh — Full network health dashboard: DNS/connectivity/open ports/bandwidth/firewall status. It uses every core tool from this book in one working script. If you can build this from scratch without looking, you have mastered this book. The credential is waiting."*

#### 🎬 Video Build Scene

1. (0:00) Explain the problem this project solves
2. (1:30) Start with the shebang and `set -euo pipefail`
3. (3:00) Build each section live — explain every line
4. (8:00) Test it end-to-end
5. (10:00) Show one failure and debug it
6. (12:00) Credential claim screen

---


## Further Reading

- 📄 [`docs/B-008-files-that-never-get-lost.md`](B-008-files-that-never-get-lost.md) — Git (uses the same network protocols)
- 📄 [`docs/linux-blockchain-educational-ecosystem.md`](linux-blockchain-educational-ecosystem.md) — Blockchain nodes use the same networking concepts
- 🏠 [`README.md`](../README.md) — Encyclopedia home

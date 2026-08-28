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

## Further Reading

- 📄 [`docs/B-008-files-that-never-get-lost.md`](B-008-files-that-never-get-lost.md) — Git (uses the same network protocols)
- 📄 [`docs/linux-blockchain-educational-ecosystem.md`](linux-blockchain-educational-ecosystem.md) — Blockchain nodes use the same networking concepts
- 🏠 [`README.md`](../README.md) — Encyclopedia home

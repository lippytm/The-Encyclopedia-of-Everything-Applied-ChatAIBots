# B-022: Shell Functions and Aliases

### Build a Personal Productivity Toolkit That Makes Your Terminal Feel Like Home

> *"Aliases are the shortcuts. Functions are the power moves. Together, stored in your .bashrc or .zshrc, they transform an unfamiliar terminal into your most productive tool. Every senior engineer has a personal library of shell functions — this is where yours begins."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Create, export, and persist shell aliases that eliminate repetitive typing
2. Write reusable shell functions that accept arguments and return values
3. Structure a personal `.bashrc`/`.zshrc` that loads cleanly and stays maintainable
4. Build a `~/scripts/lib/` function library sourced at startup
5. Create a `dev-toolkit.sh` that packages your most-used shortcuts

**Prerequisite:** B-001 through B-021

**Build Artifact:** `~/.bashrc_custom` and `~/scripts/lib/dev-toolkit.sh` — a modular shell productivity library

**Credential:** `CLL-L1-B022-ShellCrafter` — on-chain on Base

---

## Chapter 1: Aliases — Shortcuts with Memory

```bash
# In your terminal, an alias is an abbreviation for a longer command
alias ll='ls -la --color=auto'
alias la='ls -A'
alias l='ls -CF'

# Git shortcuts
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'
alias gpl='git pull'
alias gd='git diff'
alias gl='git log --oneline --graph --decorate --all'

# Navigation
alias ..='cd ..'
alias ...='cd ../..'
alias ~='cd ~'
alias ws='cd ~/developer-workspace'
alias docs='cd ~/developer-workspace/docs'

# Safety
alias rm='rm -i'       # prompt before deleting
alias cp='cp -i'       # prompt before overwriting
alias mv='mv -i'       # prompt before overwriting

# See current aliases
alias
type ll   # shows what ll expands to
```

---

## Chapter 2: Making Aliases Permanent

```bash
# Aliases defined in the terminal are session-only
# To persist them, add to ~/.bashrc (bash) or ~/.zshrc (zsh)

cat >> ~/.bashrc << 'EOF'

# === Personal Aliases ===
alias ll='ls -la --color=auto'
alias la='ls -A'
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'
alias gpl='git pull'
alias gl='git log --oneline --graph --decorate --all'
alias ..='cd ..'
alias ...='cd ../..'
alias ws='cd ~/developer-workspace'
EOF

# Reload the shell config
source ~/.bashrc

# Verify
alias | grep "gs="
```

---

## Chapter 3: Shell Functions — When Aliases Aren't Enough

Aliases can't take arguments or run logic. Functions can:

```bash
# Function syntax
function_name() {
    # $1 is first argument, $2 is second, $@ is all
    echo "Hello $1"
}

# Or:
function greet() {
    local name="${1:-World}"  # default to World if no argument
    echo "Hello, $name!"
}

greet              # Hello, World!
greet Charles      # Hello, Charles!
```

---

## Chapter 4: Practical Functions Every Developer Needs

```bash
# Create a directory and immediately cd into it
mkcd() {
    mkdir -p "$1" && cd "$1"
}

# Extract any archive format
extract() {
    case "$1" in
        *.tar.gz|*.tgz)  tar xzf "$1" ;;
        *.tar.bz2|*.tbz) tar xjf "$1" ;;
        *.tar.xz)        tar xJf "$1" ;;
        *.tar)           tar xf  "$1" ;;
        *.gz)            gunzip  "$1" ;;
        *.zip)           unzip   "$1" ;;
        *.7z)            7z x    "$1" ;;
        *)               echo "Don't know how to extract '$1'" ;;
    esac
}

# Git: add, commit, push in one shot
gacp() {
    git add -A
    git commit -m "${1:-auto: update}"
    git push
}

# Create a new project directory with Git and README
newproject() {
    local name="$1"
    [[ -z "$name" ]] && { echo "Usage: newproject <name>"; return 1; }
    mkcd ~/developer-workspace/projects/"$name"
    git init
    echo "# $name" > README.md
    git add README.md
    git commit -m "init: create $name"
    echo "Project $name initialized at: $(pwd)"
}

# Show a file's permission as a human-readable string  (B-003)
perms() {
    stat -c "%a %n" "$@"
}

# Quick http server in current directory
serve() {
    local port="${1:-8080}"
    echo "Serving on http://localhost:$port"
    python3 -m http.server "$port"
}

# Search history by keyword
hist() {
    history | grep --color=auto "$1"
}

# Get your external IP
myip() {
    curl -s ifconfig.me
    echo
}
```

---

## Chapter 5: Structuring Your Function Library

```bash
mkdir -p ~/scripts/lib

cat > ~/scripts/lib/dev-toolkit.sh << 'TOOLKIT'
#!/usr/bin/env bash
# dev-toolkit.sh — Personal shell function library
# Source this from .bashrc: source ~/scripts/lib/dev-toolkit.sh

# === Navigation ===
mkcd() { mkdir -p "$1" && cd "$1"; }

# === Git ===
gacp() {
    git add -A
    git commit -m "${1:-auto: update}"
    git push
}

gs()  { git status; }
gl()  { git log --oneline --graph --decorate --all | head -${1:-20}; }
gnew() {
    local branch="$1"
    [[ -z "$branch" ]] && { echo "Usage: gnew <branch-name>"; return 1; }
    git checkout -b "$branch"
}

# === Archives ===
extract() {
    case "$1" in
        *.tar.gz|*.tgz)  tar xzf "$1" ;;
        *.tar.bz2)        tar xjf "$1" ;;
        *.tar.xz)         tar xJf "$1" ;;
        *.tar)            tar xf  "$1" ;;
        *.gz)             gunzip  "$1" ;;
        *.zip)            unzip   "$1" ;;
        *)                echo "Unknown format: $1" ;;
    esac
}

# === Projects ===
newproject() {
    local name="$1"
    [[ -z "$name" ]] && { echo "Usage: newproject <name>"; return 1; }
    mkcd ~/developer-workspace/projects/"$name"
    git init
    echo "# $name" > README.md
    git add README.md && git commit -m "init: $name"
    echo "✅ Project created at: $(pwd)"
}

# === Utilities ===
serve()  { python3 -m http.server "${1:-8080}"; }
myip()   { curl -s ifconfig.me; echo; }
perms()  { stat -c "%a %n" "$@"; }
hist()   { history | grep --color=auto "$1"; }
reload() { source ~/.bashrc && echo "Shell reloaded."; }

echo "[dev-toolkit] loaded ✅"
TOOLKIT

chmod +x ~/scripts/lib/dev-toolkit.sh

# Add source line to ~/.bashrc
echo "source ~/scripts/lib/dev-toolkit.sh" >> ~/.bashrc
source ~/.bashrc
```

---

## Chapter 6: .bashrc/.zshrc Architecture

A clean, maintainable shell config:

```bash
cat > ~/.bashrc_custom << 'EOF'
# ~/.bashrc_custom — modular shell configuration
# Source from ~/.bashrc: source ~/.bashrc_custom

# --- Environment ---
export EDITOR="nvim"
export PAGER="less -R"
export HISTSIZE=10000
export HISTFILESIZE=20000
export HISTCONTROL=ignoredups:erasedups

# --- PATH Extensions ---
export PATH="$HOME/.local/bin:$HOME/scripts:$PATH"

# --- Prompt ---
PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '

# --- Aliases ---
alias ll='ls -la --color=auto'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias ws='cd ~/developer-workspace'
alias rm='rm -i'
alias cp='cp -i'

# --- Function Library ---
[[ -f ~/scripts/lib/dev-toolkit.sh ]] && source ~/scripts/lib/dev-toolkit.sh

EOF

# Add to .bashrc
echo "source ~/.bashrc_custom" >> ~/.bashrc
source ~/.bashrc
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-022 Verification ==="
echo "Aliases:"
alias | grep -E "ll=|gs=|gacp"

echo ""
echo "Functions:"
type mkcd
type newproject
type extract

echo ""
echo "Toolkit loaded:"
source ~/scripts/lib/dev-toolkit.sh

echo ""
echo "Newproject test:"
newproject test-b022 2>/dev/null && echo "✅ Created" || echo "Already exists"
```

---

## Further Reading

- 📄 [`docs/B-004-the-script-that-did-my-job.md`](B-004-the-script-that-did-my-job.md) — Scripting foundations
- 📄 [`docs/B-015-the-editor-that-does-everything.md`](B-015-the-editor-that-does-everything.md) — Neovim config alongside .bashrc patterns
- 📄 [`docs/B-023-archives-compression-and-backups.md`](B-023-archives-compression-and-backups.md) — The extract function in depth
- 🏠 [`README.md`](../README.md) — Encyclopedia home

# B-017: The Arch Linux Advantage

### Arch Linux, the AUR, and the OMARCHY Developer Workstation Standard

> *"Arch Linux is not for beginners who want an easy desktop. It is for professionals who want to understand exactly what is running on their machine — and why. The OMARCHY standard is built on Arch because Arch gives you a clean canvas, an unmatched package repository, and a rolling release model that keeps you perpetually at the cutting edge without reinstallation."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Explain the Arch Linux philosophy and when to choose it
2. Use `pacman` for all package management operations
3. Install and use packages from the AUR via `yay`
4. Understand what makes OMARCHY different from a default Arch install
5. Bootstrap a minimal Arch developer workstation

**Prerequisite:** B-001 through B-016

**Build Artifact:** An Arch Linux package management cheatsheet script + OMARCHY bootstrap checklist

**Credential:** `CLL-L1-B017-ArchOperator` — on-chain on Base

---

## Chapter 1: The Arch Philosophy

Arch Linux operates on three principles:

| Principle | Meaning | Contrast with Ubuntu |
|---|---|---|
| **Simplicity** | No autoconfig — you choose everything | Ubuntu auto-configures a full desktop |
| **Modernity** | Rolling release — always latest packages | Ubuntu has fixed 6-month release cycles |
| **User-centricity** | You are expected to read the Arch Wiki | Ubuntu assumes you don't want to |

*[Reality — Arch Linux is the upstream base for Manjaro, EndeavourOS, and the OMARCHY workstation standard. Its package repository (official + AUR) contains more packages than any other Linux distribution's repositories]*

---

## Chapter 2: pacman — The Package Manager

```bash
# Update system (always do this first)
sudo pacman -Syu

# Install a package
sudo pacman -S neovim git docker

# Remove a package
sudo pacman -R neovim

# Remove a package and its orphaned dependencies
sudo pacman -Rs neovim

# Search for a package
pacman -Ss "text editor"

# Show package info
pacman -Si neovim

# List installed packages
pacman -Qs

# List explicitly installed packages (not dependencies)
pacman -Qe

# Find which package owns a file
pacman -Qo /usr/bin/nvim

# Clean package cache (keep last 3 versions)
sudo pacman -Sc
```

---

## Chapter 3: The AUR — Arch User Repository

The official repositories have ~14,000 packages. The AUR adds 90,000+ more — contributed by the community, built from source on your machine.

```bash
# Install yay — the AUR helper
# (First time only — clone and build from official repos)
sudo pacman -S --needed base-devel git
git clone https://aur.archlinux.org/yay.git /tmp/yay
cd /tmp/yay && makepkg -si

# After yay is installed:
# yay uses the same syntax as pacman

# Install an AUR package
yay -S google-chrome
yay -S visual-studio-code-bin
yay -S 1password

# Update everything (official + AUR)
yay -Syu

# Search AUR
yay -Ss "notion"
```

*[Reality — the AUR is user-maintained; always inspect the PKGBUILD before installing. Run `yay -G pkgname` to download the PKGBUILD without installing]*

---

## Chapter 4: OMARCHY — The Standard Workstation

OMARCHY is an opinionated Arch Linux developer workstation standard. It makes specific choices so you don't have to:

| Category | OMARCHY Standard | Why |
|---|---|---|
| **Shell** | Zsh + Oh My Zsh | History, completion, plugins |
| **Terminal** | Alacritty | GPU-accelerated, Wayland-native |
| **Editor** | Neovim | Modal, fast, SSH-compatible |
| **Window Manager** | Hyprland (Wayland) | Tiling, animated, modern |
| **Browser** | Brave | Chromium-based, privacy-first |
| **Font** | JetBrains Mono Nerd Font | Ligatures + icons |
| **Theme** | Catppuccin Mocha | Consistent across all tools |
| **Notification** | Dunst | Lightweight, scriptable |

---

## Chapter 5: The Build — OMARCHY Bootstrap Checklist

```bash
#!/bin/bash
# omarchy-bootstrap.sh — B-017 Build Artifact
# Installs the OMARCHY core developer toolchain on a fresh Arch install
# Run after base system install

set -euo pipefail
LOG="$HOME/omarchy-bootstrap.log"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

log "=== OMARCHY Bootstrap Starting ==="

# --- Core system ---
log "Installing core packages..."
sudo pacman -Syu --noconfirm
sudo pacman -S --noconfirm --needed \
    base-devel git curl wget \
    neovim tmux zsh \
    docker docker-compose \
    python python-pip \
    nodejs npm \
    openssh \
    htop btop \
    ripgrep fd bat \
    fzf \
    unzip zip

# --- AUR helper (yay) ---
if ! command -v yay &>/dev/null; then
    log "Installing yay..."
    git clone https://aur.archlinux.org/yay.git /tmp/yay-build
    cd /tmp/yay-build && makepkg -si --noconfirm
    cd ~ && rm -rf /tmp/yay-build
fi

# --- Shell setup ---
log "Setting up Zsh..."
chsh -s /bin/zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# --- Docker ---
log "Enabling Docker..."
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"

# --- SSH ---
log "Setting up SSH..."
if [ ! -f ~/.ssh/id_ed25519 ]; then
    ssh-keygen -t ed25519 -C "$USER@$(hostname)" -f ~/.ssh/id_ed25519 -N ""
fi

# --- Neovim config ---
log "Setting up Neovim..."
mkdir -p ~/.config/nvim
[ -f ~/.config/nvim/init.lua ] || cat > ~/.config/nvim/init.lua << 'LUA'
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.expandtab = true
vim.opt.tabstop = 4
vim.opt.shiftwidth = 4
vim.g.mapleader = " "
vim.keymap.set({"n","i","v"}, "<C-s>", "<Cmd>w<CR>")
vim.keymap.set("i", "jk", "<Esc>")
LUA

log "=== OMARCHY Bootstrap Complete ==="
log "IMPORTANT: Log out and back in for Docker group and Zsh to take effect"
```

---

## Chapter 6: Proof of Work

```bash
echo "=== B-017 Verification ==="
echo "Package manager:"
pacman --version | head -1

echo ""
echo "Explicitly installed packages (top 20):"
pacman -Qe | head -20

echo ""
echo "OMARCHY tools check:"
for tool in nvim git docker zsh curl; do
    command -v "$tool" && echo "  ✅ $tool: $(command -v $tool)" || echo "  ❌ $tool: NOT FOUND"
done
```

---

## Further Reading

- 📄 [`docs/ai-clone-engine-swarms.md`](ai-clone-engine-swarms.md) — OMARCHY is System 7 in the ACSS
- 📄 [`docs/B-015-the-editor-that-does-everything.md`](B-015-the-editor-that-does-everything.md) — Neovim (OMARCHY standard editor)
- 📄 [`docs/linux-blockchain-educational-ecosystem.md`](linux-blockchain-educational-ecosystem.md) — Arch Linux in the LBEE curriculum
- 🏠 [`README.md`](../README.md) — Encyclopedia home

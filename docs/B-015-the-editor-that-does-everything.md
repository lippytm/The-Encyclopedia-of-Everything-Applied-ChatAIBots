# B-015: The Editor That Does Everything

### Neovim — The OMARCHY Standard Text Editor for Professional Developers

> *"Most developers spend 40–60% of their working hours inside a text editor. The tool you choose, and how well you learn it, directly determines your productivity ceiling. Neovim is the OMARCHY standard for a reason: it runs on any machine, in any terminal, over SSH, and with the right configuration it becomes an IDE that exceeds Visual Studio Code in every performance metric."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Navigate files and buffers in Neovim using normal mode
2. Edit text with insert mode, visual mode, and operator-motions
3. Search, find, and replace text efficiently
4. Configure Neovim with a minimal `init.lua`
5. Write and run a Python script entirely inside Neovim

**Prerequisite:** B-001 through B-014

**Build Artifact:** A `~/.config/nvim/init.lua` with line numbers, syntax highlighting, and key mappings — plus a Python script written and run without leaving Neovim

**Credential:** `CLL-L1-B015-NeovimOperator` — on-chain on Base

---

## Chapter 1: Why Neovim? (Not VS Code, Not Nano)

| Editor | Speed | Terminal-friendly | SSH-friendly | Modal | Extensible |
|---|---|---|---|---|---|
| **Neovim** | ⚡ Instant | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Lua API |
| VS Code | 🐢 Heavy | ❌ No | ❌ Limited | ❌ No | ✅ Extensions |
| nano | ⚡ Instant | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| vim | ⚡ Instant | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Vimscript |

Neovim inherits Vim's modal editing philosophy — most time is spent **navigating and operating**, not typing. The result: experienced Neovim users edit code measurably faster than equivalent VS Code users. *[Reality — OMARCHY uses Neovim as the standard editor; configuration lives in `~/.config/nvim/`]*

---

## Chapter 2: Installation

```bash
# Arch/OMARCHY (latest stable)
sudo pacman -S neovim

# Ubuntu/Debian (may need AppImage for latest version)
sudo apt install neovim

# Or install the latest AppImage
curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim-linux-x86_64.appimage
chmod +x nvim-linux-x86_64.appimage
sudo mv nvim-linux-x86_64.appimage /usr/local/bin/nvim

# Verify
nvim --version

# First launch: just open it
nvim
# Type :q! then Enter to exit (for now)
```

---

## Chapter 3: The Modal Editing Mindset

Neovim has four primary modes:

| Mode | Purpose | Enter with |
|---|---|---|
| **Normal** | Navigate, operate — DEFAULT mode | `Esc` |
| **Insert** | Type text | `i`, `a`, `o`, `I`, `A`, `O` |
| **Visual** | Select text | `v`, `V`, `Ctrl-v` |
| **Command** | Run commands | `:` |

**The key insight:** you spend most time in Normal mode. You drop into Insert mode to type a line, then return to Normal mode immediately. This is the opposite of every other editor.

```
Normal mode → i → Insert mode → type text → Esc → Normal mode
Normal mode → : → Command mode → type command → Enter → Normal mode
```

---

## Chapter 4: Essential Normal Mode Commands

### Navigation

```
h j k l        ←  ↓  ↑  →  (don't use arrow keys)
w  W           next word start (w = word, W = WORD)
b  B           previous word start
e  E           word end
0  $           line start / line end
gg G           file start / file end
Ctrl-d         half-page down
Ctrl-u         half-page up
:{n}           go to line n      (:42 → line 42)
```

### Operations (operator + motion)

```
d  = delete    dw = delete word, dd = delete line, d$ = delete to end
c  = change    cw = change word, cc = change line
y  = yank(copy) yw = yank word, yy = yank line
p  P           paste after / before cursor
u  Ctrl-r      undo / redo
.              repeat last change (powerful)
```

### Find and Search

```
/pattern       search forward
?pattern       search backward
n  N           next / previous match
*  #           search word under cursor forward / backward
:%s/old/new/g  replace all occurrences in file
:%s/old/new/gc replace all with confirmation
```

---

## Chapter 5: Insert and Visual Mode

```
# Enter insert mode at various positions
i    insert before cursor
a    append after cursor
I    insert at line start
A    append at line end
o    open new line below
O    open new line above

# Visual mode — select then operate
v    character visual
V    line visual
Ctrl-v  block visual (column select)
# After selecting: d=delete, y=yank, c=change, >=indent
```

---

## Chapter 6: Essential Commands (`:` mode)

```vim
:w             write (save)
:q             quit
:wq  or  ZZ   save and quit
:q!            quit without saving
:e filename    open file
:split filename   horizontal split
:vsplit filename  vertical split
Ctrl-w h/j/k/l    navigate splits
:terminal      open terminal (Neovim-specific)
:help keyword  open help for keyword
```

---

## Chapter 7: The Build — init.lua

```lua
-- ~/.config/nvim/init.lua
-- B-015 Build Artifact — Minimal Neovim configuration (OMARCHY base)

-- ==================== OPTIONS ====================
vim.opt.number = true           -- line numbers
vim.opt.relativenumber = true   -- relative line numbers
vim.opt.expandtab = true        -- spaces not tabs
vim.opt.tabstop = 4             -- 4 spaces per tab
vim.opt.shiftwidth = 4          -- 4 spaces per indent
vim.opt.smartindent = true      -- auto-indent
vim.opt.wrap = false            -- no line wrapping
vim.opt.ignorecase = true       -- case-insensitive search
vim.opt.smartcase = true        -- unless you type uppercase
vim.opt.termguicolors = true    -- full colour support
vim.opt.scrolloff = 8           -- keep 8 lines above/below cursor
vim.opt.updatetime = 50         -- faster cursor hold events
vim.opt.clipboard = "unnamedplus" -- use system clipboard

-- ==================== KEY MAPPINGS ====================
vim.g.mapleader = " "           -- Space as leader key

-- Save with Ctrl-S in any mode
vim.keymap.set({ "n", "i", "v" }, "<C-s>", "<Cmd>w<CR>", { desc = "Save file" })

-- Fast escape from insert mode
vim.keymap.set("i", "jk", "<Esc>", { desc = "Exit insert mode" })

-- Clear search highlighting
vim.keymap.set("n", "<leader>h", ":nohlsearch<CR>", { desc = "Clear highlight" })

-- Split navigation
vim.keymap.set("n", "<C-h>", "<C-w>h", { desc = "Window left" })
vim.keymap.set("n", "<C-j>", "<C-w>j", { desc = "Window down" })
vim.keymap.set("n", "<C-k>", "<C-w>k", { desc = "Window up" })
vim.keymap.set("n", "<C-l>", "<C-w>l", { desc = "Window right" })

-- Open terminal
vim.keymap.set("n", "<leader>t", ":terminal<CR>i", { desc = "Open terminal" })

-- Run current Python file
vim.keymap.set("n", "<leader>r", ":!python3 %<CR>", { desc = "Run Python file" })

-- File explorer
vim.keymap.set("n", "<leader>e", ":Explore<CR>", { desc = "File explorer" })
```

```bash
# Set it up
mkdir -p ~/.config/nvim
# (save init.lua from above to ~/.config/nvim/init.lua)

# Open Neovim and verify
nvim
# :checkhealth — see status report
# :set number? — should print "number"
```

---

## Chapter 8: Writing a Python Script in Neovim

```bash
# Open a new Python file
nvim ~/developer-workspace/scripts/hello_neovim.py
```

Inside Neovim:
```
i                    → enter insert mode
(type your script)   → write the code
Esc                  → return to normal mode
<leader>r            → run the script (maps to :!python3 %)
:wq                  → save and quit
```

A complete workflow — never leaving the terminal:
```
1. nvim app.py           open file
2. i                     insert mode
3. (type code)           write
4. Esc, :w               save
5. <leader>r             run
6. (see output)          verify
7. /bug                  find the bug
8. cw                    change the word
9. Esc, :wq              done
```

---

## Chapter 9: Proof of Work

```bash
# Run these to verify your setup
nvim --version | head -3

echo "Configuration exists:"
ls -la ~/.config/nvim/init.lua

echo ""
echo "Write a test file in Neovim:"
echo 'print("B-015 complete — Neovim operator credential earned")' | \
    nvim -c "w /tmp/b015-test.py" -c "q" -

python3 /tmp/b015-test.py
```

---

## Further Reading

- 📄 [`docs/B-004-the-script-that-did-my-job.md`](B-004-the-script-that-did-my-job.md) — Bash scripts written in Neovim
- 📄 [`docs/ai-clone-engine-swarms.md`](ai-clone-engine-swarms.md) — OMARCHY: the ACSS developer workstation standard
- 📄 [`docs/P011-STACK-001-repo-stack-profile.md`](P011-STACK-001-repo-stack-profile.md) — Neovim in the ACSS stack
- 🏠 [`README.md`](../README.md) — Encyclopedia home

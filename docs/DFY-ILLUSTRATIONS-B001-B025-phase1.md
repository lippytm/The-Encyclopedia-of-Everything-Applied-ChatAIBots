# DFY Illustrations: Phase 1 Linux Foundations (B-001–B-025)

## 750 Illustration Specs — Ebook + Audiobook + Video for All 250 DFY Lessons

> Each lesson has three synchronized illustrations. Read the format key once, then use as a production reference.
>
> **📘 Ebook Figure** — Markdown-renderable visual anchored to the written lesson
> **🎧 Audiobook Callout** — Word-for-word narrator script (lippytmai voice)
> **🎬 Video Scene** — SHOW→BUILD→VERIFY frame description for terminal recording

---

## B-001 — The Terminal and the Curious Mind

---

### DFY-01: Your First Terminal Alias File

**📘 Ebook Figure — Annotated Code Block**
```bash
# ~/.bash_aliases — your shortcut layer on top of Linux

alias ll='ls -lah --color=auto'    # ← human sizes, hidden files, colors
alias gs='git status'              # ← 9 chars instead of 10
alias ..='cd ..'                   # ← go up one directory
alias ...='cd ../..'               # ← go up two directories
alias grep='grep --color=auto'     # ← highlights matches
```
*Figure 1.1: Each alias is a time contract — you pay 1 minute to save it forever.*

**🎧 Audiobook Callout**
> *[CALLOUT TONE]*
> "Done-For-You Moment. Lesson 1: Your First Terminal Alias File.
> Imagine you have a personal remote control for your terminal — every button does exactly what you need, nothing more. An alias file is that remote control. Every line you add saves you keystrokes for the rest of your life.
> Your deliverable is: `~/.bash_aliases` — with 10 shortcuts that match how you work.
> Time to build: 10 minutes.
> Pause here. Build it. Then resume."
> *[CALLOUT TONE × 2]*

**🎬 Video Scene — SHOW→BUILD→VERIFY**
- **SHOW (0–15s):** Terminal splits — left shows raw `git status`, right shows `gs`. Right wins instantly.
- **BUILD (15s–8m):** Open `~/.bash_aliases` in Neovim. Add aliases one by one. Explain each with inline comment. `source ~/.bashrc` after saving.
- **VERIFY (8m–9m):** Run `ll`, `gs`, `..` — each works. `alias` command lists all 10.

---

### DFY-02: Terminal Welcome Screen Script

**📘 Ebook Figure — Data Flow Map**
```
Login event
    ↓
/etc/profile → ~/.bashrc → ~/.bash_profile
    ↓
source motd.sh
    ↓
┌─────────────────────────────────┐
│  🤖 lippytmai  │  $(hostname)   │
│  OS: Arch Linux │  Kernel: 6.x  │
│  CPU: 8 cores   │  RAM: 16 GB   │
│  Uptime: 3d 4h  │  Load: 0.42   │
└─────────────────────────────────┘
```
*Figure 1.2: `motd.sh` turns your login into a situational awareness moment.*

**🎧 Audiobook Callout**
> *[CALLOUT TONE]*
> "Done-For-You Moment. Lesson 2: Terminal Welcome Screen Script.
> Imagine your terminal greets you like a cockpit dashboard — the moment you open it, you know the state of your machine without running a single command. That's exactly what this script delivers.
> Your deliverable is: `motd.sh` — a login screen that shows hostname, OS, CPU, RAM, uptime, and load average in a formatted box.
> Time to build: 15 minutes.
> Pause here. Build it. Then resume."
> *[CALLOUT TONE × 2]*

**🎬 Video Scene — SHOW→BUILD→VERIFY**
- **SHOW (0–15s):** A new terminal opens. The dashboard appears instantly — no commands typed.
- **BUILD (15s–12m):** Write `motd.sh` step by step: `hostname`, `uname -r`, `nproc`, `free -h`, `uptime`. Add box-drawing characters. Add to `~/.bashrc`.
- **VERIFY (12m–13m):** Open a new terminal tab — dashboard appears automatically.

---

### DFY-03: Font and Color Profile for Your Terminal

**📘 Ebook Figure — Before/After Split**
```
BEFORE (default terminal):               AFTER (OMARCHY profile):
─────────────────────────────            ─────────────────────────────
White text on black                      JetBrains Mono 16pt
No ligatures                             Operator Mono ligatures
8-color palette                          256-color Catppuccin Mocha
No Powerline                             Powerline symbols in PS1
```
*Figure 1.3: Your terminal is your primary tool. It deserves the same care as your desk.*

**🎧 Audiobook Callout**
> *[CALLOUT TONE]*
> "Done-For-You Moment. Lesson 3: Font and Color Profile for Your Terminal.
> Imagine spending 8 hours a day in a room with bad lighting and uncomfortable furniture versus a perfectly designed studio. Your terminal is that room. A proper font and color profile reduces eye strain, makes errors visually distinct, and makes your workspace one you want to be in.
> Your deliverable is: a terminal profile — JetBrains Mono, 256-color scheme, with Powerline symbols.
> Time to build: 10 minutes.
> Pause here. Build it. Then resume."
> *[CALLOUT TONE × 2]*

**🎬 Video Scene — SHOW→BUILD→VERIFY**
- **SHOW (0–15s):** Side-by-side: default terminal vs OMARCHY profile. The difference is immediate.
- **BUILD (15s–8m):** Open terminal preferences. Set font, size, color scheme. Export profile as JSON.
- **VERIFY (8m–9m):** Reopen terminal. `ls` output shows colors. Code in Neovim renders ligatures.

---

### DFY-04: Shell History Supercharger

**📘 Ebook Figure — Annotated Code Block**
```bash
# ~/.bashrc — make your shell remember everything

export HISTSIZE=100000          # ← keep 100k commands in memory
export HISTFILESIZE=200000      # ← keep 200k commands on disk
export HISTCONTROL=ignoredups   # ← skip duplicate consecutive commands
export HISTTIMEFORMAT="%F %T "  # ← timestamp every command
shopt -s histappend             # ← append, never overwrite history

# Reload history in every new terminal
export PROMPT_COMMAND="history -a; history -c; history -r; $PROMPT_COMMAND"
```
*Figure 1.4: Your history is a logbook. With these settings, it's searchable back to day one.*

**🎧 Audiobook Callout**
> *[CALLOUT TONE]*
> "Done-For-You Moment. Lesson 4: Shell History Supercharger.
> Imagine being able to recall any command you've ever run, instantly, with the date it was run — even after reboots, new terminals, or remote sessions. Your shell history is the most underrated productivity tool in Linux. These six lines transform it from a 500-line buffer to a lifelong logbook.
> Your deliverable is: six lines in `~/.bashrc` that make your history unlimited, timestamped, and always synced.
> Time to build: 10 minutes.
> Pause here. Build it. Then resume."
> *[CALLOUT TONE × 2]*

**🎬 Video Scene — SHOW→BUILD→VERIFY**
- **SHOW (0–15s):** `Ctrl+R` search — instantly finds a command from last week with timestamp.
- **BUILD (15s–8m):** Add each line to `.bashrc`. Explain each variable. `source ~/.bashrc`.
- **VERIFY (8m–9m):** Run 3 commands. Open new terminal. `history` shows all 3 with timestamps.

---

### DFY-05: Terminal Multiplexer Starter Config

**📘 Ebook Figure — Architecture Map**
```
tmux session: "work"
┌─────────────────────────────────────────────┐
│  Window 0: code    │  Window 1: server       │
│ ┌──────┬──────┐    │ ┌──────────────────┐   │
│ │ nvim │ term │    │ │  uvicorn running │   │
│ │      │      │    │ │                  │   │
│ └──────┴──────┘    │ └──────────────────┘   │
│  2 panes           │  1 pane                │
└─────────────────────────────────────────────┘
  Prefix: Ctrl+a  │  Detach: d  │  Reattach: tmux a
```
*Figure 1.5: tmux lets you run multiple terminals inside one — and come back to them after a disconnect.*

**🎧 Audiobook Callout**
> *[CALLOUT TONE]*
> "Done-For-You Moment. Lesson 5: Terminal Multiplexer Starter Config.
> Imagine your entire development environment — editor, server, logs, tests — all running in named windows you can switch between with a keystroke, and which survive your terminal closing. That's tmux. This config file gives you the six most useful settings: a sane prefix key, mouse support, true color, and persistent sessions.
> Your deliverable is: `~/.tmux.conf` — six settings that make tmux immediately comfortable.
> Time to build: 15 minutes.
> Pause here. Build it. Then resume."
> *[CALLOUT TONE × 2]*

**🎬 Video Scene — SHOW→BUILD→VERIFY**
- **SHOW (0–15s):** A tmux session with three windows — editor, server, logs — switching instantly.
- **BUILD (15s–12m):** Write `~/.tmux.conf` line by line. Explain prefix, mouse, status bar. Reload config.
- **VERIFY (12m–13m):** Create session, split panes, detach, reattach — all persisted.

---

### DFY-06: Custom PS1 Prompt with Git Branch

**📘 Ebook Figure — Data Flow Map**
```
PS1 construction pipeline:
  \u          → username (lippytm)
  @           → separator
  \h          → hostname (archbox)
  :           → separator
  \w          → working directory (~)
  $(__git_ps1 " (%s)")  → git branch if in a repo
  \$          → $ for user, # for root

Result:
  lippytm@archbox:~/projects/myapp (main) $
  ───────────────────────────────────────
         User + host + path + branch
```
*Figure 1.6: A good prompt gives you situational awareness — you always know where you are and what branch you're on.*

**🎧 Audiobook Callout**
> *[CALLOUT TONE]*
> "Done-For-You Moment. Lesson 6: Custom PS1 Prompt with Git Branch.
> Imagine your terminal prompt as a GPS — it tells you your username, machine, directory, and current Git branch at every single moment, without you having to ask. When you're inside a repository and switch branches, your prompt updates instantly. This is one of those quality-of-life changes that feels small but compounds every day.
> Your deliverable is: a PS1 in `~/.bashrc` that shows user, host, path, and git branch in color.
> Time to build: 20 minutes.
> Pause here. Build it. Then resume."
> *[CALLOUT TONE × 2]*

**🎬 Video Scene — SHOW→BUILD→VERIFY**
- **SHOW (0–15s):** Switching between directories and git branches — prompt updates in real time.
- **BUILD (15s–16m):** Build PS1 step by step: colors via `\e[...m`, each component, `__git_ps1`.
- **VERIFY (16m–17m):** `cd` into a git repo, check out different branches — prompt shows each.

---

### DFY-07: Directory Jumping Script

**📘 Ebook Figure — Before/After Split**
```
BEFORE (no jump tool):              AFTER (z.sh configured):
cd ~/projects/acss/docs/phase2/     z phase2
cd ~/work/encyclopedia/docs/        z encyclopedia
cd ../../../../../../               z ~
  ↑ type full path every time         ↑ type 2-3 chars, jump
```
*Figure 1.7: `z` learns your most-visited directories. After one day, it's faster than autocomplete.*

**🎧 Audiobook Callout**
> *[CALLOUT TONE]*
> "Done-For-You Moment. Lesson 7: Directory Jumping Script.
> Imagine typing `z enc` and teleporting directly to your encyclopedia project no matter where you currently are on the filesystem. The `z` tool learns which directories you visit most, and after a single day of use, you'll almost never type a full path again.
> Your deliverable is: `z.sh` configured in `~/.bashrc` — fuzzy directory jumping from anywhere.
> Time to build: 10 minutes.
> Pause here. Build it. Then resume."
> *[CALLOUT TONE × 2]*

**🎬 Video Scene — SHOW→BUILD→VERIFY**
- **SHOW (0–15s):** From `/tmp`, type `z enc` — instantly in the encyclopedia folder.
- **BUILD (15s–8m):** Download `z.sh`, add source to `.bashrc`. Explain frecency algorithm.
- **VERIFY (8m–9m):** Visit 3 directories. Use `z` to jump between them using partial names.

---

### DFY-08: Man Page to Markdown Exporter

**📘 Ebook Figure — Flow Diagram**
```
man ls
  ↓ (raw troff format)
man2md.sh ls
  ↓ col -bx   (strip control chars)
  ↓ sed        (convert headings)
  ↓ awk        (wrap code blocks)
  ↓
ls.md  ← readable Markdown, searchable in your notes app
```
*Figure 1.8: Man pages contain decades of knowledge. Converting them to Markdown makes them part of your searchable knowledge base.*

**🎧 Audiobook Callout**
> *[CALLOUT TONE]*
> "Done-For-You Moment. Lesson 8: Man Page to Markdown Exporter.
> Imagine having every man page you've ever needed converted into a clean, searchable Markdown file in your notes folder — readable in Obsidian, Neovim, or any Markdown viewer, without the visual noise of raw terminal output.
> Your deliverable is: `man2md.sh` — converts any man page to a `.md` file with one command.
> Time to build: 15 minutes.
> Pause here. Build it. Then resume."
> *[CALLOUT TONE × 2]*

**🎬 Video Scene — SHOW→BUILD→VERIFY**
- **SHOW (0–15s):** `man2md.sh ls` runs — `ls.md` opens in Neovim, cleanly formatted.
- **BUILD (15s–12m):** Write script using `man`, `col -bx`, `sed` for heading conversion.
- **VERIFY (12m–13m):** Convert `man grep` → `grep.md`. Open in browser as rendered Markdown.

---

### DFY-09: Terminal Session Logger

**📘 Ebook Figure — Architecture Map**
```
~/.bashrc
  └── trap 'log_cmd "$BASH_COMMAND"' DEBUG
        ↓
  log_cmd() writes to:
        ↓
  ~/logs/
  ├── 2026-08-28.log   ← today's session
  ├── 2026-08-27.log   ← yesterday
  └── 2026-08-26.log   ← the day before

  Format per line:
  [2026-08-28 14:23:01] [lippytm@arch ~/projects] git status
```
*Figure 1.9: Every command you run is recorded with timestamp and directory — your complete terminal diary.*

**🎧 Audiobook Callout**
> *[CALLOUT TONE]*
> "Done-For-You Moment. Lesson 9: Terminal Session Logger.
> Imagine being able to answer the question 'What did I actually do last Tuesday at 3 PM?' with a simple `grep '2026-08-19' ~/logs/`. Every command, every directory, every timestamp — automatically recorded without you thinking about it.
> Your deliverable is: `tlog.sh` — auto-logs every terminal session to dated files in `~/logs/`.
> Time to build: 20 minutes.
> Pause here. Build it. Then resume."
> *[CALLOUT TONE × 2]*

**🎬 Video Scene — SHOW→BUILD→VERIFY**
- **SHOW (0–15s):** `grep "git" ~/logs/2026-08-28.log` — every git command from today with timestamps.
- **BUILD (15s–16m):** Write `tlog.sh` with `trap DEBUG`, timestamp, directory capture.
- **VERIFY (16m–17m):** Run 5 commands. `cat ~/logs/$(date +%F).log` — all 5 appear with times.

---

### DFY-10: "First Day on a New Machine" Checklist

**📘 Ebook Figure — Checklist Visual**
```
✅ Shell: bash/zsh set as default
✅ .bashrc / .zshrc: sourced and working
✅ Git: name, email, editor configured
✅ SSH key: generated, copied to clipboard
✅ Package manager: updated and functional
✅ Editor (Neovim): installed and launches
✅ tmux: installed and config present
✅ Network: DNS resolves, ping works
✅ Clock: timezone and NTP verified
✅ Dotfiles: cloned and stowed
❌ → Any ❌ = machine is not ready for real work
```
*Figure 1.10: A checklist takes 5 minutes. A missed dependency wastes 2 hours.*

**🎧 Audiobook Callout**
> *[CALLOUT TONE]*
> "Done-For-You Moment. Lesson 10: First Day on a New Machine Checklist.
> Imagine a flight checklist. Pilots don't rely on memory — they have a list, and they run through it every single time, because the cost of missing one item is too high. Your development machine is no different. This checklist has 20 items that verify your environment is ready before you write a single line of code.
> Your deliverable is: a personal first-day checklist — 20 items, all checked green before you start.
> Time to build: 5 minutes.
> Pause here. Build it. Then resume."
> *[CALLOUT TONE × 2]*

**🎬 Video Scene — SHOW→BUILD→VERIFY**
- **SHOW (0–15s):** Running through the checklist on a fresh VM — every item turns green.
- **BUILD (15s–4m):** Copy template, personalize 5 items to your specific stack.
- **VERIFY (4m–5m):** Run through it on a test machine — two items fail, then get fixed.

---

## B-002 — Commands That Actually Work

---

### DFY-01: File Management Command Cheat Sheet

**📘 Ebook Figure — Comparison Table**
```
| Goal                    | Command                          |
|-------------------------|----------------------------------|
| List with sizes         | ls -lah                          |
| Find by name            | find . -name "*.py"              |
| Find by content         | grep -r "pattern" .              |
| Copy directory          | cp -r src/ dest/                 |
| Move/rename             | mv old_name new_name             |
| Delete safely           | mv file ~/.trash/                |
| Count files             | find . -type f | wc -l           |
| Show file type          | file unknown_file                |
| Check if file exists    | [ -f path ] && echo yes          |
| Sort by date            | ls -lt                           |
```
*Figure 2.1: 30 commands. One file. Always at hand.*

**🎧 Audiobook Callout**
> *[CALLOUT TONE]*
> "Done-For-You Moment. Lesson 1: File Management Command Cheat Sheet.
> Imagine having a laminated reference card next to your keyboard — except it opens in 0.1 seconds with your favorite text search. This cheat sheet covers 30 file management commands, each with a real-world example, organized by what you're trying to do rather than alphabetically.
> Your deliverable is: `cheatsheet-files.md` — 30 commands, categorized, with examples.
> Time to build: 5 minutes.
> Pause here. Build it. Then resume."
> *[CALLOUT TONE × 2]*

**🎬 Video Scene — SHOW→BUILD→VERIFY**
- **SHOW (0–15s):** `cat cheatsheet-files.md` — clean table renders in terminal with `glow`.
- **BUILD (15s–4m):** Open template, add 5 personalized commands for your workflow.
- **VERIFY (4m–5m):** Pick 3 commands from the sheet, run each — all work as documented.

---

### DFY-02: Bulk File Renamer Script

**📘 Ebook Figure — Data Flow Map**
```
Input directory:                    After rename_files.sh:
  photo_001.jpg                       2026-08-01-photo.jpg
  photo_002.jpg           →           2026-08-02-photo.jpg
  photo_003.jpg                       2026-08-03-photo.jpg
  report_final.pdf                    report_final.pdf (unchanged)

  Usage: rename_files.sh --prefix "2026-08" --ext jpg
```
*Figure 2.2: Bulk renaming without a script means 100 manual operations. With it: one command.*

**🎧 Audiobook Callout**
> *[CALLOUT TONE]*
> "Done-For-You Moment. Lesson 2: Bulk File Renamer Script.
> Picture a folder with 200 photos named `IMG_4521.jpg` through `IMG_4721.jpg`. Now picture the same folder after running one command — every file named by date, topic, and sequence. This script accepts a pattern, a prefix, and an extension, and renames every matching file in seconds.
> Your deliverable is: `rename_files.sh` — renames by pattern, prefix, or extension in bulk.
> Time to build: 20 minutes.
> Pause here. Build it. Then resume."
> *[CALLOUT TONE × 2]*

**🎬 Video Scene — SHOW→BUILD→VERIFY**
- **SHOW (0–15s):** Before: `ls` shows 10 jumbled filenames. After: one command, all renamed cleanly.
- **BUILD (15s–17m):** Write script with `for` loop, `mv`, parameter parsing, dry-run mode.
- **VERIFY (17m–18m):** Run dry-run first (shows what would change), then live run.

---

### DFY-03: Find and Delete Old Files Script

**📘 Ebook Figure — Flow Diagram**
```
cleanup.sh --days 30 --dir ~/downloads --ext log

  find ~/downloads -name "*.log" -mtime +30
        ↓
  Dry-run preview:
    Would delete: debug.log (45 days old, 2.3 MB)
    Would delete: access.log (60 days old, 8.1 MB)
    Total: 2 files, 10.4 MB
        ↓
  Confirm? [y/N]:
        ↓ y
  Deleted. Space reclaimed: 10.4 MB
```
*Figure 2.3: Always dry-run before delete. This script enforces that discipline.*

**🎧 Audiobook Callout**
> *[CALLOUT TONE]*
> "Done-For-You Moment. Lesson 3: Find and Delete Old Files Script.
> Imagine a script that finds every log file older than 30 days, shows you exactly what it would delete and how much space it would free, waits for your confirmation, and only then deletes. That's the difference between automation and reckless automation.
> Your deliverable is: `cleanup.sh` — finds files by age and type, with mandatory dry-run preview.
> Time to build: 15 minutes.
> Pause here. Build it. Then resume."
> *[CALLOUT TONE × 2]*

**🎬 Video Scene — SHOW→BUILD→VERIFY**
- **SHOW (0–15s):** Run cleanup on a test directory — dry-run shows 5 files, confirm, they're gone.
- **BUILD (15s–12m):** `find -mtime`, dry-run flag, confirmation prompt, deletion with logging.
- **VERIFY (12m–13m):** Create 3 old test files. Run script. Verify only old files removed.

---

### DFY-04: Disk Usage Reporter

**📘 Ebook Figure — Architecture Map**
```
disk_report.sh output:
─────────────────────────────────────────
Disk Usage Report — 2026-08-28 14:00
─────────────────────────────────────────
Filesystem: /dev/sda1    Used: 47G / 200G (23%)
[████████░░░░░░░░░░░░░░░░░░░░░░] 23%

TOP 10 LARGEST DIRECTORIES:
  8.2G  /home/lippytm/Videos
  4.1G  /home/lippytm/.cache
  3.3G  /home/lippytm/projects
─────────────────────────────────────────
```
*Figure 2.4: A disk report takes 1 second to read and prevents 100% disk surprises.*

**🎧 Audiobook Callout**
> *[CALLOUT TONE]*
> "Done-For-You Moment. Lesson 4: Disk Usage Reporter.
> Imagine receiving a weekly email — or running a single command — that shows you exactly where your disk space is going: the top 10 directories by size, a visual progress bar for each filesystem, and a warning when you're above 80% full. No more `df -h` followed by `du -sh /*` guessing.
> Your deliverable is: `disk_report.sh` — a formatted disk usage report with progress bars.
> Time to build: 15 minutes.
> Pause here. Build it. Then resume."
> *[CALLOUT TONE × 2]*

**🎬 Video Scene — SHOW→BUILD→VERIFY**
- **SHOW (0–15s):** Script output — clean report with progress bar and top-10 directories.
- **BUILD (15s–12m):** `df -h`, `du -sh`, progress bar with `printf`, threshold warning.
- **VERIFY (12m–13m):** Run report. Create a large test file. Run again — it appears in top-10.

---

### DFY-05: Safe `rm` Wrapper

**📘 Ebook Figure — Before/After Split**
```
BEFORE (rm with no safety net):        AFTER (trash.sh):
$ rm important_file.txt                $ trash important_file.txt
(gone forever)                         Moved to: ~/.trash/important_file.txt

$ rm -rf ~/projects/                   $ trash ~/projects/
(everything gone, no undo)             Moved to: ~/.trash/projects/
                                       $ restore projects  ← get it back!
```
*Figure 2.5: `rm` is permanent. `trash` gives you a 30-day window to change your mind.*

**🎧 Audiobook Callout**
> *[CALLOUT TONE]*
> "Done-For-You Moment. Lesson 5: Safe rm Wrapper.
> Every experienced Linux user has a story about accidentally deleting something important with `rm`. The `trash.sh` wrapper replaces your delete habit with a safer one — files go to a `~/.trash` folder, not into the void. You can restore them. You can review what's there. And a cron job cleans trash older than 30 days automatically.
> Your deliverable is: `trash.sh` — a `rm` replacement that moves files instead of deleting them.
> Time to build: 20 minutes.
> Pause here. Build it. Then resume."
> *[CALLOUT TONE × 2]*

**🎬 Video Scene — SHOW→BUILD→VERIFY**
- **SHOW (0–15s):** `trash important.txt` — file moves to `~/.trash/`. `restore important.txt` — back.
- **BUILD (15s–16m):** Write wrapper, `mv` to `.trash`, collision handling, `restore` function.
- **VERIFY (16m–17m):** Delete 3 files, list trash, restore one, verify it's back.

---

*[Sections DFY-06 through DFY-10 for B-002, and all sections for B-003–B-025 follow the same three-illustration format. Full production specs are generated per-book during the recording and design phase by the `lippytmai` clone in TEACH mode, routed via Hermes event `ILLUS:{book_id}:{lesson}:READY`.]*

---

## Illustration Batch Production Notes

For Phase 1 (B-001–B-025), the full set of 750 illustration specs is produced in batches aligned to QEP approval:

| Batch | Books | Illustrations | Production Gate |
|---|---|---|---|
| Batch 1 | B-001–B-005 | 150 | ✅ B-001 full specs above — template for all |
| Batch 2 | B-006–B-010 | 150 | Produced on QEP-B006-B010 G13 approval |
| Batch 3 | B-011–B-015 | 150 | Produced on QEP-B011-B015 G13 approval |
| Batch 4 | B-016–B-020 | 150 | Produced on QEP-B016-B020 G13 approval |
| Batch 5 | B-021–B-025 | 150 | Produced on QEP-B021-B025 G13 approval |

**Template law:** Every illustration in this system must match the format of B-001's 10 DFY specs above — the three-section structure is non-negotiable for consistency across all 550 lessons.

---

## Illustration Standard Reference

### Ebook Figure Rules
1. Use only plain Markdown (no HTML, no external images)
2. Every figure gets a caption: *Figure N.M: One-sentence insight*
3. ASCII diagrams use `─`, `│`, `┌`, `┐`, `└`, `┘`, `├`, `┤`, `↓`, `→`
4. Code blocks always have a language tag
5. Tables use standard Markdown `|` format

### Audiobook Callout Script Rules
1. Open with `[CALLOUT TONE]`
2. State lesson number and title
3. Mental model analogy: real-world comparison in 2–3 sentences
4. State deliverable and time
5. End with: "Pause here. Build it. Then resume."
6. Close with `[CALLOUT TONE × 2]`
7. Maximum 90 seconds when read aloud at natural pace

### Video Scene Rules
1. Always SHOW→BUILD→VERIFY structure
2. SHOW: must be completable in 15 seconds
3. BUILD: must be completable by learner watching at 1× speed
4. VERIFY: must show the exact output promised in the lesson deliverable
5. Total scene: 8–18 minutes per DFY lesson

---

## Further Reading

- 📄 [`docs/DFY-ILLUSTRATION-SYSTEM.md`](DFY-ILLUSTRATION-SYSTEM.md) — illustration standards
- 📄 [`docs/DFY-B001-B025-phase1-linux.md`](DFY-B001-B025-phase1-linux.md) — Phase 1 DFY lessons
- 📄 [`docs/DFY-ILLUSTRATIONS-B026-B055-phase2.md`](DFY-ILLUSTRATIONS-B026-B055-phase2.md) — Phase 2 illustrations
- 📄 [`docs/ai-copilot-video-sandbox-creator.md`](ai-copilot-video-sandbox-creator.md) — ACVS video pipeline
- 🏠 [`README.md`](../README.md) — Encyclopedia home

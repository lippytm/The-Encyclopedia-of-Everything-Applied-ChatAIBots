# DFY Lessons: Phase 1 Linux Foundations (B-001–B-025)

## 250 Done-For-You Lessons — CLL (Complete Linux Library) L0/L1

> *"You don't just learn Linux here. You leave with 250 working tools, scripts, configs, and checklists — built while you learned."*

---

## How to Use This File

Each section covers one book. Each book has **10 DFY lessons** — numbered DFY-01 through DFY-10.

- **Ebook learners:** Each DFY lesson maps to a Chapter. Run it after you finish that chapter.
- **Audiobook learners:** Each DFY lesson is a "Done-For-You Moment" callout. Pause, build, resume.
- **Video learners:** Each DFY lesson is a dedicated scene in the HDVG video. Follow along in your terminal.

**Credential unlocked:** Complete all 10 DFY lessons for a book → DFY completion marker on your ADA credential record.

---

## B-001 — The Terminal and the Curious Mind

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Your First Terminal Alias File | Config | `~/.bash_aliases` with 10 useful shortcuts | 10 min | Fabric |
| DFY-02 | Terminal Welcome Screen Script | Script | `motd.sh` — prints system info on login | 15 min | Clone Engine |
| DFY-03 | Font and Color Profile for Your Terminal | Config | `.Xresources` / terminal profile JSON | 10 min | OMARCHY |
| DFY-04 | Shell History Supercharger | Config | `.bashrc` with `HISTSIZE`, `HISTCONTROL`, timestamps | 10 min | OMARCHY |
| DFY-05 | Terminal Multiplexer Starter Config | Config | `~/.tmux.conf` — 6 most useful settings | 15 min | OMARCHY |
| DFY-06 | Custom PS1 Prompt with Git Branch | Config | `.bashrc` snippet showing branch + exit code | 20 min | Clone Engine |
| DFY-07 | Directory Jumping Script | Script | `z.sh` wrapper or `cdpath` config for fast navigation | 10 min | Fabric |
| DFY-08 | Man Page to Markdown Exporter | Script | `man2md.sh` — converts any man page to readable `.md` | 15 min | Fabric |
| DFY-09 | Terminal Session Logger | Script | `tlog.sh` — auto-logs every terminal session to `~/logs/` | 20 min | Hermes |
| DFY-10 | "First Day on a New Machine" Checklist | Checklist | 20-item checklist: verify shell, editor, git, network | 5 min | ADA |

---

## B-002 — Commands That Actually Work

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | File Management Command Cheat Sheet | Template | `cheatsheet-files.md` — 30 commands with examples | 5 min | Fabric |
| DFY-02 | Bulk File Renamer Script | Script | `rename_files.sh` — rename by pattern, prefix, extension | 20 min | ADA |
| DFY-03 | Find and Delete Old Files Script | Script | `cleanup.sh` — deletes files older than N days | 15 min | ADA |
| DFY-04 | Disk Usage Reporter | Script | `disk_report.sh` — top 10 largest files + dirs | 15 min | Hermes |
| DFY-05 | Safe `rm` Wrapper | Script | `trash.sh` — moves files to `~/.trash` instead of deleting | 20 min | ADA |
| DFY-06 | Quick Archive Builder | Script | `archive.sh dir [name]` — creates `.tar.gz` with timestamp | 15 min | ADA |
| DFY-07 | Directory Tree Snapshot | Script | `snapshot.sh` — saves `tree` output to dated file | 10 min | Fabric |
| DFY-08 | Permission Audit Script | Script | `check_perms.sh` — flags world-writable files | 15 min | Hermes |
| DFY-09 | Command History Analyzer | Script | `top_commands.sh` — your 20 most-used commands | 10 min | Fabric |
| DFY-10 | File Operations Deployment Checklist | Checklist | Pre-deploy file audit: perms, ownership, size, age | 5 min | ADA |

---

## B-003 — The File That Remembered Everything

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Universal Note-Taking Script | Script | `note.sh` — appends timestamped notes to `~/notes/daily.md` | 15 min | Clone Engine |
| DFY-02 | Log Rotation Config Template | Config | `logrotate.d/myapp` — weekly rotation, 4 keep, compress | 10 min | ADA |
| DFY-03 | File Change Watcher | Script | `watch_file.sh` — alerts when a file is modified | 20 min | Hermes |
| DFY-04 | Append-Only Audit Log Writer | Script | `audit_log.sh` — writes signed, append-only entries | 20 min | Hermes |
| DFY-05 | Config File Backup Script | Script | `backup_configs.sh` — copies dotfiles to `~/dotfiles-backup/` | 15 min | ADA |
| DFY-06 | File Search Power Tool | Script | `fsearch.sh` — combines `find`, `grep`, and `fzf` | 20 min | Fabric |
| DFY-07 | Duplicate File Finder | Script | `find_dupes.sh` — MD5-based duplicate detection | 20 min | Fabric |
| DFY-08 | Version-Tracked Config Template | Template | `.gitconfig` for personal dotfiles repo | 10 min | Clone Engine |
| DFY-09 | File Integrity Checker | Script | `integrity.sh` — SHA256 checksums for critical files | 15 min | Hermes |
| DFY-10 | Data Retention Checklist | Checklist | What to keep, what to archive, what to delete — 15 items | 5 min | ADA |

---

## B-004 — The Script That Did My Job

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Daily Task Automator Template | Template | `daily.sh` — templated script for your repeating morning tasks | 15 min | ADA |
| DFY-02 | Argument Parser Template | Template | Reusable `parse_args()` function with `--help` and `-v` | 15 min | Fabric |
| DFY-03 | Script Error Handler Template | Template | `trap ERR` + `set -euo pipefail` boilerplate | 10 min | Hermes |
| DFY-04 | Progress Bar Function | Script | `progress_bar.sh` — visual progress for long-running loops | 20 min | ADA |
| DFY-05 | Script Self-Documenter | Script | `describe.sh` — reads `##` comments and prints usage | 15 min | Fabric |
| DFY-06 | Multi-Machine Deployer Template | Template | `deploy.sh` — SSH-based deployment to N servers | 25 min | ADA |
| DFY-07 | Idempotent Setup Script Template | Template | `setup.sh` — checks before installing, safe to re-run | 20 min | ADA |
| DFY-08 | Cron-Ready Script Template | Template | Script with locking, logging, and exit-code reporting | 15 min | Hermes |
| DFY-09 | Script Profiler | Script | `time_script.sh` — measures real/user/sys time per section | 15 min | Fabric |
| DFY-10 | Automation Readiness Checklist | Checklist | 12-item check before scheduling any script with cron | 5 min | ADA |

---

## B-005 — Installing Things Without Breaking Things

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Package Install Verification Script | Script | `verify_install.sh` — checks PATH, version, manpage for any tool | 10 min | ADA |
| DFY-02 | Arch Linux Bootstrap Script | Script | `arch_bootstrap.sh` — installs your personal base package list | 30 min | OMARCHY |
| DFY-03 | Dependency Conflict Resolver Checklist | Checklist | 8 steps to diagnose and fix `pacman`/`apt` dependency errors | 5 min | ADA |
| DFY-04 | Package Audit Script | Script | `pkg_audit.sh` — lists manually installed packages + sizes | 15 min | Fabric |
| DFY-05 | Rollback Procedure Template | Template | Step-by-step rollback for a failed `pacman -Syu` | 10 min | ADA |
| DFY-06 | AUR Helper Setup Script | Script | `yay_setup.sh` — installs and configures `yay` on Arch | 20 min | OMARCHY |
| DFY-07 | Virtual Environment Creator | Script | `mkenv.sh` — creates Python venv + activates + installs reqs | 10 min | ADA |
| DFY-08 | Software Inventory Exporter | Script | `export_packages.sh` — saves package list to dated `.txt` | 10 min | Fabric |
| DFY-09 | Installation Log Aggregator | Script | `install_log.sh` — centralizes all `pacman.log` entries | 15 min | Hermes |
| DFY-10 | Safe Update Checklist | Checklist | 10 checks before running a system update | 5 min | ADA |

---

## B-006 — The Process That Wouldn't Stop

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Process Monitor Dashboard | Script | `procmon.sh` — real-time top-10 CPU/RAM processes | 20 min | Hermes |
| DFY-02 | Zombie Process Killer | Script | `kill_zombies.sh` — finds and reaps zombie processes | 15 min | ADA |
| DFY-03 | Process Ownership Auditor | Script | `who_runs.sh` — lists processes by user with PIDs | 10 min | Hermes |
| DFY-04 | Memory Leak Detector Template | Script | `mem_watch.sh` — tracks RSS growth for a named process | 20 min | Hermes |
| DFY-05 | Signal Handler Template | Template | `trap SIGTERM SIGINT` boilerplate for clean shutdown | 10 min | ADA |
| DFY-06 | Background Job Manager | Script | `jobctl.sh` — start/stop/status for named background jobs | 25 min | ADA |
| DFY-07 | Process Dependency Map | Script | `proc_tree.sh` — visualizes parent/child process tree | 15 min | Fabric |
| DFY-08 | CPU Spike Alerter | Script | `cpu_alert.sh` — sends desktop notification when CPU > threshold | 20 min | Hermes |
| DFY-09 | Nice/Renice Automation Template | Template | `priority.sh` — batch-adjusts process priority for build jobs | 10 min | ADA |
| DFY-10 | Process Health Checklist | Checklist | 10 checks when a process is hung or consuming too many resources | 5 min | ADA |

---

## B-007 — The Network That Connected Everything

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Network Health Check Script | Script | `netcheck.sh` — ping, DNS, trace, port scan in one run | 20 min | Hermes |
| DFY-02 | Port Scanner Script | Script | `portscan.sh` — scans common ports on a target host | 15 min | Hermes |
| DFY-03 | Bandwidth Monitor | Script | `bwmon.sh` — per-interface TX/RX in real time using `vnstat` | 20 min | Hermes |
| DFY-04 | DNS Lookup Tool | Script | `dnslookup.sh` — A/MX/TXT/NS records for any domain | 10 min | Fabric |
| DFY-05 | SSL Certificate Checker | Script | `certcheck.sh` — days until expiry for any domain | 15 min | Hermes |
| DFY-06 | `/etc/hosts` Manager | Script | `hosts_manager.sh` — add/remove/list entries safely | 15 min | ADA |
| DFY-07 | Firewall Rule Template | Template | `ufw_setup.sh` — sensible default ufw rules for a dev machine | 20 min | ADA |
| DFY-08 | Network Interface Config Template | Template | `netctl` / `NetworkManager` profile for static IP | 15 min | OMARCHY |
| DFY-09 | HTTP Response Tester | Script | `httptest.sh` — curls a URL, reports status, headers, time | 10 min | Hermes |
| DFY-10 | Network Security Checklist | Checklist | 12 items: open ports, firewall status, DNS, interfaces | 5 min | ADA |

---

## B-008 — Files That Never Get Lost

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Git Repository Initializer | Script | `gitinit.sh` — init + first commit + `.gitignore` + branch rename | 10 min | Clone Engine |
| DFY-02 | Personal `.gitconfig` Template | Config | Full `.gitconfig` with aliases, colors, diff tool, editor | 10 min | Clone Engine |
| DFY-03 | Git Alias Collection | Config | 15 aliases: `git s`, `git lg`, `git undo`, `git amend`, etc. | 10 min | Clone Engine |
| DFY-04 | Pre-Commit Hook Template | Template | `.git/hooks/pre-commit` — lint + test before every commit | 20 min | ADA |
| DFY-05 | Commit Message Template | Template | `.gitmessage` — enforces conventional commit format | 10 min | Hermes |
| DFY-06 | Branch Cleanup Script | Script | `git_prune.sh` — deletes merged local + remote branches | 15 min | ADA |
| DFY-07 | Git Log Pretty Printer | Script | `git_report.sh` — weekly activity report with stats | 15 min | Hermes |
| DFY-08 | Repo Health Checker | Script | `git_health.sh` — checks for large files, secrets, stale branches | 20 min | Hermes |
| DFY-09 | Dotfiles Git Repo Setup | Workflow | Complete workflow: bare repo + checkout for dotfiles | 25 min | Clone Engine |
| DFY-10 | Git Workflow Checklist | Checklist | 10 steps: feature branch → commit → PR → merge → cleanup | 5 min | ADA |

---

## B-009 — Working with Text Like a Pro

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Log Parser Script | Script | `parse_log.sh` — extracts errors/warnings from any log file | 20 min | Hermes |
| DFY-02 | CSV to Markdown Table Converter | Script | `csv2md.sh` — converts CSV to GitHub-flavored Markdown | 15 min | Fabric |
| DFY-03 | Multi-File Search and Replace | Script | `sfreplace.sh` — `sed`-powered find-replace across a directory | 15 min | ADA |
| DFY-04 | Text Statistics Reporter | Script | `textstats.sh` — word count, unique words, reading time | 10 min | Fabric |
| DFY-05 | JSON Pretty-Printer and Validator | Script | `jsonlint.sh` — formats and validates JSON using `jq` | 10 min | Fabric |
| DFY-06 | YAML Validator Script | Script | `yamllint.sh` — validates YAML files using Python `yaml` | 10 min | Fabric |
| DFY-07 | Regex Test Harness | Script | `regextest.sh` — test patterns against sample input interactively | 15 min | Fabric |
| DFY-08 | Column Extractor and Joiner | Script | `colextract.sh` — `awk`-based column extraction from any TSV/CSV | 15 min | Fabric |
| DFY-09 | Markdown Link Checker | Script | `linkcheck.sh` — finds broken internal links in `.md` files | 20 min | Hermes |
| DFY-10 | Text Processing Checklist | Checklist | 8 checks before processing production text data | 5 min | ADA |

---

## B-010 — The Service That Started Itself

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Systemd Service Unit Template | Template | `myapp.service` — Type=simple, restart policy, logging | 15 min | ADA |
| DFY-02 | Systemd Timer Template (Cron Replacement) | Template | `myapp.timer` + `myapp.service` — replaces cron | 20 min | ADA |
| DFY-03 | Service Health Monitor | Script | `svc_health.sh` — checks active/failed status for N services | 15 min | Hermes |
| DFY-04 | Auto-Restart with Alert Script | Script | `svc_watchdog.sh` — restarts failed service + sends alert | 20 min | Hermes |
| DFY-05 | Journal Log Exporter | Script | `journal_export.sh` — exports last N lines of a service's logs | 10 min | Hermes |
| DFY-06 | Service Dependency Graph Generator | Script | `svc_graph.sh` — visualizes `systemd` `Requires`/`After` chains | 20 min | Fabric |
| DFY-07 | Startup Time Analyzer | Script | `boot_time.sh` — ranks slowest services at boot | 10 min | Fabric |
| DFY-08 | Service Hardening Checklist | Checklist | 10 systemd security options: `NoNewPrivileges`, `PrivateTmp`, etc. | 10 min | ADA |
| DFY-09 | Multi-Service Orchestration Template | Template | `docker-compose` → `systemd` bridge for multi-service apps | 25 min | ADA |
| DFY-10 | Service Deployment Checklist | Checklist | 12 steps before enabling a new systemd service in production | 5 min | ADA |

---

## B-011 — Environment Variables and Secrets

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | `.env` Loader and Validator Script | Script | `envload.sh` — loads `.env`, checks required vars, errors loudly | 15 min | ADA |
| DFY-02 | Secrets Audit Script | Script | `secrets_audit.sh` — scans codebase for hardcoded patterns | 20 min | Hermes |
| DFY-03 | Environment Profile Switcher | Script | `envswitch.sh` — switches between dev/staging/prod `.env` files | 15 min | ADA |
| DFY-04 | `.env.example` Generator | Script | `gen_env_example.sh` — creates `.env.example` with values stripped | 10 min | Clone Engine |
| DFY-05 | Vault-Style Local Secrets Template | Template | `pass`-based secrets manager setup for local development | 25 min | ADA |
| DFY-06 | CI/CD Secrets Injection Template | Template | GitHub Actions secrets block + `.env` matrix strategy | 15 min | ADA |
| DFY-07 | Secret Rotation Checklist | Checklist | 10 steps to rotate a leaked or expired credential safely | 5 min | Hermes |
| DFY-08 | Environment Variable Documentation Generator | Script | `env_docs.sh` — generates Markdown table of all env vars | 10 min | Fabric |
| DFY-09 | Runtime Env Validator Script | Template | Python `validate_env.py` — startup check for required vars | 15 min | ADA |
| DFY-10 | Secrets Management Checklist | Checklist | 12-item checklist for new project secrets hygiene | 5 min | ADA |

---

## B-012 — The Container That Held Everything

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Production Dockerfile Template | Template | Multi-stage build with `python:3.12-slim`, non-root user | 20 min | ADA |
| DFY-02 | Docker Compose Dev Stack | Template | `docker-compose.dev.yml` — app + db + redis + hot-reload | 25 min | ADA |
| DFY-03 | Container Health Check Script | Script | `container_health.sh` — reports status for all running containers | 10 min | Hermes |
| DFY-04 | Image Size Auditor | Script | `image_audit.sh` — lists images by size, flags bloated layers | 10 min | Fabric |
| DFY-05 | Docker Log Aggregator | Script | `docker_logs.sh` — tails logs for all services at once | 10 min | Hermes |
| DFY-06 | Container Cleanup Script | Script | `docker_prune.sh` — removes stopped containers, unused images/volumes | 10 min | ADA |
| DFY-07 | Docker Security Checklist | Checklist | 10 items: no-root, read-only FS, drop capabilities, `--env-file` | 5 min | ADA |
| DFY-08 | Multi-Architecture Build Workflow | Workflow | GitHub Actions buildx for `linux/amd64` + `linux/arm64` | 25 min | ADA |
| DFY-09 | Docker Secrets Injection Template | Template | Docker Swarm secrets + compose secrets for production | 20 min | ADA |
| DFY-10 | Container Deployment Checklist | Checklist | 15 steps before `docker compose up` in production | 5 min | ADA |

---

## B-013 — SSH: The Secure Handshake

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | SSH Key Generator Script | Script | `ssh_keygen.sh` — generates ed25519 key with comment + copies to clipboard | 10 min | ADA |
| DFY-02 | SSH Config Template | Config | `~/.ssh/config` — HostAlias, IdentityFile, ForwardAgent per host | 15 min | ADA |
| DFY-03 | SSH Key Distributor | Script | `ssh_push.sh` — copies public key to N servers via `ssh-copy-id` | 10 min | ADA |
| DFY-04 | SSH Tunnel Template | Template | `tunnel.sh` — local port forward + background `autossh` | 20 min | ADA |
| DFY-05 | SSH Bastion Jump Script | Script | `jump.sh` — single command to reach hosts behind a bastion | 15 min | ADA |
| DFY-06 | SSH Hardening Config Template | Config | `sshd_config` — disable password auth, restrict ciphers | 15 min | Hermes |
| DFY-07 | Remote Command Runner | Script | `rcmd.sh` — runs a command on N hosts in parallel | 20 min | ADA |
| DFY-08 | SSH Audit Script | Script | `ssh_audit.sh` — checks key age, algorithm, authorized_keys entries | 15 min | Hermes |
| DFY-09 | Fail2ban Setup Template | Config | `jail.conf` snippet for SSH brute-force protection | 20 min | Hermes |
| DFY-10 | SSH Security Checklist | Checklist | 12 items: keys only, no root, fail2ban, restricted IPs | 5 min | ADA |

---

## B-014 — Cron and the Art of Scheduled Automation

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Cron Job Template Library | Template | 10 ready-to-use crontab entries with comment headers | 10 min | ADA |
| DFY-02 | Cron Wrapper Script | Script | `cronwrap.sh` — adds locking, logging, and failure alerting | 20 min | Hermes |
| DFY-03 | Cron Job Monitor | Script | `cronmon.sh` — verifies jobs ran, reports missed executions | 20 min | Hermes |
| DFY-04 | Cron-to-Systemd Migrator | Script | `cron2systemd.sh` — converts crontab entries to timer units | 25 min | ADA |
| DFY-05 | Log Rotation Cron Template | Template | Weekly log rotation + cleanup + compression crontab | 10 min | ADA |
| DFY-06 | Database Backup Cron Script | Script | `db_backup.sh` — nightly `pg_dump` + S3 upload + verify | 30 min | ADA |
| DFY-07 | Cron Environment Validator | Script | `cron_env.sh` — tests that a script runs correctly in cron's env | 15 min | ADA |
| DFY-08 | Scheduled Report Emailer Template | Template | `send_report.sh` — generates and emails daily report via `msmtp` | 25 min | Hermes |
| DFY-09 | Cron Job Inventory Exporter | Script | `list_crons.sh` — exports all crontabs (all users) to dated file | 10 min | Fabric |
| DFY-10 | Cron Safety Checklist | Checklist | 10 items before scheduling any production cron job | 5 min | ADA |

---

## B-015 — The Editor That Does Everything (Neovim)

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Neovim Bootstrap Config | Config | `~/.config/nvim/init.lua` — lazy.nvim + LSP + treesitter | 30 min | OMARCHY |
| DFY-02 | Python LSP Setup Script | Script | `nvim_python_lsp.sh` — installs `pyright` + `ruff-lsp` | 15 min | OMARCHY |
| DFY-03 | Neovim Keybinding Reference Card | Template | `keybindings.md` — your personal keymap reference | 10 min | Clone Engine |
| DFY-04 | Project Session Manager Config | Config | `neovim-sessions.lua` — auto-save/restore project sessions | 20 min | Clone Engine |
| DFY-05 | File Tree Config Template | Config | `nvim-tree.lua` — file explorer with git status icons | 15 min | OMARCHY |
| DFY-06 | Git Integration Config | Config | `gitsigns.nvim` + `fugitive` config — blame, diff, stage in editor | 20 min | Clone Engine |
| DFY-07 | Neovim Formatter Setup | Config | `conform.nvim` — auto-format on save for Python, Lua, Markdown | 15 min | ADA |
| DFY-08 | Snippet Library Template | Template | 10 personal snippets for your most-used code patterns | 20 min | Clone Engine |
| DFY-09 | Neovim Health Check Script | Script | `nvim_health.sh` — runs `:checkhealth` and saves output | 10 min | ADA |
| DFY-10 | Editor Productivity Checklist | Checklist | 10 items: LSP working, formatter active, shortcuts memorized | 5 min | ADA |

---

## B-016 — Pipes, Redirects, and Composition

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Pipeline Builder Function Library | Script | `pipes_lib.sh` — 8 composable filter functions | 20 min | Fabric |
| DFY-02 | Log Analysis Pipeline | Script | `analyze_logs.sh` — grep → awk → sort → uniq → report | 20 min | Hermes |
| DFY-03 | Data Transform Pipeline Template | Template | `transform.sh` — generic stdin → process → stdout pipeline | 15 min | Fabric |
| DFY-04 | Error Stream Splitter | Script | `split_streams.sh` — separates stdout/stderr to different files | 10 min | Hermes |
| DFY-05 | Named Pipe (FIFO) IPC Template | Template | Producer + consumer scripts via `mkfifo` | 25 min | Hermes |
| DFY-06 | Parallel Pipeline Runner | Script | `parallel_pipe.sh` — runs pipeline stages concurrently with `&` | 20 min | ADA |
| DFY-07 | Pipeline Performance Profiler | Script | `pipe_time.sh` — measures time per stage using `ts` | 15 min | Fabric |
| DFY-08 | Live Data Dashboard Pipeline | Script | `dashboard.sh` — real-time metrics via pipeline + `watch` | 20 min | Hermes |
| DFY-09 | Pipeline Testing Harness | Template | Unit-test shell pipelines with sample input/output fixtures | 20 min | ADA |
| DFY-10 | Pipeline Design Checklist | Checklist | 8 questions before building a production data pipeline | 5 min | ADA |

---

## B-017 — Arch Linux and the OMARCHY Standard

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | OMARCHY Base Package List | Config | `pkgs-base.txt` — your personal Arch base package manifest | 15 min | OMARCHY |
| DFY-02 | Arch Installation Checklist | Checklist | 20-step verified Arch install procedure | 10 min | OMARCHY |
| DFY-03 | Post-Install Bootstrap Script | Script | `arch_post_install.sh` — user, locale, time, AUR, dotfiles | 30 min | OMARCHY |
| DFY-04 | `pacman.conf` Hardened Template | Config | Parallel downloads, color output, ILoveCandy, `NoExtract` rules | 10 min | OMARCHY |
| DFY-05 | Makepkg Config Optimizer | Config | `~/.makepkg.conf` — `MAKEFLAGS`, `COMPRESSXZ`, `BUILDDIR` | 10 min | OMARCHY |
| DFY-06 | System Maintenance Script | Script | `maintenance.sh` — update, clean cache, remove orphans, journal | 20 min | ADA |
| DFY-07 | Arch Snapshot and Rollback Setup | Workflow | `snapper` + `grub-btrfs` for pre-update snapshots | 30 min | ADA |
| DFY-08 | Dotfiles Deployment Workflow | Workflow | GNU Stow-based dotfiles repo with one-command deploy | 25 min | Clone Engine |
| DFY-09 | OMARCHY Developer Workstation Audit | Script | `audit_omarchy.sh` — checks 30 expected tools are installed | 15 min | OMARCHY |
| DFY-10 | OMARCHY Onboarding Checklist | Checklist | 25-item new machine setup checklist | 10 min | OMARCHY |

---

## B-018 — Logs, Monitoring, and Observability

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Centralized Log Aggregator Script | Script | `log_aggregator.sh` — collects logs from N services to one file | 20 min | Hermes |
| DFY-02 | Log Level Filter Tool | Script | `logfilter.sh` — extracts ERROR/WARN/INFO by level | 10 min | Hermes |
| DFY-03 | Prometheus Node Exporter Setup | Workflow | Install + systemd unit + basic scrape config | 25 min | Hermes |
| DFY-04 | Grafana Dashboard Template | Template | JSON dashboard for Linux system metrics (CPU/RAM/disk/net) | 20 min | Hermes |
| DFY-05 | Alert Rule Template (Alertmanager) | Template | `rules.yml` — 5 essential alerting rules | 20 min | Hermes |
| DFY-06 | Log Anomaly Detector Script | Script | `log_anomaly.sh` — flags lines matching error/exception patterns | 20 min | Hermes |
| DFY-07 | Application Heartbeat Monitor | Script | `heartbeat.sh` — checks service health every N seconds | 15 min | Hermes |
| DFY-08 | Uptime Reporter | Script | `uptime_report.sh` — calculates uptime % from log data | 20 min | Hermes |
| DFY-09 | SLA Compliance Checker | Script | `sla_check.sh` — verifies response time < threshold | 20 min | Hermes |
| DFY-10 | Observability Readiness Checklist | Checklist | 12 items: logs, metrics, traces, alerts, dashboards | 5 min | Hermes |

---

## B-019 — Linux Security Essentials

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Security Hardening Script | Script | `harden.sh` — applies 15 hardening steps to a fresh Linux install | 30 min | Hermes |
| DFY-02 | CIS Benchmark Checklist (Subset) | Checklist | 20 highest-priority CIS Linux benchmark items | 10 min | Hermes |
| DFY-03 | File Permission Auditor | Script | `perm_audit.sh` — finds SUID/SGID, world-writable, no-owner files | 15 min | Hermes |
| DFY-04 | User Account Auditor | Script | `user_audit.sh` — lists users with shells, sudo, last login | 10 min | Hermes |
| DFY-05 | Open Ports Reporter | Script | `ports_open.sh` — lists listening ports with owning process | 10 min | Hermes |
| DFY-06 | Failed Login Monitor | Script | `auth_watch.sh` — tails `/var/log/auth.log` for failed attempts | 15 min | Hermes |
| DFY-07 | Rootkit Scanner Automation | Workflow | `rkhunter` install + cron scan + email alert | 20 min | Hermes |
| DFY-08 | `sudoers` Minimal Template | Config | Least-privilege `sudoers` with `NOPASSWD` only for specific commands | 15 min | Hermes |
| DFY-09 | AppArmor / SELinux Status Checker | Script | `mac_status.sh` — verifies MAC framework is active + enforcing | 10 min | Hermes |
| DFY-10 | Security Incident Response Checklist | Checklist | 15 immediate steps when you suspect a compromise | 5 min | Hermes |

---

## B-020 — Disk Space: The Resource That Runs Out

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Disk Usage Report Script | Script | `disk_usage.sh` — top 20 dirs by size + low-space alert | 15 min | Hermes |
| DFY-02 | Log Cleanup Automation | Script | `log_cleanup.sh` — removes logs older than N days | 10 min | ADA |
| DFY-03 | Large File Finder | Script | `find_large.sh` — finds files > N MB anywhere on the system | 10 min | Fabric |
| DFY-04 | Docker Volume Cleaner | Script | `docker_vols.sh` — removes dangling volumes and build cache | 10 min | ADA |
| DFY-05 | Backup Storage Estimator | Script | `backup_size.sh` — estimates how much space backups will consume | 15 min | ADA |
| DFY-06 | inode Exhaustion Checker | Script | `inode_check.sh` — alerts when inode usage > 80% | 10 min | Hermes |
| DFY-07 | Tmpfs Ram Disk Setup Template | Config | `fstab` entry for `/tmp` on `tmpfs` | 10 min | OMARCHY |
| DFY-08 | Disk Quota Setup Script | Script | `quota_setup.sh` — sets per-user disk quotas | 20 min | ADA |
| DFY-09 | Storage Growth Trend Analyzer | Script | `disk_trend.sh` — plots weekly disk growth from log data | 25 min | Hermes |
| DFY-10 | Disk Capacity Planning Checklist | Checklist | 10 questions to answer before a server runs out of space | 5 min | ADA |

---

## B-021 — The Linux Filesystem Explained

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Filesystem Hierarchy Quick Reference | Template | `fs_map.md` — every `/` directory, what goes there, what doesn't | 10 min | Fabric |
| DFY-02 | Mount Point Manager Script | Script | `mount_manager.sh` — list/mount/unmount with labels | 15 min | ADA |
| DFY-03 | Symlink Auditor | Script | `symlink_audit.sh` — finds broken symlinks across the system | 10 min | Fabric |
| DFY-04 | XDG Base Directory Config Template | Config | `~/.config/user-dirs.dirs` — standard XDG layout | 10 min | OMARCHY |
| DFY-05 | Filesystem Type Checker | Script | `fstype.sh` — reports filesystem type and options for each mount | 10 min | Fabric |
| DFY-06 | `/proc` and `/sys` Explorer Script | Script | `proc_info.sh` — extracts useful info from procfs | 15 min | Fabric |
| DFY-07 | BTRFS Subvolume Layout Template | Template | Recommended subvolume layout for snapshots and rollback | 20 min | OMARCHY |
| DFY-08 | Filesystem Integrity Checker | Script | `fsck_schedule.sh` — schedules periodic fsck with reporting | 15 min | Hermes |
| DFY-09 | Automount Config Template | Config | `/etc/fstab` entries with `nofail`, `x-systemd.automount` | 15 min | ADA |
| DFY-10 | Filesystem Planning Checklist | Checklist | 10 decisions before partitioning a new system | 5 min | ADA |

---

## B-022 — Shell Functions and Libraries

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Personal Shell Function Library | Script | `~/.bash_functions` — 20 utility functions for daily use | 30 min | Clone Engine |
| DFY-02 | Logging Library for Shell Scripts | Script | `log_lib.sh` — `log_info`, `log_warn`, `log_error`, `log_debug` | 15 min | Hermes |
| DFY-03 | Argument Validation Library | Script | `args_lib.sh` — `require_arg`, `require_file`, `require_cmd` | 15 min | ADA |
| DFY-04 | Retry Function Template | Script | `retry()` function with exponential backoff | 15 min | ADA |
| DFY-05 | Color Output Library | Script | `color_lib.sh` — `red`, `green`, `yellow`, `blue`, `bold` functions | 10 min | Clone Engine |
| DFY-06 | Interactive Menu Builder | Script | `menu_lib.sh` — arrow-key navigable selection menus | 25 min | ADA |
| DFY-07 | HTTP Client Function Library | Script | `http_lib.sh` — `http_get`, `http_post`, `http_put` via curl | 20 min | Hermes |
| DFY-08 | String Manipulation Library | Script | `str_lib.sh` — `trim`, `upper`, `lower`, `contains`, `starts_with` | 15 min | Fabric |
| DFY-09 | Shared Library Loader Pattern | Template | `source_lib.sh` pattern for reusable shell library loading | 10 min | Fabric |
| DFY-10 | Function Library Testing Template | Template | `bats`-based test suite for shell functions | 20 min | ADA |

---

## B-023 — Backups That Actually Work

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Rsync Backup Script | Script | `rsync_backup.sh` — incremental backup with exclusions + logging | 20 min | ADA |
| DFY-02 | Remote Backup to S3 Script | Script | `s3_backup.sh` — `rclone` or `aws s3 sync` with retention | 25 min | ADA |
| DFY-03 | Database Backup Automation | Script | `db_backup.sh` — `pg_dump` / `mysqldump` + compress + upload | 25 min | ADA |
| DFY-04 | Backup Verification Script | Script | `verify_backup.sh` — restores a random file, checks integrity | 20 min | ADA |
| DFY-05 | Backup Manifest Generator | Script | `backup_manifest.sh` — creates SHA256 manifest of backup contents | 15 min | Hermes |
| DFY-06 | 3-2-1 Backup Strategy Template | Template | `backup_strategy.md` — 3 copies, 2 media, 1 offsite: your setup | 10 min | ADA |
| DFY-07 | Disaster Recovery Runbook Template | Template | `dr_runbook.md` — step-by-step restore procedure | 20 min | ADA |
| DFY-08 | Backup Monitoring Script | Script | `backup_monitor.sh` — alerts when backup is late or too small | 20 min | Hermes |
| DFY-09 | Retention Policy Enforcer | Script | `retention.sh` — deletes backups older than policy allows | 15 min | ADA |
| DFY-10 | Backup Readiness Checklist | Checklist | 15 items: verify restore, test, monitor, document | 5 min | ADA |

---

## B-024 — User and Permission Management

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | New User Setup Script | Script | `adduser_setup.sh` — creates user, sets group, copies skel, restricts shell | 20 min | ADA |
| DFY-02 | Bulk User Creator | Script | `bulk_users.sh` — creates N users from CSV with temp passwords | 20 min | ADA |
| DFY-03 | User Activity Reporter | Script | `user_activity.sh` — last login, command count, open sessions | 15 min | Hermes |
| DFY-04 | Sudo Access Auditor | Script | `sudo_audit.sh` — lists who has sudo + what commands allowed | 10 min | Hermes |
| DFY-05 | Inactive Account Detector | Script | `stale_users.sh` — flags accounts with no login in > 90 days | 15 min | Hermes |
| DFY-06 | Group Membership Manager | Script | `group_mgr.sh` — add/remove users from groups, audit membership | 15 min | ADA |
| DFY-07 | Password Policy Enforcer Config | Config | `pam_pwquality.conf` — min length, complexity, history | 15 min | Hermes |
| DFY-08 | User Offboarding Script | Script | `offboard.sh` — lock account, backup home, remove sessions | 20 min | ADA |
| DFY-09 | ACL Manager Script | Script | `acl_mgr.sh` — sets/reads/removes POSIX ACLs on directories | 20 min | ADA |
| DFY-10 | User Management Checklist | Checklist | 12 items for new user provisioning in a team environment | 5 min | ADA |

---

## B-025 — Linux on Every Platform

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Cross-Platform Script Compatibility Checker | Script | `compat_check.sh` — tests for bash vs sh, GNU vs BSD differences | 20 min | CLL |
| DFY-02 | WSL Setup Script | Script | `wsl_setup.sh` — installs dev tools, configures `.wslconfig` | 25 min | OMARCHY |
| DFY-03 | macOS Compatibility Shims | Script | `mac_shims.sh` — aliases GNU tools for macOS compatibility | 15 min | CLL |
| DFY-04 | Container-First Development Template | Template | `Dockerfile.dev` — Linux-identical dev environment anywhere | 20 min | ADA |
| DFY-05 | CI Platform Matrix Template | Template | GitHub Actions matrix: Ubuntu/macOS/Windows for the same script | 20 min | ADA |
| DFY-06 | Architecture Detection Function | Script | `arch_detect.sh` — detects `x86_64`/`arm64`/`riscv64` at runtime | 10 min | CLL |
| DFY-07 | Package Manager Abstraction Layer | Script | `pkgmgr.sh` — unified `install/remove/update` across apt/pacman/brew | 25 min | CLL |
| DFY-08 | SSH Config for Multiple Platforms | Config | `~/.ssh/config` entries for WSL, VMs, cloud, Raspberry Pi | 15 min | ADA |
| DFY-09 | Platform Capability Matrix | Template | `platform_matrix.md` — what works where, what needs a workaround | 10 min | Fabric |
| DFY-10 | Cross-Platform Deployment Checklist | Checklist | 10 checks before running a script on a new OS or architecture | 5 min | ADA |

---

## Further Reading

- 📄 [`docs/DFY-LESSONS-SYSTEM.md`](DFY-LESSONS-SYSTEM.md) — DFY system overview
- 📄 [`docs/DFY-B026-B055-phase2-python.md`](DFY-B026-B055-phase2-python.md) — Phase 2 DFY lessons
- 📄 [`docs/ai-deployment-activations.md`](ai-deployment-activations.md) — ADA credential system
- 🏠 [`README.md`](../README.md) — Encyclopedia home

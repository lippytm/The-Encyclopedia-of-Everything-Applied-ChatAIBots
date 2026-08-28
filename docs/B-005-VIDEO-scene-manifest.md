# B-005 HDVG Video Script — Installing Things Without Breaking Things

## Scene Manifest | Content ID: B-005-VIDEO | Duration: ~22 min | Level: Beginner

```json
{
  "manifest_version": "1.0",
  "content_id": "B-005-VIDEO",
  "ebook_id": "B-005",
  "title": "Installing Things Without Breaking Things",
  "subtitle": "Package Managers, Python, and the Art of Clean Setup",
  "narrator_voice": "lippytmai",
  "total_duration_estimate_min": 22,
  "credential": "CLL-L1-B005-DevEnvironmentBuilder",
  "gesn_mission": "GESN-B005",
  "intro": {
    "narration": "Every experienced developer has a story about destroying their development environment. The day they ran a global pip install and broke three projects at once. The time they upgraded Python and half their scripts stopped working. Today you get the second-attempt knowledge on your first attempt. Package managers. Virtual environments. Clean, isolated, reproducible Python setups. This is how professionals do it.",
    "visual_prompt": "Before/after animation: chaotic desktop covered in conflicting library versions (version numbers flying everywhere, red error messages). Then: clean isolated project directories, each with its own bubble containing its own Python version and packages. Text: 'Isolated. Reproducible. Professional.'",
    "duration_sec": 45
  },
  "scenes": [
    {
      "id": "S01",
      "title": "What Is a Package Manager?",
      "narration": "A package manager is the librarian of your operating system. When you need a new tool — say, Python, or Docker, or a text editor — you don't download an installer from a random website. You ask the package manager. It knows where to find it, what it depends on, how to install it safely, and how to uninstall it cleanly. Linux distributions ship with their own: apt for Ubuntu and Debian, pacman for Arch, dnf for Fedora. macOS uses Homebrew.",
      "visual_prompt": "Librarian metaphor animation: package manager as a librarian in a vast library. User requests 'Python'. Librarian checks catalog, walks to shelf, retrieves Python plus its 3 dependencies, delivers all 4 items neatly. Contrast: downloading random .exe from internet — question marks, security warnings, no dependency tracking.",
      "code_block": null,
      "interactive_overlay": {
        "type": "quiz",
        "question": "What command updates the package list on Ubuntu/Debian before installing?",
        "options": ["sudo apt upgrade", "sudo apt update", "sudo apt install --refresh", "sudo apt sync"],
        "correct": 1,
        "explanation": "sudo apt update downloads a fresh list of available packages from Ubuntu's servers. It does NOT install anything — it just refreshes the catalog. Always run this before apt install."
      },
      "duration_sec": 85
    },
    {
      "id": "S02",
      "title": "apt — Install, Update, Remove",
      "narration": "The golden sequence for apt: update first, upgrade second, install third. Update refreshes the catalog. Upgrade applies pending updates to your installed software. Install gets you the new thing. Remove takes it out. And autoremove cleans up orphaned dependencies that are no longer needed.",
      "visual_prompt": "Terminal recording showing the three commands running in sequence: apt update (downloading progress bars), apt upgrade (packages updating), apt install python3 (Python installing). Clean, step-by-step animation with timestamps showing how fast each step is.",
      "code_block": {
        "language": "bash",
        "code": "sudo apt update\nsudo apt upgrade -y\nsudo apt install python3 python3-pip python3-venv python3-dev\npython3 --version\npip3 --version"
      },
      "interactive_overlay": null,
      "duration_sec": 80
    },
    {
      "id": "S03",
      "title": "The Virtual Environment Problem",
      "narration": "Here's the conflict: Project Alpha needs requests version 2.28. Project Beta needs requests version 2.31. You can only have one version installed globally. The solution Python invented is the virtual environment — an isolated copy of Python with its own package set, per project. Activate it, install packages, they go into that project only. Deactivate, gone. You can have as many as you need, all running different versions of every library.",
      "visual_prompt": "Two project boxes on screen. A global Python icon tries to serve both, gets pulled apart by conflicting version numbers. Then: two separate venv bubbles appear inside each project. Each bubble has its own Python and its own package set. No conflict. Visual shows the venv/ directory structure inside each project.",
      "code_block": {
        "language": "bash",
        "code": "cd ~/developer-workspace/project-alpha\npython3 -m venv venv\nsource venv/bin/activate\n# (venv) prompt appears\npip install requests\npip list\ndeactivate"
      },
      "interactive_overlay": {
        "type": "quiz",
        "question": "After running 'source venv/bin/activate', how does your terminal prompt change?",
        "options": [
          "Nothing changes visually",
          "(venv) appears at the start of the prompt",
          "The prompt turns red",
          "The terminal closes and reopens"
        ],
        "correct": 1,
        "explanation": "When a virtual environment is active, the venv name appears in parentheses at the start of your prompt: (venv) charles@hostname:~/project$. This tells you which venv is active — crucial for knowing where pip installs will go."
      },
      "duration_sec": 100
    },
    {
      "id": "S04",
      "title": "pip and requirements.txt",
      "narration": "Inside your active venv, pip installs packages into that venv only. pip freeze captures your exact environment — every package and exact version — to a requirements.txt file. Anyone who gets your project can recreate your exact environment with one command: pip install -r requirements.txt. This is how open source projects, deployed APIs, and production systems guarantee everyone is running the same thing.",
      "visual_prompt": "pip freeze runs: packages stream out of the venv bubble into a requirements.txt file. Then: requirements.txt floats to a second computer. pip install -r requirements.txt recreates the identical venv bubble on the second machine. Identical packages, identical versions, highlighted in matching colors.",
      "code_block": {
        "language": "bash",
        "code": "source venv/bin/activate\npip install requests rich\npip freeze > requirements.txt\ncat requirements.txt\n\npip install -r requirements.txt\npip install --upgrade pip"
      },
      "interactive_overlay": null,
      "duration_sec": 80
    },
    {
      "id": "S05",
      "title": "The Build — Complete Python Dev Environment",
      "narration": "Follow along. We're going to create a virtual environment, install packages, write a Python program that uses type hints and imports, make it executable, and save our environment. This is the exact workflow you'll use at the start of every Python project for the rest of your career.",
      "visual_prompt": "Step-by-step terminal walkthrough. Each step labeled with a number. venv creation, activation, pip install, writing hello_world.py, running it (rich table appears in terminal), pip freeze, .gitignore creation. Each step checkmarked on completion.",
      "code_block": {
        "language": "bash",
        "code": "cd ~/developer-workspace/project-alpha\npython3 -m venv venv\nsource venv/bin/activate\npip install --upgrade pip\npip install requests rich\n# write src/hello_world.py (see ebook)\npython3 src/hello_world.py\npip freeze > requirements.txt\necho 'venv/\\n__pycache__/\\n*.pyc' > .gitignore"
      },
      "interactive_overlay": {
        "type": "build_gate",
        "prompt": "Create venv, install rich, write and run hello_world.py. The rich table should display in your terminal. Mark complete to earn your badge.",
        "required_output": "B-005: Python Dev Environment — ACTIVE",
        "xp_reward": 200,
        "unlocks_credential": "CLL-L1-B005-DevEnvironmentBuilder"
      },
      "duration_sec": 160
    },
    {
      "id": "S06",
      "title": "The Full Environment Stack",
      "narration": "Let's zoom out and see what you've built over Books B-001 through B-005. Hardware at the bottom. Linux kernel. Bash shell. Package manager. Python. pip. venv. Your code at the top. Each layer isolates and controls the layer above it. You now understand the entire stack that every Python developer stands on. The next 20 books will teach you to build on it.",
      "visual_prompt": "Layer diagram builds from bottom to top: Hardware → Linux Kernel → Shell (Bash) → Package Manager (apt/pacman) → Python 3.x → pip → venv → Your Code. Each layer glows as it's narrated. A second diagram shows the same stack for a cloud server — identical layers. Text: 'Same stack. Everywhere.'",
      "code_block": null,
      "interactive_overlay": {
        "type": "quiz",
        "question": "Why should you never install Python packages globally (without a venv)?",
        "options": [
          "Global installs are slower",
          "Different projects may need different versions of the same package, causing conflicts",
          "Global Python packages require sudo and are a security risk",
          "pip does not work without a venv"
        ],
        "correct": 1,
        "explanation": "Without venvs, all projects share the same Python and the same set of installed packages. When two projects need different versions of the same package, only one version can be installed — causing subtle import errors and broken environments."
      },
      "duration_sec": 90
    },
    {
      "id": "S07",
      "title": "Outro",
      "narration": "You've completed the first five books of the lippytm.ai Earn-while-you-Learn series. Terminal. Commands. Permissions. Scripting. Python environment. You have the foundation. In B-006, you'll learn process management — how to find, monitor, and control the programs running on your Linux system. Keep building.",
      "visual_prompt": "GESN mission complete. Badge: CLL-L1-B005. XP: +250. Skill tree: 'Python Setup', 'Package Management', 'Virtual Environments' nodes light up. Series progress bar: 5/100 Beginner books complete. B-006 preview card.",
      "code_block": null,
      "interactive_overlay": {
        "type": "mission_complete",
        "badge": "CLL-L1-B005-DevEnvironmentBuilder",
        "xp_total": 250,
        "series_progress": "5/100 Beginner Complete",
        "next_mission": "B-006-VIDEO",
        "next_title": "The Process That Wouldn't Stop"
      },
      "duration_sec": 45
    }
  ]
}
```

*Production notes: 7 scenes, ~22 min, 5 interactive overlays, 250 XP. Approved under QEP-B001-B005.*

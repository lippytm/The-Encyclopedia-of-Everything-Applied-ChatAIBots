# B-001 HDVG Video Script — The Terminal and the Curious Mind

## Scene Manifest for HD Video Generator (HDVG)
### Content ID: B-001-VIDEO | Duration: ~18 min | Level: Beginner | Format: MP4/WebM/HLS

---

```json
{
  "manifest_version": "1.0",
  "content_id": "B-001-VIDEO",
  "ebook_id": "B-001",
  "title": "The Terminal and the Curious Mind",
  "subtitle": "Your First Steps in Linux and the Command Line",
  "narrator_voice": "lippytmai",
  "total_duration_estimate_min": 18,
  "credential": "CLL-L0-B001-TerminalApprentice",
  "gesn_mission": "GESN-B001",
  "intro": {
    "narration": "What if I told you that underneath every smartphone, every website, every AI model, and every blockchain — there is a black screen with a blinking cursor. And the developers who build those systems? They talk to that cursor every single day. Welcome to The Terminal and the Curious Mind. My name is lippytmai. I'm your AI guide through the lippytm.ai Earn-while-you-Learn series. By the end of this video, you will have created your first real project on your computer — using only your keyboard. Let's begin.",
    "visual_prompt": "Cinematic opening: dark terminal screen, blinking cursor center frame. Text appears letter by letter: 'Every great system starts here.' Cut to: montage of beautiful server rooms, blockchain visualizations, AI neural networks, a robot hand — all traced back to a terminal prompt.",
    "duration_sec": 45
  },
  "scenes": [
    {
      "id": "S01",
      "title": "What Is a Terminal?",
      "narration": "Your computer has two faces. The face you already know — windows, icons, a mouse. And the face that runs underneath it all — the terminal. The terminal is not scary. It's just faster. Think of it this way: your operating system is a city. The shell is the language everyone speaks in that city. And the terminal is the phone you use to call anyone, anywhere, instantly.",
      "visual_prompt": "Split screen animation: left side shows a modern GUI desktop, right side shows a clean terminal. An animated arrow shows the same 'create folder' action — GUI takes 4 clicks, terminal takes 1 command. Speed comparison graphic. Label each part: OS=city, Shell=language, Terminal=phone.",
      "code_block": null,
      "interactive_overlay": {
        "type": "quiz",
        "question": "What is the shell?",
        "options": ["The physical computer hardware", "The program that reads your commands", "The graphical user interface", "The internet browser"],
        "correct": 1,
        "explanation": "The shell (like Bash or Zsh) is the program that interprets your typed commands and sends them to the operating system."
      },
      "duration_sec": 90
    },
    {
      "id": "S02",
      "title": "Opening Your Terminal",
      "narration": "Let's open yours right now. On Linux: press Control-Alt-T. On macOS: Command-Space, type terminal, press Enter. On Windows: install WSL2 — I'll show you how in just a moment. Once it opens, you'll see something like this: your username, your computer name, a tilde, and a dollar sign. That dollar sign is the prompt. It means: I'm ready. What do you want to do?",
      "visual_prompt": "Screen recording style: hands on keyboard, pressing Ctrl+Alt+T on Ubuntu. Terminal window opens with a satisfying animation. Zoom in on the prompt. Annotate each part with callout labels: username in green, hostname in blue, ~ in yellow, $ in white.",
      "code_block": {
        "language": "bash",
        "code": "charles@lippytm-dev:~$\n# username @ hostname : current-directory $ prompt"
      },
      "interactive_overlay": null,
      "duration_sec": 75
    },
    {
      "id": "S03",
      "title": "Your File System Is a Tree",
      "narration": "Before you can navigate, you need a map. Your computer's files are organized in a tree — everything branches from a single root, written as a forward slash. Your home directory — where all your personal files live — is written as a tilde. Think of it as your apartment in the city of your operating system.",
      "visual_prompt": "Animated tree diagram building from root. Branches appear one by one: /home, /etc, /usr, /var. Then zoom into /home/charles — highlight it, label it with a house icon. Animation connects tilde symbol to the home directory path.",
      "code_block": {
        "language": "bash",
        "code": "/                    ← root (top of everything)\n├── home/\n│   └── charles/    ← your home = ~\n│       ├── Documents/\n│       └── projects/\n├── etc/             ← system config\n└── usr/             ← installed programs"
      },
      "interactive_overlay": {
        "type": "quiz",
        "question": "What does ~ (tilde) represent in Linux?",
        "options": ["The root directory /", "Your current directory", "Your home directory", "The parent directory"],
        "correct": 2,
        "explanation": "Tilde (~) is a shorthand for your home directory, e.g., /home/charles. You can use it in any path: ~/Documents means /home/charles/Documents."
      },
      "duration_sec": 90
    },
    {
      "id": "S04",
      "title": "pwd, ls, cd — Your Navigation Trio",
      "narration": "Three commands. That's all you need to navigate anywhere on your system. pwd — Print Working Directory — tells you exactly where you are. ls — List — shows you what's in your current location. cd — Change Directory — moves you somewhere else. Let me show you each one.",
      "visual_prompt": "Split screen: terminal on left, animated file tree on right. As each command is typed, the tree highlights the corresponding location. pwd causes a pulsing ring around current node. ls reveals the children. cd moves a glowing cursor to the new directory.",
      "code_block": {
        "language": "bash",
        "code": "pwd\n# Output: /home/charles\n\nls\n# Output: Documents  Downloads  projects\n\ncd Documents\npwd\n# Output: /home/charles/Documents\n\ncd ..\n# Go up one level\n\ncd ~\n# Go home from anywhere"
      },
      "interactive_overlay": {
        "type": "challenge",
        "prompt": "Using only pwd, ls, and cd — navigate to your Documents folder and back home. Type the three commands you would use.",
        "answer_hint": "cd Documents → pwd → cd ~",
        "xp_reward": 50
      },
      "duration_sec": 120
    },
    {
      "id": "S05",
      "title": "mkdir, touch, echo, cat — Building Things",
      "narration": "Navigation is reading. Now let's write. mkdir creates directories. touch creates empty files. echo sends text to the screen — and with a redirect symbol, it sends text into a file. cat shows you a file's contents. These four commands are the foundation of creating anything on a Linux system.",
      "visual_prompt": "Time-lapse style: directory tree grows in real time as commands are typed. Each mkdir adds a new branch. Each touch adds a leaf. The echo redirect is visualized as water flowing into a container (the file). cat opens the container and shows the contents.",
      "code_block": {
        "language": "bash",
        "code": "mkdir my-first-project\ncd my-first-project\ntouch hello.txt\necho \"Hello from the terminal!\" > hello.txt\ncat hello.txt\n# Output: Hello from the terminal!"
      },
      "interactive_overlay": null,
      "duration_sec": 90
    },
    {
      "id": "S06",
      "title": "The Build — Live Demo",
      "narration": "Now it's your turn. Follow along exactly. We're going to create a real project directory, write your first file, and verify your build. This is your proof of work for Book B-001. Pause the video, open your terminal, and follow each step.",
      "visual_prompt": "Full-screen terminal recording. Commands appear one at a time with a 2-second pause between each. Each command has a callout explaining what it does. Final output shows the complete directory structure with ls -la. Overlay: green checkmarks appear next to each completed step.",
      "code_block": {
        "language": "bash",
        "code": "cd ~\nmkdir my-first-project\ncd my-first-project\necho \"Name: Your Name Here\" > hello.txt\necho \"Date: $(date)\" >> hello.txt\necho \"Goal: Learn to build from first principles.\" >> hello.txt\nmkdir notes\nnano notes/b001-reflections.txt\n# Type your reflection, then Ctrl+O, Enter, Ctrl+X\nls -la\ncat hello.txt"
      },
      "interactive_overlay": {
        "type": "build_gate",
        "prompt": "Complete the build above. When your ls -la output matches the expected structure, mark this step complete to unlock your B-001 credential.",
        "required_files": ["hello.txt", "notes/b001-reflections.txt"],
        "xp_reward": 200,
        "unlocks_credential": "CLL-L0-B001-TerminalApprentice"
      },
      "duration_sec": 180
    },
    {
      "id": "S07",
      "title": "What You Just Did — The Deeper Understanding",
      "narration": "Let's take a step back. You just did something that millions of professional developers do every single day. You navigated a file system. You created structured directories. You wrote files from the command line. You used command substitution with dollar-sign-parentheses to insert the current date dynamically. Each of these patterns will appear in every book in this series — from Python scripts to blockchain deployments.",
      "visual_prompt": "Concept map radiating from the terminal icon: branches to 'Web Development', 'Cloud Engineering', 'Blockchain/Web3', 'AI/ML', 'DevOps'. Each branch shows a real tool that uses terminal skills: React CLI, AWS CLI, Hardhat, Python ML training, Docker.",
      "code_block": null,
      "interactive_overlay": {
        "type": "quiz",
        "question": "What does >> do differently than > when writing to a file?",
        "options": [
          ">> overwrites the file, > appends to it",
          ">> appends to the file, > overwrites it",
          "They do the same thing",
          ">> creates a new file, > updates an existing one"
        ],
        "correct": 1,
        "explanation": "> overwrites (replaces all existing content). >> appends (adds to the end without deleting what's already there). This distinction matters enormously when writing log files."
      },
      "duration_sec": 90
    },
    {
      "id": "S08",
      "title": "Outro — What Comes Next",
      "narration": "You've completed Book B-001: The Terminal and the Curious Mind. You've earned your CLL Level 0 Terminal Apprentice credential. In Book B-002, you'll learn the 20 commands that cover 80% of everything professional developers do — copy, move, delete, search, and build your first multi-project workspace. See you there. Keep building.",
      "visual_prompt": "GESN mission complete screen: badge animation (CLL-L0-B001 badge spins and locks into place). Credential card appears with learner's name. Text: 'Mission Complete. 250 XP earned.' Preview thumbnail for B-002 appears with a continue button.",
      "code_block": null,
      "interactive_overlay": {
        "type": "mission_complete",
        "badge": "CLL-L0-B001-TerminalApprentice",
        "xp_total": 250,
        "next_mission": "B-002-VIDEO",
        "next_title": "Commands That Actually Work"
      },
      "duration_sec": 45
    }
  ]
}
```

---

## Production Notes

| Property | Value |
|---|---|
| **Narration voice** | lippytmai (ElevenLabs custom voice) |
| **Total scenes** | 8 |
| **Estimated runtime** | 18 minutes |
| **Interactive overlays** | 6 (4 quizzes, 1 challenge, 1 build gate, 1 mission complete) |
| **GESN XP total** | 250 XP |
| **Credential gate** | Scene S06 build_gate triggers `CLL-L0-B001-TerminalApprentice` mint |
| **Quality gate** | Must pass G1–G13 QEP before distribution |
| **Output formats** | MP4 (1080p), WebM (1080p), HLS adaptive stream |
| **Subtitle track** | Auto-generated via Whisper, reviewed by Engine 5 |

---

## Further Reading

- 📄 [`docs/B-001-the-terminal-and-the-curious-mind.md`](B-001-the-terminal-and-the-curious-mind.md) — The ebook this script is based on
- 📄 [`docs/P011-VIDEO-001-hd-video-generator.md`](P011-VIDEO-001-hd-video-generator.md) — The HDVG pipeline that produces this video
- 📄 [`docs/P011-GESN-001-gamer-educational-systems-networks.md`](P011-GESN-001-gamer-educational-systems-networks.md) — GESN missions and badges
- 🏠 [`README.md`](../README.md) — Encyclopedia home

# B-002 HDVG Video Script — Commands That Actually Work

## Scene Manifest | Content ID: B-002-VIDEO | Duration: ~20 min | Level: Beginner

```json
{
  "manifest_version": "1.0",
  "content_id": "B-002-VIDEO",
  "ebook_id": "B-002",
  "title": "Commands That Actually Work",
  "subtitle": "The 20 Bash Commands That Cover 80% of Real Developer Work",
  "narrator_voice": "lippytmai",
  "total_duration_estimate_min": 20,
  "credential": "CLL-L0-B002-CommandBuilder",
  "gesn_mission": "GESN-B002",
  "intro": {
    "narration": "You've opened the terminal. You navigated it. Now let's make it do real work. In this video you'll learn the 20 commands that professional developers use every single day — to copy files, move projects, search through thousands of lines of logs, and chain tools together into pipelines. These are the commands that make your terminal feel like a superpower. Let's go.",
    "visual_prompt": "Fast-cut montage: developer hands flying across keyboard, log files scrolling, files moving between directories with animated paths. Text overlays count up: '1 command... 5 commands... 20 commands.' Final frame: a glowing command line with the text 'Your toolkit is ready.'",
    "duration_sec": 40
  },
  "scenes": [
    {
      "id": "S01",
      "title": "The 20 Commands Table",
      "narration": "Here are your 20. We'll cover every single one. Notice something: they fall into categories. Navigation — you already know those from B-001. File operations: cp, mv, rm. Viewing: cat, head, tail, wc. Searching: grep, find. The pipe. History. And the manual. Let's start with file operations.",
      "visual_prompt": "Animated table builds row by row. Each row slides in with the command name, a short description, and a color-coded category badge (blue=navigation, green=file ops, orange=search, purple=pipeline, red=danger zone for rm).",
      "code_block": null,
      "interactive_overlay": {
        "type": "quiz",
        "question": "Which command moves OR renames a file?",
        "options": ["cp", "mv", "rm", "touch"],
        "correct": 1,
        "explanation": "mv does both: mv old.txt new.txt renames it; mv file.txt ~/Documents/ moves it. Same command, different argument patterns."
      },
      "duration_sec": 80
    },
    {
      "id": "S02",
      "title": "cp and mv — Copy and Move",
      "narration": "cp makes a copy and leaves the original. mv moves the original — which also works as a rename, because a rename is just moving a file to a new name in the same directory. Watch how I use them, and notice the pattern: source first, destination second. Always.",
      "visual_prompt": "Split-screen file tree animation. Left side: original file structure. Right side: destination. When cp runs, an animated copy of the file flies to the destination, original stays. When mv runs, the file physically slides from source to destination, leaving nothing behind.",
      "code_block": {
        "language": "bash",
        "code": "cp hello.txt backup/hello-backup.txt\ncp -r my-project/ my-project-backup/\n\nmv old-name.txt new-name.txt\nmv report.txt ~/Documents/\nmv draft.txt ~/Documents/final-report.txt"
      },
      "interactive_overlay": null,
      "duration_sec": 90
    },
    {
      "id": "S03",
      "title": "rm — The Dangerous One",
      "narration": "rm deletes files permanently. There is no Recycle Bin. There is no undo. This is the command that has ended careers when used carelessly on production servers. So we learn one rule: always run ls on the path first. See what's there. Then delete. Every. Single. Time.",
      "visual_prompt": "Dramatic visual: files disappear into a black void when rm runs. Red warning icon appears. Then: the safety protocol animation — green path shows ls first (files appear, verified), then rm runs safely. Rule appears in large text: 'ls before rm -rf. Every time.'",
      "code_block": {
        "language": "bash",
        "code": "ls old-project/\nrm -rf old-project/\n\nmkdir -p ~/.trash\nmv risky-file.txt ~/.trash/"
      },
      "interactive_overlay": {
        "type": "quiz",
        "question": "What is the safest way to delete a directory called 'old-build'?",
        "options": [
          "rm -rf old-build/",
          "ls old-build/ then rm -rf old-build/ after verifying",
          "delete it from the file manager GUI",
          "mv old-build/ /dev/null"
        ],
        "correct": 1,
        "explanation": "Always ls first to verify what you're about to delete. rm -rf is permanent — there's no undo on the terminal."
      },
      "duration_sec": 90
    },
    {
      "id": "S04",
      "title": "grep and find — Search Everything",
      "narration": "grep searches inside files. find searches for files. Together, they can locate anything on your system in seconds. Here's the pattern I use every day: grep to find the content I need, find to locate the file that has it. Let me show you both.",
      "visual_prompt": "Split animation: left panel shows a stack of log files; grep sends a beam of light through them and highlights matching lines. Right panel shows a file tree; find sends a search beam through directories and illuminates matching files. Both complete simultaneously.",
      "code_block": {
        "language": "bash",
        "code": "grep -rn \"error\" ./logs/\ngrep -i \"ERROR\" app.log\ngrep -v \"DEBUG\" app.log\ngrep -c \"404\" access.log\n\nfind . -name \"*.py\"\nfind . -mtime -1\nfind . -type d -name \"node_modules\""
      },
      "interactive_overlay": {
        "type": "challenge",
        "prompt": "Search the ~/developer-workspace directory recursively for any file containing the word 'project'. What command would you use?",
        "answer_hint": "grep -r 'project' ~/developer-workspace/",
        "xp_reward": 75
      },
      "duration_sec": 110
    },
    {
      "id": "S05",
      "title": "The Pipe — Your First Pipeline",
      "narration": "The pipe character — the vertical bar — is the most important concept in Unix. It takes the output of one command and feeds it directly as input to the next. You're not just running commands anymore. You're chaining them together into pipelines — mini programs you build from single-purpose tools. This is the Unix philosophy. And it's beautiful.",
      "visual_prompt": "Animated pipeline visualization: command 1 outputs a stream of data (represented as glowing particles), the pipe symbol captures it, feeds it into command 2 which filters it, another pipe feeds command 3 which counts it. Final number glows. Text: 'Composable. Reusable. Powerful.'",
      "code_block": {
        "language": "bash",
        "code": "ls -la | grep \".py\"\nls -la | grep \".py\" | wc -l\ngrep \"ERROR\" app.log | tail -10\ncat essay.txt | tr ' ' '\\n' | sort | uniq -c | sort -rn | head -20"
      },
      "interactive_overlay": {
        "type": "quiz",
        "question": "What does this command do: ls | grep '.py' | wc -l",
        "options": [
          "Lists all files, shows only Python files, counts characters",
          "Lists all files, filters for .py files, counts the matching lines",
          "Searches file contents for .py, then counts words",
          "Finds all Python files and deletes them"
        ],
        "correct": 1,
        "explanation": "ls lists all files → pipe to grep '.py' keeps only lines containing .py → pipe to wc -l counts those lines. Result: the number of Python files in the current directory."
      },
      "duration_sec": 110
    },
    {
      "id": "S06",
      "title": "The Build — Developer Workspace",
      "narration": "Now build it yourself. Pause here, open your terminal, and follow along. We're creating a full developer workspace with three projects, a logs folder, and a README — using every command from this book.",
      "visual_prompt": "Full-screen terminal recording showing the complete build sequence. Directory tree animates in real time on the right side as each command executes. Green checkmarks appear on each completed step. Final frame: full tree visible with all files present.",
      "code_block": {
        "language": "bash",
        "code": "mkdir -p ~/developer-workspace\ncd ~/developer-workspace\nmkdir -p project-alpha/src project-alpha/tests\nmkdir -p project-beta/src project-beta/docs\nmkdir -p project-gamma/src project-gamma/config\ntouch project-alpha/src/main.py\ntouch project-beta/src/app.js\ntouch project-gamma/src/server.rs\nmkdir logs\necho \"$(date): Workspace created\" > logs/setup.log\nfind . -type f\necho \"File count: $(find . -type f | wc -l)\""
      },
      "interactive_overlay": {
        "type": "build_gate",
        "prompt": "Create the developer-workspace structure above. Run 'find . -type f | wc -l' — the output should be at least 7. Mark complete to earn your badge.",
        "required_files": ["project-alpha/src/main.py", "logs/setup.log"],
        "xp_reward": 200,
        "unlocks_credential": "CLL-L0-B002-CommandBuilder"
      },
      "duration_sec": 150
    },
    {
      "id": "S07",
      "title": "Outro",
      "narration": "You now have 20 commands in your arsenal. You can navigate, create, copy, move, delete safely, search files and their contents, and build pipelines. In B-003, you'll learn permissions — who can read, write, and execute every file. That knowledge will unlock the ability to build secure systems. See you there.",
      "visual_prompt": "GESN mission complete screen. Badge: CLL-L0-B002-CommandBuilder. XP: +250. Skill tree lights up 'Bash Navigation' and 'File Operations' nodes. Preview card for B-003 appears.",
      "code_block": null,
      "interactive_overlay": {
        "type": "mission_complete",
        "badge": "CLL-L0-B002-CommandBuilder",
        "xp_total": 250,
        "next_mission": "B-003-VIDEO",
        "next_title": "The File That Remembered Everything"
      },
      "duration_sec": 45
    }
  ]
}
```

---

*Production notes: 7 scenes, ~20 min, 5 interactive overlays, 250 XP. Approved under QEP-B001-B005.*

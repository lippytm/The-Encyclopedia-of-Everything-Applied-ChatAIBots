# B-003 HDVG Video Script — The File That Remembered Everything

## Scene Manifest | Content ID: B-003-VIDEO | Duration: ~22 min | Level: Beginner

```json
{
  "manifest_version": "1.0",
  "content_id": "B-003-VIDEO",
  "ebook_id": "B-003",
  "title": "The File That Remembered Everything",
  "subtitle": "Linux Permissions, Users, and Groups",
  "narrator_voice": "lippytmai",
  "total_duration_estimate_min": 22,
  "credential": "CLL-L1-B003-PermissionsEngineer",
  "gesn_mission": "GESN-B003",
  "intro": {
    "narration": "In 1969, the engineers who built Unix faced a challenge that would define computing for the next 60 years: how do you give many people access to the same machine without letting them destroy each other's work? The answer they invented is still running on every Linux server, every macOS laptop, and every cloud instance in the world right now. It's called the permission model. And once you understand it, you'll never look at a file the same way again.",
    "visual_prompt": "1969 historical aesthetic: black-and-white photo of Bell Labs transitions to modern colorful server room. Timeline graphic shows Unix 1969 → Linux 1991 → AWS 2006 → every cloud server today. A single file icon persists through all eras, glowing with permission bits.",
    "duration_sec": 50
  },
  "scenes": [
    {
      "id": "S01",
      "title": "The Three Layers: Owner, Group, Others",
      "narration": "Every file on Linux has three pieces of ownership. The owner — the user who created it. The group — a named collection of users who share access. And others — everyone else. For each of these three, the system can grant or deny three operations: read, write, and execute.",
      "visual_prompt": "Three concentric rings animate around a file icon. Innermost ring: owner (gold). Middle ring: group (silver). Outer ring: others (bronze). Three operation icons appear on each ring: an eye for read, a pencil for write, a running figure for execute. Some icons light up, others go dark.",
      "code_block": null,
      "interactive_overlay": {
        "type": "quiz",
        "question": "Who does 'others' refer to in Linux permissions?",
        "options": [
          "Other files in the same directory",
          "Other processes running on the system",
          "Everyone on the system except the owner and group members",
          "Other administrators only"
        ],
        "correct": 2,
        "explanation": "'Others' is everyone on the system who is neither the file owner nor a member of the file's group. This is the most public access level."
      },
      "duration_sec": 85
    },
    {
      "id": "S02",
      "title": "Reading the Permission String",
      "narration": "Run ls -la on any directory and you'll see strings like this: dash-rwx-r-x-r-x. Let me decode that for you permanently. The first character is the type: dash for a regular file, d for directory, l for symlink. The next nine characters are three groups of three — owner, group, others. r for read, w for write, x for execute, dash for none.",
      "visual_prompt": "Large animated permission string: -rwxr-xr-x. Brackets appear below each section. The first character bracket labels 'file type'. The next three bracket as 'owner'. The next three as 'group'. The final three as 'others'. Color-coded: rwx=green, r-x=blue, ---=red.",
      "code_block": {
        "language": "bash",
        "code": "ls -la\n# -rwxr-xr-x 1 charles developers 891 Aug 28 deploy.sh\n# -rw-r--r-- 1 charles charles   234 Aug 28 README.md\n# -rw------- 1 charles charles    44 Aug 28 .secret\n# drwxr-xr-x 5 charles developers  80 Aug 28 project-alpha/"
      },
      "interactive_overlay": {
        "type": "quiz",
        "question": "What do the permissions -rw-r--r-- mean?",
        "options": [
          "Owner can read/write/execute; group can read; others can read",
          "Owner can read/write; group can read; others can read",
          "Owner can read/write; group and others have no access",
          "Everyone can read and write"
        ],
        "correct": 1,
        "explanation": "rw- = read+write (no execute). r-- = read only. So: owner reads and writes, group reads, others read. This is the standard permission for non-executable files like text documents and configs."
      },
      "duration_sec": 100
    },
    {
      "id": "S03",
      "title": "chmod — Changing Permissions",
      "narration": "chmod has two modes. Symbolic mode uses letters: u for user, g for group, o for others, a for all. Plus to add, minus to remove, equals to set exactly. Octal mode uses numbers: r is 4, w is 2, x is 1. Add them together for each group. 7 is full access. 6 is read-write. 5 is read-execute. 4 is read-only. 0 is nothing. The two most common patterns you'll use every day: 755 for scripts and directories, 644 for regular files.",
      "visual_prompt": "Side-by-side: symbolic mode on left, octal on right. Symbolic: letters animate in to form 'u+x', 'g-w', 'a=r'. Octal: binary digit wheels spin to show 7=111, 6=110, 5=101. Final graphic: the two most-used patterns 755 and 644 displayed large with their use cases labeled.",
      "code_block": {
        "language": "bash",
        "code": "chmod u+x deploy.sh\nchmod g-w config.json\nchmod a+r README.md\n\nchmod 755 deploy.sh\nchmod 644 config.json\nchmod 600 .secret\nchmod 700 private/"
      },
      "interactive_overlay": {
        "type": "quiz",
        "question": "Which chmod command would make a file readable only by its owner?",
        "options": ["chmod 644 file", "chmod 600 file", "chmod 755 file", "chmod 400 file"],
        "correct": 1,
        "explanation": "chmod 600 = rw------- : owner has read+write, group and others have nothing. chmod 400 would give owner read-only. For an SSH key or .env file, 600 is the standard."
      },
      "duration_sec": 110
    },
    {
      "id": "S04",
      "title": "chown and Groups",
      "narration": "chmod changes what can be done to a file. chown changes who owns it. You can change just the owner, or the owner and group together using a colon separator. And chgrp changes just the group. These are the commands you'll use when setting up project directories for a team — or when you need to fix a permission error on a server.",
      "visual_prompt": "File card animation: ownership badge changes as chown runs. Before: 'charles/charles'. After: 'alice/developers'. The change propagates through a directory tree with -R flag. Group badge separately changes with chgrp.",
      "code_block": {
        "language": "bash",
        "code": "chown alice report.txt\nchown alice:developers report.txt\nchgrp developers report.txt\nsudo chown -R $USER:developers ~/team-project/"
      },
      "interactive_overlay": null,
      "duration_sec": 80
    },
    {
      "id": "S05",
      "title": "The Build — Secure Team Project",
      "narration": "Now let's build a real secure directory structure. Three roles: you as owner with full access, a developers group with collaborative access, and the world with read-only access to docs and logs. Every permission we set has a reason. Watch and follow along.",
      "visual_prompt": "Directory tree animates with permission badges on each folder. Color coding: owner badges gold, group badges silver, others badges bronze. As chmod commands run, badges update in real time. secrets/ folder pulses red to indicate maximum restriction. Final state: full annotated tree.",
      "code_block": {
        "language": "bash",
        "code": "sudo groupadd developers 2>/dev/null; sudo usermod -aG developers $USER\nmkdir -p ~/team-project/{src,tests,docs,secrets,logs}\ncd ~/team-project\nsudo chown -R $USER:developers .\nchmod 750 .\nchmod 775 src/ docs/\nchmod 750 tests/\nchmod 700 secrets/\nchmod 755 logs/\nchmod 600 secrets/env.secret\nls -la"
      },
      "interactive_overlay": {
        "type": "build_gate",
        "prompt": "Create team-project/ with the permission structure above. Run 'ls -la ~/team-project/' — secrets/ must show drwx------. Mark complete to earn your badge.",
        "required_permissions": {"secrets/": "700", "src/": "775"},
        "xp_reward": 200,
        "unlocks_credential": "CLL-L1-B003-PermissionsEngineer"
      },
      "duration_sec": 150
    },
    {
      "id": "S06",
      "title": "Outro",
      "narration": "You now understand the Linux permission model — the same model protecting servers at Google, AWS, and every major blockchain node in the world. In B-004, you'll write your first Bash script — and you'll use chmod to make it executable. See you there.",
      "visual_prompt": "GESN mission complete. Badge: CLL-L1-B003. XP: +275. Skill tree: 'File Permissions' and 'User Management' nodes light up. B-004 preview card.",
      "code_block": null,
      "interactive_overlay": {
        "type": "mission_complete",
        "badge": "CLL-L1-B003-PermissionsEngineer",
        "xp_total": 275,
        "next_mission": "B-004-VIDEO",
        "next_title": "The Script That Did My Job"
      },
      "duration_sec": 40
    }
  ]
}
```

*Production notes: 6 scenes, ~22 min, 5 interactive overlays, 275 XP. Approved under QEP-B001-B005.*

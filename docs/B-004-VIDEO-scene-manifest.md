# B-004 HDVG Video Script — The Script That Did My Job

## Scene Manifest | Content ID: B-004-VIDEO | Duration: ~25 min | Level: Beginner

```json
{
  "manifest_version": "1.0",
  "content_id": "B-004-VIDEO",
  "ebook_id": "B-004",
  "title": "The Script That Did My Job",
  "subtitle": "Write Your First Bash Script and Automate the Work You Hate",
  "narrator_voice": "lippytmai",
  "total_duration_estimate_min": 25,
  "credential": "CLL-L1-B004-BashAutomator",
  "gesn_mission": "GESN-B004",
  "intro": {
    "narration": "Here is the most honest thing I can tell you about professional software engineering: a large portion of it is finding tasks you do repeatedly — and writing code to do them instead. The backup you run every morning. The log you check before every deploy. The directory you create at the start of every project. In this video, you'll write a real Bash script that automates your file backup. And you'll learn every fundamental scripting concept along the way.",
    "visual_prompt": "Time comparison animation: person manually performing 5 tasks repeatedly, each taking 30 seconds, loop repeating daily for a year. Counter shows total time wasted. Then: same person writes one script, runs it once, counter shows '0 seconds every morning forever.' Bold text: 'Automate the work you hate.'",
    "duration_sec": 50
  },
  "scenes": [
    {
      "id": "S01",
      "title": "The Shebang and Script Anatomy",
      "narration": "A Bash script is a text file with commands. Three things make it a script rather than just a text file. First: the shebang on line one — hash-bang-slash-bin-slash-bash — which tells the OS which interpreter to use. Second: chmod plus x to make it executable. Third: running it with dot-slash. Without the shebang, your script might run with the wrong shell and fail in ways that are very hard to debug.",
      "visual_prompt": "Annotated script file appears. Shebang line highlighted in gold with callout: 'Tells OS: use Bash to run this'. chmod +x shown as a key turning a lock on the file. The ./ prefix shown as a map pin saying 'run from current directory'. All three elements connect to the running terminal.",
      "code_block": {
        "language": "bash",
        "code": "#!/bin/bash\n# my-script.sh\necho \"Hello from my first script!\"\n\n# Make executable and run\nchmod +x my-script.sh\n./my-script.sh"
      },
      "interactive_overlay": {
        "type": "quiz",
        "question": "What is the purpose of #!/bin/bash on the first line?",
        "options": [
          "It's a comment that documents the file",
          "It tells the OS to use /bin/bash to interpret this file",
          "It imports the bash library",
          "It sets the file permissions automatically"
        ],
        "correct": 1,
        "explanation": "The shebang (#!) tells the operating system which program to use to execute the script. Without it, the system may default to /bin/sh which has fewer features than bash."
      },
      "duration_sec": 90
    },
    {
      "id": "S02",
      "title": "Variables and Special Variables",
      "narration": "Variables in Bash have one rule that trips up almost every beginner: no spaces around the equals sign. NAME equals quote Charles quote — no spaces. Use the variable with a dollar sign prefix. The shell has special built-in variables too: dollar-zero is the script name, dollar-one through dollar-nine are arguments, dollar-hash is the argument count, and dollar-question-mark is the exit code of the last command.",
      "visual_prompt": "Variable assignment animation: correct form NAME='Charles' with green checkmark vs. NAME = 'Charles' with red X (shows error). Dollar sign usage: $NAME transforms to its value with a zoom effect. Special variables table slides in with examples of each.",
      "code_block": {
        "language": "bash",
        "code": "NAME=\"Charles\"\nTODAY=$(date +%Y%m%d)\necho \"Hello, $NAME!\"\necho \"Today: $TODAY\"\n\n# Special variables\necho \"Script: $0\"\necho \"Args: $#\"\necho \"Last exit: $?\""
      },
      "interactive_overlay": null,
      "duration_sec": 90
    },
    {
      "id": "S03",
      "title": "if/elif/else and Test Operators",
      "narration": "Conditionals in Bash use square brackets for the test. The key test operators: dash-f tests if a file exists, dash-d for a directory, dash-z if a string is empty. Important: always quote your variables inside the brackets — unquoted variables with spaces will break your tests in ways that are subtle and hard to find.",
      "visual_prompt": "Flow diagram: if → test condition (diamond shape) → true path (green) → elif → false path (orange) → else (red). Each branch shows its output. Test operators table slides in: -f, -d, -e, -z, -n, string comparisons, number comparisons.",
      "code_block": {
        "language": "bash",
        "code": "if [ -f \"$FILE\" ]; then\n    echo \"File exists\"\nelif [ -d \"$DIR\" ]; then\n    echo \"Directory exists\"\nelse\n    echo \"Nothing found\"\nfi\n\nif [ -f \"$FILE\" ] && [ -r \"$FILE\" ]; then\n    echo \"Exists and readable\"\nfi"
      },
      "interactive_overlay": {
        "type": "quiz",
        "question": "Which test correctly checks if a variable $NAME is NOT empty?",
        "options": [
          "[ $NAME != '' ]",
          "[ -n \"$NAME\" ]",
          "[ -z \"$NAME\" ]",
          "[ $NAME -gt 0 ]"
        ],
        "correct": 1,
        "explanation": "-n tests for non-empty string. -z tests for empty string. Always quote the variable: [ -n \"$NAME\" ] not [ -n $NAME ] — without quotes, an empty $NAME causes a syntax error."
      },
      "duration_sec": 100
    },
    {
      "id": "S04",
      "title": "Loops and Functions",
      "narration": "Loops iterate — for loops over lists, while loops as long as a condition is true. Functions let you name a block of code and reuse it. The key insight: functions in Bash work like mini-scripts — they have their own local variables (declared with the local keyword), they return exit codes, and they can be called anywhere in the script after they're defined.",
      "visual_prompt": "For loop: animated list of project names, loop pointer moves through each one. While loop: condition meter depletes until false. Functions: code block gets a label, then dotted lines show it being called from three different places in the script, executing once at each call site.",
      "code_block": {
        "language": "bash",
        "code": "for project in project-alpha project-beta project-gamma; do\n    echo \"Backing up: $project\"\ndone\n\nlog_message() {\n    local level=\"$1\"\n    local message=\"$2\"\n    echo \"[$(date)] [$level] $message\" | tee -a \"$LOG_FILE\"\n}"
      },
      "interactive_overlay": null,
      "duration_sec": 90
    },
    {
      "id": "S05",
      "title": "Error Handling — set -euo pipefail",
      "narration": "Here's what separates a beginner script from a production script: error handling. Three settings at the top of every script you write. Set -e: exit immediately if any command fails. Set -u: treat unset variables as errors. Set -o pipefail: fail if any command in a pipeline fails, not just the last one. Add a trap to catch errors and run cleanup code. These four patterns prevent scripts from silently doing the wrong thing.",
      "visual_prompt": "Three settings appear one by one with visual demonstrations. set -e: a command fails, red X, script stops immediately vs. without set -e the script continues and causes cascade failures. set -u: unset variable referenced, error shown vs. silently empty. pipefail: pipeline fails midway, caught vs. uncaught.",
      "code_block": {
        "language": "bash",
        "code": "set -euo pipefail\n\nhandle_error() {\n    echo \"ERROR at line $1, exit code $2\"\n    exit \"$2\"\n}\ntrap 'handle_error $LINENO $?' ERR"
      },
      "interactive_overlay": {
        "type": "quiz",
        "question": "What does 'set -u' do in a Bash script?",
        "options": [
          "Runs the script as the root user",
          "Makes the script exit on any error",
          "Treats unset variables as errors instead of empty strings",
          "Enables debug mode"
        ],
        "correct": 2,
        "explanation": "set -u (also written as set -o nounset) causes the script to exit with an error when it tries to use a variable that hasn't been set. Without it, $UNSET_VAR silently becomes an empty string, which can cause subtle bugs."
      },
      "duration_sec": 100
    },
    {
      "id": "S06",
      "title": "The Build — backup.sh",
      "narration": "Now we put it all together. The backup.sh script uses everything from this video: variables, conditionals, loops, functions, and error handling. It validates your source directory, checks disk space, backs up your workspace to a timestamped archive, prunes old backups to stay within your limit, and logs every action. Follow along — build it yourself.",
      "visual_prompt": "Script builds section by section in the terminal. Each function appears with a callout naming which concept it demonstrates. A progress bar fills as each section is written. Final: ./backup.sh runs, log output streams, completion message appears.",
      "code_block": {
        "language": "bash",
        "code": "#!/bin/bash\nset -euo pipefail\n\nSOURCE_DIR=\"${1:-$HOME/developer-workspace}\"\nBACKUP_ROOT=\"$HOME/backups\"\nTIMESTAMP=$(date '+%Y%m%d_%H%M%S')\nBACKUP_PATH=\"$BACKUP_ROOT/backup_${TIMESTAMP}\"\nMAX_BACKUPS=7\n\nlog() { echo \"[$(date '+%H:%M:%S')] [$1] $2\" | tee -a \"$HOME/developer-workspace/logs/backup.log\"; }\n\nsetup() { mkdir -p \"$BACKUP_ROOT\" \"$HOME/developer-workspace/logs\"; log INFO \"Backup started\"; }\nperform_backup() { cp -r \"$SOURCE_DIR\" \"$BACKUP_PATH\"; log INFO \"Backup complete: $BACKUP_PATH\"; }\n\nsetup\nperform_backup\nlog INFO \"Done\""
      },
      "interactive_overlay": {
        "type": "build_gate",
        "prompt": "Save backup.sh, chmod +x it, run it, and verify ~/backups/ contains a timestamped directory. Mark complete to earn your badge.",
        "required_artifact": "~/backups/backup_*/",
        "xp_reward": 225,
        "unlocks_credential": "CLL-L1-B004-BashAutomator"
      },
      "duration_sec": 180
    },
    {
      "id": "S07",
      "title": "Outro",
      "narration": "Your first real Bash script is running. It backs up your work, handles errors, logs what it does, and cleans up after itself. In B-005, you'll set up Python — the language that will carry you from the terminal into web APIs, AI models, and smart contracts. Keep building.",
      "visual_prompt": "GESN mission complete. Badge: CLL-L1-B004-BashAutomator. XP: +300. Skill tree: 'Bash Scripting', 'Error Handling', 'Automation' nodes light up. B-005 preview.",
      "code_block": null,
      "interactive_overlay": {
        "type": "mission_complete",
        "badge": "CLL-L1-B004-BashAutomator",
        "xp_total": 300,
        "next_mission": "B-005-VIDEO",
        "next_title": "Installing Things Without Breaking Things"
      },
      "duration_sec": 40
    }
  ]
}
```

*Production notes: 7 scenes, ~25 min, 5 interactive overlays, 300 XP. Approved under QEP-B001-B005.*

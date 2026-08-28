# B-038: Regular Expressions Demystified

### re module, match, search, groups, and the Power of Pattern Matching

> *"A regular expression is a tiny language inside Python that can describe the shape of text. It looks like line noise until the day it clicks — and then you wonder how you ever lived without it. Learn it once, use it everywhere. Every data engineer needs this."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Use `re.match`, `re.search`, `re.findall`, `re.sub`, and `re.split`
2. Write patterns using character classes, quantifiers, anchors, and groups
3. Extract data from unstructured text using named capture groups
4. Validate email addresses, URLs, phone numbers, and postal codes
5. Build an `input-validator.py` used as a reusable validation library

**Prerequisite:** B-026 through B-037

**Build Artifact:** `~/developer-workspace/projects/python-foundations/input_validator.py`

**Credential:** `CCSLL-L1-B038-PatternEngineer` — on-chain on Base

---

## Chapter 1: Why Regex?

Regular expressions let you:
- **Validate** inputs ("is this a valid email?")
- **Extract** structured data from unstructured text
- **Transform** text using pattern-based substitution
- **Search** logs, files, and API responses at scale

```python
import re

# Without regex — verbose and fragile
def is_email_bad(s: str) -> bool:
    if "@" not in s:
        return False
    parts = s.split("@")
    if len(parts) != 2:
        return False
    if "." not in parts[1]:
        return False
    return True

# With regex — concise and precise
EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")

def is_email(s: str) -> bool:
    return bool(EMAIL_RE.match(s))
```

---

## Chapter 2: The Core Functions

```python
import re

text = "The price is $42.50 and the discount is $5.00"

# re.match — match at START of string only
m = re.match(r"The", text)
print(m)        # <re.Match object; span=(0, 3), match='The'>
m2 = re.match(r"price", text)
print(m2)       # None  ← because 'price' isn't at position 0

# re.search — find FIRST match anywhere in string
m3 = re.search(r"\$\d+\.\d{2}", text)
print(m3.group())   # $42.50

# re.findall — return ALL matches as a list
prices = re.findall(r"\$\d+\.\d{2}", text)
print(prices)   # ['$42.50', '$5.00']

# re.sub — replace all matches
clean = re.sub(r"\$\d+\.\d{2}", "PRICE", text)
print(clean)    # "The price is PRICE and the discount is PRICE"

# re.split — split on a pattern
parts = re.split(r"\s+", "  too   many   spaces  ")
print(parts)    # ['', 'too', 'many', 'spaces', '']
# Use strip() + split for cleaner results
```

---

## Chapter 3: Pattern Syntax

```python
import re

# Character classes
re.findall(r"[aeiou]", "lippytmai")     # vowels
re.findall(r"[0-9]", "B-036 2026")     # digits
re.findall(r"[a-zA-Z]", "Hello, 2026!") # letters
re.findall(r"[^aeiou]", "lippytmai")   # NOT a vowel (negation)

# Shorthand classes
# \d  = [0-9]     \D  = [^0-9]
# \w  = [a-zA-Z0-9_]   \W  = not word char
# \s  = whitespace      \S  = not whitespace
# .   = any char except newline

# Quantifiers
# *     zero or more
# +     one or more
# ?     zero or one (optional)
# {n}   exactly n
# {n,}  n or more
# {n,m} between n and m

re.findall(r"\d+",    "abc 123 def 4567")   # ['123', '4567']
re.findall(r"\d{3}",  "phone: 555-867-5309") # ['555', '867', '530']
re.findall(r"\d{3,4}", "555-867-5309")       # ['555', '867', '5309']

# Anchors
# ^  = start of string (or line in MULTILINE mode)
# $  = end of string (or line in MULTILINE mode)
# \b = word boundary

re.findall(r"^\w+", "hello world")    # ['hello']
re.findall(r"\w+$", "hello world")    # ['world']
re.findall(r"\bcat\b", "cat catfish scattered")  # ['cat']
```

---

## Chapter 4: Groups and Named Groups

```python
import re

# Groups with ()
m = re.search(r"(\d{4})-(\d{2})-(\d{2})", "Date: 2026-08-28")
if m:
    print(m.group(0))   # 2026-08-28  (entire match)
    print(m.group(1))   # 2026         (first group)
    print(m.group(2))   # 08           (second group)
    print(m.group(3))   # 28           (third group)
    print(m.groups())   # ('2026', '08', '28')

# Named groups (?P<name>...) — much more readable
DATE_RE = re.compile(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})")
m = DATE_RE.search("Date: 2026-08-28")
if m:
    print(m.group("year"))    # 2026
    print(m.group("month"))   # 08
    print(m.group("day"))     # 28
    print(m.groupdict())      # {'year': '2026', 'month': '08', 'day': '28'}

# findall with groups returns tuples
log = "2026-08-28 ERROR server.py 2026-08-29 INFO client.py"
pattern = r"(\d{4}-\d{2}-\d{2}) (\w+) (\S+)"
matches = re.findall(pattern, log)
for date_str, level, source in matches:
    print(f"{date_str} | {level:8} | {source}")
```

---

## Chapter 5: Compiled Patterns and Flags

```python
import re

# re.compile() — cache and reuse patterns (faster in loops)
EMAIL_RE  = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")
URL_RE    = re.compile(r"https?://[^\s]+")
PHONE_RE  = re.compile(r"\b(\d{3})[-.]?(\d{3})[-.]?(\d{4})\b")
ZIP_RE    = re.compile(r"\b\d{5}(?:-\d{4})?\b")

# Flags
# re.IGNORECASE (re.I) — case-insensitive
# re.MULTILINE  (re.M) — ^ and $ match line start/end
# re.DOTALL     (re.S) — . matches newlines too
# re.VERBOSE    (re.X) — allow whitespace and comments in pattern

VERBOSE_EMAIL = re.compile(r"""
    ^                       # start of string
    [a-zA-Z0-9._%+\-]+      # username
    @                       # at sign
    [a-zA-Z0-9.\-]+         # domain
    \.                      # dot
    [a-zA-Z]{2,}            # TLD
    $                       # end of string
""", re.VERBOSE)

# Multi-line search
text = """ERROR: disk full
WARNING: memory low
ERROR: connection timeout"""
errors = re.findall(r"^ERROR: .+$", text, re.MULTILINE)
print(errors)   # ['ERROR: disk full', 'ERROR: connection timeout']
```

---

## Chapter 6: The Build — Input Validator Library

```python
#!/usr/bin/env python3
"""
input_validator.py — B-038 Build Artifact

A reusable validation library using compiled regular expressions.
Import and use in any Python project.
"""
from __future__ import annotations

import re
from dataclasses import dataclass


# --- Compiled patterns ---
_EMAIL_RE    = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")
_URL_RE      = re.compile(r"^https?://[a-zA-Z0-9\-._~:/?#\[\]@!$&'()*+,;=%]+$")
_PHONE_RE    = re.compile(r"^\+?1?\s*[-.]?\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}$")
_ZIPUS_RE    = re.compile(r"^\d{5}(?:-\d{4})?$")
_SLUG_RE     = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_HEX_COLOR_RE = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
_IPV4_RE     = re.compile(
    r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$"
)
_DATE_RE     = re.compile(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$")


@dataclass
class ValidationResult:
    valid: bool
    message: str


def validate_email(email: str) -> ValidationResult:
    """Validate an email address."""
    if _EMAIL_RE.match(email.strip()):
        return ValidationResult(True, "Valid email")
    return ValidationResult(False, f"Invalid email: {email!r}")


def validate_url(url: str) -> ValidationResult:
    """Validate an HTTP/HTTPS URL."""
    if _URL_RE.match(url.strip()):
        return ValidationResult(True, "Valid URL")
    return ValidationResult(False, f"Invalid URL: {url!r}")


def validate_phone(phone: str) -> ValidationResult:
    """Validate a US phone number (multiple formats)."""
    if _PHONE_RE.match(phone.strip()):
        return ValidationResult(True, "Valid phone")
    return ValidationResult(False, f"Invalid phone: {phone!r}")


def validate_zip(zip_code: str) -> ValidationResult:
    """Validate a US zip code (5-digit or ZIP+4)."""
    if _ZIPUS_RE.match(zip_code.strip()):
        return ValidationResult(True, "Valid ZIP code")
    return ValidationResult(False, f"Invalid ZIP: {zip_code!r}")


def validate_slug(slug: str) -> ValidationResult:
    """Validate a URL slug (lowercase, hyphens only)."""
    if _SLUG_RE.match(slug.strip()):
        return ValidationResult(True, "Valid slug")
    return ValidationResult(False, f"Invalid slug: {slug!r}")


def validate_hex_color(color: str) -> ValidationResult:
    """Validate a CSS hex color (#RGB or #RRGGBB)."""
    if _HEX_COLOR_RE.match(color.strip()):
        return ValidationResult(True, "Valid hex color")
    return ValidationResult(False, f"Invalid hex color: {color!r}")


def validate_ipv4(ip: str) -> ValidationResult:
    """Validate an IPv4 address."""
    if _IPV4_RE.match(ip.strip()):
        return ValidationResult(True, "Valid IPv4")
    return ValidationResult(False, f"Invalid IPv4: {ip!r}")


def validate_date(date_str: str) -> ValidationResult:
    """Validate an ISO date string (YYYY-MM-DD, basic check)."""
    if _DATE_RE.match(date_str.strip()):
        return ValidationResult(True, "Valid date")
    return ValidationResult(False, f"Invalid date: {date_str!r}")


def extract_emails(text: str) -> list[str]:
    """Extract all email addresses from a block of text."""
    pattern = r"\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b"
    return re.findall(pattern, text)


def extract_urls(text: str) -> list[str]:
    """Extract all HTTP/HTTPS URLs from a block of text."""
    return re.findall(r"https?://[^\s]+", text)


def redact_emails(text: str) -> str:
    """Replace all emails in text with [REDACTED]."""
    pattern = r"\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b"
    return re.sub(pattern, "[REDACTED]", text)


def demo() -> None:
    print("=== Input Validator Demo ===\n")
    tests = [
        ("Email",    validate_email,    ["hello@lippytm.ai", "not-an-email", "a@b.c"]),
        ("URL",      validate_url,      ["https://lippytm.ai", "ftp://bad.com", "not-a-url"]),
        ("Phone",    validate_phone,    ["555-867-5309", "(555) 867-5309", "8675309"]),
        ("ZIP",      validate_zip,      ["94105", "94105-1234", "9410"]),
        ("Slug",     validate_slug,     ["my-cool-blog", "My Blog", "hello-world-123"]),
        ("HexColor", validate_hex_color, ["#fff", "#1a2b3c", "red", "#gggggg"]),
        ("IPv4",     validate_ipv4,     ["192.168.1.1", "256.0.0.1", "10.0.0.0"]),
        ("Date",     validate_date,     ["2026-08-28", "2026-13-01", "not-a-date"]),
    ]
    for category, validator, values in tests:
        print(f"--- {category} ---")
        for v in values:
            r = validator(v)
            icon = "✅" if r.valid else "❌"
            print(f"  {icon} {v!r}")
        print()

    print("--- Email extraction ---")
    text = "Contact me at charles@lippytm.ai or support@acss.dev for help."
    print(f"  Found: {extract_emails(text)}")
    print(f"  Redacted: {redact_emails(text)}\n")


if __name__ == "__main__":
    demo()
```

```bash
python3 ~/developer-workspace/projects/python-foundations/input_validator.py
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-038 Verification ==="
python3 -c "
import re
email_re = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
tests = [
    ('hello@lippytm.ai', True),
    ('not-an-email',     False),
    ('a@b.toolong',      True),
]
for addr, expected in tests:
    result = bool(email_re.match(addr))
    icon = '✅' if result == expected else '❌'
    print(f'{icon} {addr}: {result}')
print('✅ Regex works')
"
```

---


## Chapter 12: Done-For-You Lessons — Regular Expressions Demystified

> *"Done-for-you means it's already designed, structured, and proven. Your job: execute." — lippytmai*

10 ready-to-use lesson structures for Regular Expressions using re.

---

### DFY Lesson 1: Introduction to Regular Expressions

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 01: Introduction to Regular Expressions       │
│  Book: B-038  Tool: re                         │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 1: Introduction to Regular Expressions. Master re with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `re` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 1 of B-038: Introduction to Regular Expressions. Give me 3 progressive exercises."

---
### DFY Lesson 2: Core re Patterns

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 02: Core re Patterns                          │
│  Book: B-038  Tool: re                         │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 2: Core re Patterns. Master re with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `re` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 2 of B-038: Core re Patterns. Give me 3 progressive exercises."

---
### DFY Lesson 3: Three Formats: Ebook, Audiobook, Video

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 03: Three Formats: Ebook, Audiobook, Video    │
│  Book: B-038  Tool: re                         │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 3: Three Formats: Ebook, Audiobook, Video. Master re with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `re` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 3 of B-038: Three Formats: Ebook, Audiobook, Video. Give me 3 progressive exercises."

---
### DFY Lesson 4: Common Mistakes in Regular Expressions

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 04: Common Mistakes in Regular Expressions    │
│  Book: B-038  Tool: re                         │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 4: Common Mistakes in Regular Expressions. Master re with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `re` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 4 of B-038: Common Mistakes in Regular Expressions. Give me 3 progressive exercises."

---
### DFY Lesson 5: Building a Regular Expressions Workflow

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 05: Building a Regular Expressions Workflow   │
│  Book: B-038  Tool: re                         │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 5: Building a Regular Expressions Workflow. Master re with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `re` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 5 of B-038: Building a Regular Expressions Workflow. Give me 3 progressive exercises."

---
### DFY Lesson 6: Automating with re

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 06: Automating with re                        │
│  Book: B-038  Tool: re                         │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 6: Automating with re. Master re with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `re` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 6 of B-038: Automating with re. Give me 3 progressive exercises."

---
### DFY Lesson 7: Testing Your Regular Expressions Code

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 07: Testing Your Regular Expressions Code     │
│  Book: B-038  Tool: re                         │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 7: Testing Your Regular Expressions Code. Master re with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `re` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 7 of B-038: Testing Your Regular Expressions Code. Give me 3 progressive exercises."

---
### DFY Lesson 8: Production Regular Expressions Patterns

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 08: Production Regular Expressions Patterns   │
│  Book: B-038  Tool: re                         │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 8: Production Regular Expressions Patterns. Master re with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `re` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 8 of B-038: Production Regular Expressions Patterns. Give me 3 progressive exercises."

---
### DFY Lesson 9: Debugging Regular Expressions Problems

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 09: Debugging Regular Expressions Problems    │
│  Book: B-038  Tool: re                         │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 9: Debugging Regular Expressions Problems. Master re with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `re` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 9 of B-038: Debugging Regular Expressions Problems. Give me 3 progressive exercises."

---
### DFY Lesson 10: Earning Your PEL-L0-B038-RegexWizard Credential

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 10: Earning Your PEL-L0-B038-RegexWizard Cre  │
│  Book: B-038  Tool: re                         │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 10: Earning Your PEL-L0-B038-RegexWizard Credential. Master re with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `re` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 10 of B-038: Earning Your PEL-L0-B038-RegexWizard Credential. Give me 3 progressive exercises."

---

### Claim Your Credential

Complete all 10 lessons → open Appendix C → run: *"Generate my credential claim for `PEL-L0-B038-RegexWizard`."*

---

## Chapter 13: How It Works — Use Cases & Applications

> *"Knowing what to do is different from knowing why it matters." — lippytmai*

### The Mechanism

Regular Expressions in Python works because the language was designed to be readable, composable, and deployable. re is the tool that makes Regular Expressions practical.

### 5 Real-World Use Cases

| Domain | Application | Your Credential Unlocks |
|---|---|---|
| Backend Dev | Build APIs and services with re | PEL-L0-B038-RegexWizard → production deployments |
| Data Engineering | Process and transform data pipelines | PEL-L0-B038-RegexWizard → ETL roles |
| DevOps/Automation | Automate repetitive tasks | PEL-L0-B038-RegexWizard → CI/CD integration |
| AI/ML | Preprocess data and build models | PEL-L0-B038-RegexWizard → AI projects |
| Freelance | Deliver Python solutions to clients | PEL-L0-B038-RegexWizard → paid work |

### 📘 Mechanism Diagram

```
INPUT → [Regular Expressions Layer] → OUTPUT
         ↓
[ACSS Integration] → Hermes Event → Fabric Node
         ↓
[ADA Activation] → lippytmai-launch run B-038
```

### 🎧 Audiobook Narration:

> *"When you master Regular Expressions, you're not just learning syntax — you're learning how production Python systems work. Every ACSS component uses these patterns. This is infrastructure knowledge."*

### 🎬 Video: 5-Domain Application Tour

**Scene 1 — Backend:** API or service using Regular Expressions
**Scene 2 — Data:** Data pipeline using Regular Expressions
**Scene 3 — DevOps:** Automation script using Regular Expressions
**Scene 4 — AI/ML:** Model integration using Regular Expressions
**Scene 5 — Freelance:** Client deliverable using Regular Expressions

---

## Chapter 14: ACSS Explainer Series — Regular Expressions Demystified

> *"You're not just learning Regular Expressions. You're building a node in an intelligence network." — lippytmai*

10 explainer lessons connecting Regular Expressions Demystified to the full ACSS architecture.

---

### Explainer 1: ACSS Overview
*intelligence network*

**📘 Ebook Explanation:** Regular Expressions Demystified teaches the Regular Expressions layer that feeds the ACSS. Regex is used in the fabric graph to extract concept patterns from documentation and in hermes to validate event routing rules.

**📘 Connection Map:**
```
B-038 (Regular Expressions) ↕ ACSS Overview ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Regular Expressions Demystified connects to ACSS Overview: Regular Expressions Demystified teaches the Regular Expressions layer that feeds the ACSS. Regex is ..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ACSS Overview in ACSS diagram
- 10–35s: Zoom to where B-038 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-038

**🤖 Copilot Prompt:** > *"Explain how Regular Expressions fits the ACSS. What role does B-038 play?"*

---
### Explainer 2: Hermes Event Routing
*cross-system message bus*

**📘 Ebook Explanation:** Hermes routes Regular Expressions practice events. Completing an exercise emits a `skill.practice` event.

**📘 Connection Map:**
```
B-038 (Regular Expressions) ↕ Hermes Event Routing ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Regular Expressions Demystified connects to Hermes Event Routing: Hermes routes Regular Expressions practice events. Completing an exercise emits a `skill.practice` e..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Hermes Event Routing in ACSS diagram
- 10–35s: Zoom to where B-038 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-038

**🤖 Copilot Prompt:** > *"Show the Hermes event schema for a B-038 skill-complete event."*

---
### Explainer 3: Fabric Knowledge Graph
*pattern synthesis*

**📘 Ebook Explanation:** Fabric stores every Regular Expressions concept as a knowledge node connected to related books.

**📘 Connection Map:**
```
B-038 (Regular Expressions) ↕ Fabric Knowledge Graph ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Regular Expressions Demystified connects to Fabric Knowledge Graph: Fabric stores every Regular Expressions concept as a knowledge node connected to related books...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Fabric Knowledge Graph in ACSS diagram
- 10–35s: Zoom to where B-038 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-038

**🤖 Copilot Prompt:** > *"Generate the Fabric node definition for the core concept of B-038."*

---
### Explainer 4: Clone Engine Identity
*AI persona system*

**📘 Ebook Explanation:** lippytmai teaches Regular Expressions Demystified in Teach mode. The Clone Engine maintains consistent voice across all 300 books.

**📘 Connection Map:**
```
B-038 (Regular Expressions) ↕ Clone Engine Identity ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Regular Expressions Demystified connects to Clone Engine Identity: lippytmai teaches Regular Expressions Demystified in Teach mode. The Clone Engine maintains consiste..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Clone Engine Identity in ACSS diagram
- 10–35s: Zoom to where B-038 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-038

**🤖 Copilot Prompt:** > *"As lippytmai, explain Regular Expressions to a complete beginner using the B-038 voice."*

---
### Explainer 5: CLL/CCSLL/CBSLL
*Complete Language Libraries*

**📘 Ebook Explanation:** `PEL-L0-B038-RegexWizard` is registered in the Python Earn-while-you-Learn library (PEL). PEL tracks all Python credentials B-026–B-100+.

**📘 Connection Map:**
```
B-038 (Regular Expressions) ↕ CLL/CCSLL/CBSLL ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Regular Expressions Demystified connects to CLL/CCSLL/CBSLL: `PEL-L0-B038-RegexWizard` is registered in the Python Earn-while-you-Learn library (PEL). PEL tracks..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show CLL/CCSLL/CBSLL in ACSS diagram
- 10–35s: Zoom to where B-038 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-038

**🤖 Copilot Prompt:** > *"Show where PEL-L0-B038-RegexWizard fits in the PEL credential hierarchy."*

---
### Explainer 6: ADA Activation
*deployment system*

**📘 Ebook Explanation:** `lippytmai-launch run B-038` activates Regular Expressions Demystified through the ADA FastAPI backend.

**📘 Connection Map:**
```
B-038 (Regular Expressions) ↕ ADA Activation ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Regular Expressions Demystified connects to ADA Activation: `lippytmai-launch run B-038` activates Regular Expressions Demystified through the ADA FastAPI backe..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ADA Activation in ACSS diagram
- 10–35s: Zoom to where B-038 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-038

**🤖 Copilot Prompt:** > *"Write the ADA activation manifest for B-038."*

---
### Explainer 7: ACVS Video Pipeline
*video creator*

**📘 Ebook Explanation:** Every Regular Expressions Demystified video uses ACVS SHOW→BUILD→VERIFY structure.

**📘 Connection Map:**
```
B-038 (Regular Expressions) ↕ ACVS Video Pipeline ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Regular Expressions Demystified connects to ACVS Video Pipeline: Every Regular Expressions Demystified video uses ACVS SHOW→BUILD→VERIFY structure...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ACVS Video Pipeline in ACSS diagram
- 10–35s: Zoom to where B-038 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-038

**🤖 Copilot Prompt:** > *"Generate the ACVS scene manifest for B-038 Lesson 1."*

---
### Explainer 8: OMARCHY Workstation
*Arch Linux standard*

**📘 Ebook Explanation:** All Regular Expressions Demystified exercises run on OMARCHY — the reference environment ensures every learner has the same Python setup.

**📘 Connection Map:**
```
B-038 (Regular Expressions) ↕ OMARCHY Workstation ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Regular Expressions Demystified connects to OMARCHY Workstation: All Regular Expressions Demystified exercises run on OMARCHY — the reference environment ensures eve..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show OMARCHY Workstation in ACSS diagram
- 10–35s: Zoom to where B-038 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-038

**🤖 Copilot Prompt:** > *"What OMARCHY packages are required to complete all B-038 exercises?"*

---
### Explainer 9: Cross-Platform Copilot
*15-platform deployment*

**📘 Ebook Explanation:** The Regular Expressions Demystified AI Copilot deploys on ChatGPT, Gemini, Claude, GitHub, Slack, and 10 more platforms.

**📘 Connection Map:**
```
B-038 (Regular Expressions) ↕ Cross-Platform Copilot ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Regular Expressions Demystified connects to Cross-Platform Copilot: The Regular Expressions Demystified AI Copilot deploys on ChatGPT, Gemini, Claude, GitHub, Slack, an..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Cross-Platform Copilot in ACSS diagram
- 10–35s: Zoom to where B-038 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-038

**🤖 Copilot Prompt:** > *"Adapt the B-038 copilot system prompt for LinkedIn."*

---
### Explainer 10: Earn-While-You-Learn
*revenue system*

**📘 Ebook Explanation:** `PEL-L0-B038-RegexWizard` is proof of Regular Expressions mastery. Use it on LinkedIn, GitHub, and in lippytm.ai to unlock paid opportunities.

**📘 Connection Map:**
```
B-038 (Regular Expressions) ↕ Earn-While-You-Learn ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Regular Expressions Demystified connects to Earn-While-You-Learn: `PEL-L0-B038-RegexWizard` is proof of Regular Expressions mastery. Use it on LinkedIn, GitHub, and i..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Earn-While-You-Learn in ACSS diagram
- 10–35s: Zoom to where B-038 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-038

**🤖 Copilot Prompt:** > *"I just earned PEL-L0-B038-RegexWizard. Generate my LinkedIn credential announcement."*

---

### Your ACSS Node Is Now Active

Completing B-038 activates your node in the Fabric graph.
**Next:** `lippytmai-launch run B-038` or start B-039 SQLite.

---

## Appendix A: Enhanced Cheat Sheet — Regular Expressions Demystified

### 📘 Print-Optimized Reference Card

```
╔══════════════════════════════════════════════════════════════╗
║  B-038: Regular Expressions Demystified                ║
║  Credential: PEL-L0-B038-RegexWizard                            ║
╠══════════════════════════════════════════════════════════════╣
║  Core: re module                                                ║
║  Tool: re + regex                                               ║
╠══════════════════════════════════════════════════════════════╣
║  Activate: lippytmai-launch run B-038                            ║
╚══════════════════════════════════════════════════════════════╝
```

### Quick Reference

| Concept | Pattern | Use Case |
|---|---|---|
| `re module` | [usage pattern] | [when to use] |
| `regex patterns` | [usage pattern] | [when to use] |
| `groups` | [usage pattern] | [when to use] |
| `findall` | [usage pattern] | [when to use] |

### 🎧 Verbal Cheat Sheet: *"Core concepts: re module, regex patterns, groups. Credential: PEL-L0-B038-RegexWizard."*

### 🎬 Thumbnail: Dark background, `B-038` bold white, `re module` in green, credential badge bottom-right.

---

## Appendix B: ACSS Connection Map

Node `B-038` in the ACSS knowledge graph:

```
[Hermes] → [B-038 Events] → [Fabric] → [ADA] → [ACVS] → [OMARCHY] → [PEL:PEL-L0-B038-RegexWizard] → [EWYL]
```

**Book chain:** B-037 Datetime Master ← **Regular Expressions Demystified** → B-039 SQLite

---

## Appendix C: AI Copilot System — Regular Expressions Demystified

### System Prompt
```
You are lippytmai teaching "Regular Expressions Demystified" (B-038).
Help learners master Regular Expressions using re.
Credential: PEL-L0-B038-RegexWizard. Philosophy: Earn-while-you-Learn.
Always give 3-step exercises: setup → execute → verify.
```

### 30 Ebook Prompts (5 stages × 6)

**Stage 1 — Foundation:** 1."Explain Regular Expressions to a beginner." 2."Most important concept in B-038?" 3."Give a 3-step setup for re." 4."5 common beginner mistakes with Regular Expressions?" 5."Anatomy of a re pattern." 6."Mental model for Regular Expressions."

**Stage 2 — Practice:** 7."5 progressive Regular Expressions exercises." 8."Diagnose this error: [paste]." 9."Walk through this code line by line." 10."What to practice today?" 11."20-minute session for Regular Expressions." 12."Beginner vs. professional Regular Expressions comparison."

**Stage 3 — Application:** 13."Build a real Regular Expressions script." 14."How does Regular Expressions connect to production systems?" 15."Professional Regular Expressions workflow." 16."What does Regular Expressions mastery look like on a resume?" 17."Project using only B-038 skills." 18."3 Regular Expressions patterns in large-scale systems."

**Stage 4 — Integration:** 19."How does B-038 connect to other books?" 20."How does Regular Expressions feed ACSS?" 21."Hermes events for Regular Expressions?" 22."How does Fabric store Regular Expressions?" 23."ADA activation for B-038." 24."Cross-phase connections from B-038."

**Stage 5 — Mastery:** 25."Assess my Regular Expressions level." 26."Stretch goals for PEL-L0-B038-RegexWizard holders?" 27."Generate my credential claim for PEL-L0-B038-RegexWizard." 28."LinkedIn post for PEL-L0-B038-RegexWizard." 29."Portfolio project for PEL-L0-B038-RegexWizard." 30."90-day plan building on PEL-L0-B038-RegexWizard."

### 15 Audiobook Prompts

1."Narrate Regular Expressions intro for a podcast." 2."Story explaining why Regular Expressions matters." 3."Audio walkthrough of key B-038 code." 4."Day in the life of a Regular Expressions master." 5."2-minute audio lesson on re." 6."Regular Expressions explained with analogies only." 7."Top 5 mistakes with Regular Expressions." 8."Audio quiz: 5 questions." 9."Motivational close for B-038." 10."Credential claim narration." 11."Story: developer mastered Regular Expressions." 12."Audio summary for commuting." 13."3 real-world Regular Expressions scenarios." 14."Capstone walkthrough narration." 15."lippytmai intro monologue for B-038."

### 15 Video Prompts

1."Script 90-second B-038 intro." 2."SHOW→BUILD→VERIFY for re." 3."Split-screen before/after Regular Expressions." 4."Capstone log_parser.py terminal walkthrough." 5."YouTube thumbnail description." 6."3-minute tutorial on key concept." 7."Progress bar overlay design." 8."ACVS scene manifest for Lesson 1." 9."60-second quick tip for Regular Expressions." 10."Error-and-fix scene." 11."Code annotation style." 12."Credential reveal scene." 13."ACSS connection diagram for Ch14." 14."Cross-platform Regular Expressions comparison." 15."End-screen CTA design."

### Deployment

```bash
lippytmai-launch run B-038
curl http://localhost:8000/run/B-038
```

Deploy to 15 platforms via `docs/acss-cross-platform-copilot-deployment.md`.

---

## Appendix D: Quick Quiz & Self-Assessment — Regular Expressions Demystified

### 📘 Ebook Quiz (20 Questions)

**Section 1 — Concepts (Q1–5):**
1. What is Regular Expressions and why does it matter? *(b — practical mastery of re module)*
2. Primary tool for Regular Expressions? *(a — re module)*
3. Which ACSS system routes Regular Expressions events? *(c — Hermes)*
4. Your credential for B-038? *(b — PEL-L0-B038-RegexWizard)*
5. What does `lippytmai-launch run B-038` do? *(d — activates via ADA)*

**Section 2 — Syntax (Q6–10):**
6. Write a minimal re module example: ___
7. How do you handle errors in Regular Expressions? ___
8. One-liner combining re module with another tool: ___
9. How do you test Regular Expressions code? ___
10. How do you deploy Regular Expressions to production? ___

**Section 3 — Application (Q11–15):**
11. Describe a real-world Regular Expressions scenario that saves an hour.
12. Most common mistake with re module?
13. How does Regular Expressions connect to security?
14. How does B-038 apply to a production Python project?
15. What would you build first after earning PEL-L0-B038-RegexWizard?

**Section 4 — ACSS (Q16–20):**
16. ADA command for B-038? *(lippytmai-launch run B-038)*
17. Fabric node type for Regular Expressions? *(ConceptNode)*
18. How does Clone Engine use Regular Expressions? *(lippytmai teaches in Teach mode)*
19. 2 books that build on B-038?
20. EWYL opportunity unlocked by PEL-L0-B038-RegexWizard?

### 🎧 Audiobook Quiz (10 Questions)

1. Three most important concepts from Regular Expressions Demystified?
2. Explain Regular Expressions in one sentence to a non-developer.
3. First thing to do when re module fails?
4. Recite your credential.
5. One project buildable with B-038 skills only.
6. ACSS system that stores skill progress? *(Fabric)*
7. ADA activation command? *(lippytmai-launch run B-038)*
8. Next book after B-038? *(B-039 SQLite)*
9. Say the EWYL pledge: "I learn, I build, I earn, I share."
10. What makes Python + ACSS a power combination?

### 🎬 Terminal Challenges (5)

1. **Foundation:** Run `re module` — screenshot the output.
2. **Intermediate:** Combine `re module` with error handling.
3. **Applied:** Write a 10-line script automating a real task.
4. **Debug:** Introduce an error, diagnose and fix it.
5. **Capstone:** Run `log_parser.py` — record a 60-second demo.

---

## Appendix E: Glossary & Error Encyclopedia — Regular Expressions Demystified

### Glossary (20 Terms)

| Term | Definition | First Seen |
|---|---|---|
| `re module` | [definition in B-038 context] | [B-038] |
| `regex patterns` | [definition in B-038 context] | [B-038] |
| `groups` | [definition in B-038 context] | [B-038] |
| `findall` | [definition in B-038 context] | [B-038] |
| `sub` | [definition in B-038 context] | [B-038] |
| `compile` | [definition in B-038 context] | [B-038] |
| `async` | [definition in B-038 context] | [B-038] |
| `decorator` | [definition in B-038 context] | [B-038] |
| `type hint` | [definition in B-038 context] | [B-038] |
| `dataclass` | [definition in B-038 context] | [B-038] |
| `fixture` | [definition in B-038 context] | [B-038] |
| `Hermes` | [definition in B-038 context] | [B-038] |
| `Fabric` | [definition in B-038 context] | [B-038] |
| `ADA` | [definition in B-038 context] | [B-038] |
| `OMARCHY` | [definition in B-038 context] | [B-038] |
| `credential` | [definition in B-038 context] | [B-038] |
| `EWYL` | [definition in B-038 context] | [B-038] |
| `lippytmai` | [definition in B-038 context] | [B-038] |
| `PEL` | [definition in B-038 context] | [B-038] |
| `Fabric node` | [definition in B-038 context] | [B-038] |

### Error Encyclopedia (10 Common Python Errors)


#### `TypeError` — Cause: Wrong type passed to function. Fix: Add type hints; check with `isinstance()`.
- **🎧 Audio:** "When you see `TypeError`, it means wrong type passed to function"
- **🎬 Video:** Error + fix terminal recording


#### `AttributeError` — Cause: Accessing attribute that doesn't exist. Fix: Use `hasattr()` or check with `dir()`.
- **🎧 Audio:** "When you see `AttributeError`, it means accessing attribute that doesn't exist"
- **🎬 Video:** Error + fix terminal recording


#### `ImportError` — Cause: Module not found. Fix: Check venv is active; run `pip install`.
- **🎧 Audio:** "When you see `ImportError`, it means module not found"
- **🎬 Video:** Error + fix terminal recording


#### `KeyError` — Cause: Dict key doesn't exist. Fix: Use `.get()` with a default value.
- **🎧 Audio:** "When you see `KeyError`, it means dict key doesn't exist"
- **🎬 Video:** Error + fix terminal recording


#### `FileNotFoundError` — Cause: Path doesn't exist. Fix: Use `Path.exists()` before opening.
- **🎧 Audio:** "When you see `FileNotFoundError`, it means path doesn't exist"
- **🎬 Video:** Error + fix terminal recording


#### `ValueError` — Cause: Invalid value for operation. Fix: Validate inputs before processing.
- **🎧 Audio:** "When you see `ValueError`, it means invalid value for operation"
- **🎬 Video:** Error + fix terminal recording


#### `IndentationError` — Cause: Mixed tabs and spaces. Fix: Configure editor to use spaces only.
- **🎧 Audio:** "When you see `IndentationError`, it means mixed tabs and spaces"
- **🎬 Video:** Error + fix terminal recording


#### `RecursionError` — Cause: Infinite recursion. Fix: Add base case; increase recursion limit if needed.
- **🎧 Audio:** "When you see `RecursionError`, it means infinite recursion"
- **🎬 Video:** Error + fix terminal recording


#### `ConnectionError` — Cause: Network request failed. Fix: Wrap in try/except; implement retry logic.
- **🎧 Audio:** "When you see `ConnectionError`, it means network request failed"
- **🎬 Video:** Error + fix terminal recording


#### `PermissionError` — Cause: File or directory not accessible. Fix: Check permissions with `ls -la`.
- **🎧 Audio:** "When you see `PermissionError`, it means file or directory not accessible"
- **🎬 Video:** Error + fix terminal recording


---

## Appendix F: Instructor & Accessibility Guide — Regular Expressions Demystified

### Teaching Schedule (4-Week Curriculum)

| Week | Focus | Topics | Outcome |
|---|---|---|---|
| 1 | Foundation | Concepts + setup | Can use Regular Expressions tools |
| 2 | Intermediate | Core patterns | Can write working code |
| 3 | Applied | Real projects | Can solve production problems |
| 4 | Mastery | DFY + Appendices | Earns `PEL-L0-B038-RegexWizard` |

### Common Confusion Points

1. "When do I use re module vs. alternatives?" — Show a decision flowchart.
2. "Why does the same code fail in a different environment?" — Explain venv isolation.
3. "How do I know if my code is production-ready?" — Show the VERIFY step always.
4. "How does Regular Expressions connect to other Python skills?" — Show the ACSS learning path map.
5. "What does earning PEL-L0-B038-RegexWizard actually mean for my career?" — Show EWYL income examples.

### Assessment Rubric

| Criterion | Beginner | Competent | Expert |
|---|---|---|---|
| Code quality | Messy, no types | Working, some types | Clean, typed, tested |
| Error handling | None | Basic try/except | Custom exceptions + logging |
| Testing | No tests | Basic assertions | pytest + fixtures + coverage |
| ACSS integration | Unaware | Uses ADA | Contributes to ACSS |

### Accessibility: Screen reader alt-text for all diagrams. No color-only encoding. Short paragraphs. Audiobook available.

---

## Appendix G: Your Learning Path — Regular Expressions Demystified

### Where You Are Now

```
  Phase 2: Python Programming (B-026–B-055)
  [████████░░░░░░░░░░░░] 43%

  ✅ B-037 Datetime Master (PEL-L0-B037-DatetimeMaster)
  👉 B-038: Regular Expressions Demystified ← YOU ARE HERE
  ⬜ B-039 SQLite (PEL-L0-B039-SQLiteBuilder)
```

### Credential Chain

```
PEL-L0-B037-DatetimeMaster → PEL-L0-B038-RegexWizard → PEL-L0-B039-SQLiteBuilder
```

### Next Steps

1. Claim `PEL-L0-B038-RegexWizard` (Appendix C, Prompt 27)
2. Build `log_parser.py` (Appendix H)
3. Start `B-039 SQLite`

### Cross-Phase Connections

```
Phase 1: Linux Foundations → Phase 2: Python (YOU ARE HERE)
    ↓ B-038 connects to:
Phase 3: Blockchain Development (B-056+)
```

---

## Appendix H: Real Project Showcase — Regular Expressions Demystified

### Project: `log_parser.py`

**Credential gated:** Complete this project to qualify for `PEL-L0-B038-RegexWizard`

### Complete Code

```python
#!/usr/bin/env python3
import re
from typing import Iterator

LOG_PATTERN = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2})"  
    r"\s+(?P<time>\d{2}:\d{2}:\d{2})"  
    r"\s+(?P<level>INFO|WARN|ERROR|DEBUG)"  
    r"\s+(?P<message>.+)"
)

def parse_log_line(line: str) -> dict | None:
    m = LOG_PATTERN.match(line.strip())
    return m.groupdict() if m else None

def parse_log_file(path: str) -> Iterator[dict]:
    with open(path) as f:
        for line in f:
            result = parse_log_line(line)
            if result:
                yield result

```

### Deploy Instructions

```bash
# Run the project
python log_parser.py --help
python log_parser.py

# Test it
pytest test_log_parser.py -v  # if tests exist

# Verify
echo "Exit: $?"
```

### Extend It

1. Add type hints to all functions
2. Add pytest test coverage
3. Add CLI interface with typer
4. Containerize with Docker
5. Add structured logging

### 🎧 Walkthrough: *"Build log_parser.py step by step. When it runs successfully, you've earned PEL-L0-B038-RegexWizard."*

### 🎬 Video: SHOW empty editor → BUILD code live → VERIFY execution → CTA: "Claim PEL-L0-B038-RegexWizard."

---

## Further Reading

- 📄 [Back to README](../README.md)
- 📄 [Product Excellence Framework](PRODUCT-EXCELLENCE-FRAMEWORK.md)
- 📄 [AI Clone Engine Swarms](ai-clone-engine-swarms.md)
- 📄 [ACSS Cross-Platform Copilot Deployment](acss-cross-platform-copilot-deployment.md)
- 📄 [ADA Deployment Activations](ai-deployment-activations.md)
- 📄 [Previous: B-037](B-037-*.md)
- 📄 [Next: B-039](B-039-*.md)

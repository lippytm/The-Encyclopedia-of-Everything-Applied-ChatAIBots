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

## Further Reading

- 📄 [`docs/B-036-type-hints-making-python-honest.md`](B-036-type-hints-making-python-honest.md) — Type annotations for validators
- 📄 [`docs/B-032-the-internet-in-a-function.md`](B-032-the-internet-in-a-function.md) — Validating API request data
- 📄 [`docs/B-040-automation-scripts-that-save-hours.md`](B-040-automation-scripts-that-save-hours.md) — Regex in file renaming
- 🏠 [`README.md`](../README.md) — Encyclopedia home

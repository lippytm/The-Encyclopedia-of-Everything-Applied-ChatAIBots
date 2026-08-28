# DFY Illustration System

## Visual Layer for All 550 Done-For-You Lessons

> *"A diagram explains in 3 seconds what a paragraph takes 30 seconds to read. A screencast makes a complex task trivially clear. An audiobook callout burns the mental model into memory. All three together — that's the lippytm.ai illustration layer."*

---

## The Three-Format Illustration Standard

Every DFY lesson in the lippytm.ai curriculum ships with **three synchronized illustrations** — one for each learning format:

| Format | Illustration Type | Purpose |
|---|---|---|
| **📘 Ebook** | Annotated diagram, ASCII art, table, or code flow figure | Visual reference anchored to the written lesson |
| **🎧 Audiobook** | Spoken "Mental Model Callout" — describes the visual in words | Makes the concept vivid without a screen |
| **🎬 Video Tutorial** | Scene description: terminal recording, animated diagram, or annotated screenshot | Shows the exact artifact being built, frame by frame |

---

## Ebook Illustration Types

| Type | When to Use | Format |
|---|---|---|
| **Flow Diagram** | Multi-step process (pipelines, deployment flows) | ASCII block arrows `→` |
| **Comparison Table** | Two approaches side-by-side (sync vs async, old vs new) | Markdown table |
| **Annotated Code Block** | Code with inline `# ← explanation` comments | Fenced code block |
| **File/Directory Tree** | Project structure, filesystem layout | `tree`-style indented text |
| **Architecture Map** | System components and their relationships | ASCII box diagram |
| **Before/After Split** | Showing the problem and the fix | Two fenced blocks |
| **Checklist Visual** | Step-by-step verification | Emoji ✅ / ❌ checklist |
| **Data Flow Map** | How data moves through a script | `input → process → output` ASCII |

---

## Audiobook Callout Script Standard

Every audiobook callout follows this structure:

```
[CALLOUT TONE — 1 bell sound]
"Done-For-You Moment. Lesson {N}: {Title}.

Imagine {mental model description — 2-3 sentences max}.

Your deliverable is: {exact artifact name}.
Time to build: {N minutes}.

Pause here. Build it. Then resume."
[CALLOUT TONE — 2 bell sounds]
```

**Voice identity:** `lippytmai` (calm, confident, encouraging — never rushed)
**Callout tone:** Distinct from chapter narration — learner knows to act, not just listen

---

## Video Tutorial Scene Standard

Every video DFY scene follows the **SHOW→BUILD→VERIFY** structure:

| Frame | Duration | Content |
|---|---|---|
| **SHOW** | 0–20 sec | Show the finished artifact running — the "what you'll have" moment |
| **BUILD** | 20 sec – (N-1 min) | Live terminal or editor recording — build it from scratch |
| **VERIFY** | Last 30 sec | Run the finished artifact, show output, confirm it works |

**Recording standard:**
- Terminal: `80×24`, `JetBrains Mono 16pt`, dark background (OMARCHY palette)
- Cursor: blinking, visible — never hidden
- Typing speed: deliberate, not rushed — learner can follow along
- Mistakes: leave them in and fix them — shows real workflow
- Annotations: yellow `→` callout arrows for key lines

---

## ACSS Integration for Illustrations

```
Illustration Production Flow:
  DFY Lesson defined (type, deliverable)
       ↓
  lippytmai generates 3 illustration specs
       ↓
  Hermes event: ILLUS:{book_id}:{lesson}:READY
       ↓
  Fabric records: FabricIllusNode(book, lesson, ebook_fig, audio_callout, video_scene)
       ↓
  ADA stores: illustration assets linked to book entry
       ↓
  Clone Engine: lippytmai narrates audiobook callout
```

---

## Illustration Files in This Repository

| File | Books | Illustrations |
|---|---|---|
| [`DFY-ILLUSTRATIONS-B001-B025-phase1.md`](DFY-ILLUSTRATIONS-B001-B025-phase1.md) | B-001–B-025 | 750 (250 lessons × 3 formats) |
| [`DFY-ILLUSTRATIONS-B026-B055-phase2.md`](DFY-ILLUSTRATIONS-B026-B055-phase2.md) | B-026–B-055 | 900 (300 lessons × 3 formats) |

**Total illustration specs (Phases 1–2): 1,650**

---

## Quality Standards

- **Every ebook figure** must be renderable in plain Markdown — no external image dependencies
- **Every audiobook callout** must work as standalone audio without any visual reference
- **Every video scene** must be completable by a learner watching once at 1× speed
- **Consistency:** same artifact built in all 3 formats — learner can switch formats mid-lesson

---

## Further Reading

- 📄 [`docs/DFY-LESSONS-SYSTEM.md`](DFY-LESSONS-SYSTEM.md) — DFY lesson system overview
- 📄 [`docs/DFY-ILLUSTRATIONS-B001-B025-phase1.md`](DFY-ILLUSTRATIONS-B001-B025-phase1.md) — Phase 1 illustration specs
- 📄 [`docs/DFY-ILLUSTRATIONS-B026-B055-phase2.md`](DFY-ILLUSTRATIONS-B026-B055-phase2.md) — Phase 2 illustration specs
- 📄 [`docs/ai-copilot-video-sandbox-creator.md`](ai-copilot-video-sandbox-creator.md) — ACVS video production pipeline
- 📄 [`docs/creative-building-process.md`](creative-building-process.md) — 8-stage creative loop
- 🏠 [`README.md`](../README.md) — Encyclopedia home

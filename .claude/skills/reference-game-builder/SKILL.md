---
name: reference-game-builder
description: "Use when making reference-matched PPTX and HTML games."
version: 1.0.0
author: Reference Game Builder contributors
license: MIT
---

# Reference-matched PowerPoint and HTML games

Build a playable educational presentation from a video reference, then produce a visually faithful standalone HTML edition when requested. Preserve the requested file format and the reference's visual identity. This skill is provider-independent and works as a Claude Code project or personal skill.

## When to Use

- Recreating a cinematic classroom quiz, character-themed presentation, clickable selection board or game-like PowerPoint.
- Porting an approved PowerPoint to an offline HTML game without redesigning it.
- Producing matching PPTX/HTML editions with shared artwork, questions and animation assets.

## Non-negotiables

1. **Deliver the requested medium.** A `.pptx` request requires an actual PowerPoint. HTML is a separate output, not a substitute unless explicitly approved.
2. **Match the reference before adding features.** Reproduce its scene, character scale, prop layout, color, typography, navigation and transition beats. A generic quiz with scores and timers is not a visual clone.
3. **Inspect the video itself.** Download when permitted, extract a contact sheet, then inspect full-resolution frames. Captions and thumbnails do not prove the interaction mechanics.
4. **Keep editable text separate from generated artwork.** Generate scenes, characters and blank props, not finished slides with baked-in questions.
5. **Do not invent capabilities.** Macro-free slide links do not maintain a persistent score. A PDF render does not prove native PowerPoint animation playback.
6. **Do not assume image-generation access.** Use an available authorised image tool, or ask for supplied/exported images. Do not describe images as generated unless actual outputs exist. Do not incur unapproved paid generation.
7. Do not upload, publish or use third-party accounts unless the user explicitly requests it. Never package credentials, original machine paths or private operator data.

## Before building

Record a short acceptance brief:

- output: PPTX, HTML, or both;
- primary reference and any secondary references;
- language, aspect ratio and target viewing device;
- flow, question types/count, feedback and navigation;
- visual elements that must be preserved;
- editable fields and any deliberate differences;
- what can be verified locally versus what requires a native application.

If supplied with the accompanying example bundle, inspect `source/crash-powerpoint/`, `source/crash-html/`, `README.md` and `CLAUDE.md` before editing. Work in a copy. The example is an eight-question implementation, not a generic arbitrary-length engine.

## Workflow

### 1. Reverse-engineer the reference

Use `yt-dlp` when the public platform permits access, `ffprobe` for media facts, and `ffmpeg` for contact sheets. A practical first pass is one frame every 1–3 seconds. Inspect close-ups of the menu, question, answer feedback and edit view. Record observed behavior separately from inferred implementation.

Make a scene list such as:

`intro → title → portal → eight-crate menu → question → answer feedback → menu → closing`

Treat a second video supplied as additional insight as supplemental, not permission to replace the first reference's layout.

### 2. Build a reusable asset kit

Read [references/assets-and-motion.md](references/assets-and-motion.md) and [references/image-prompts.md](references/image-prompts.md).

Generate full-screen backgrounds with empty UI space, a character cutout if needed, and a separate prop sheet. Prefer transparent assets; otherwise use a flat key color absent from the foreground. Crop/key the actual generated output, inspect its real dimensions and check edges. Never assume the requested image size equals the returned size.

Render short cinematic clips only where they improve fidelity. A useful lightweight method is Three.js for real 3D crates/portal geometry plus a generated character billboard. This is not a fully rigged 3D character. Render deterministic frames with Playwright, encode H.264/yuv420p MP4 with faststart, and extract poster frames.

### 3. Build the native PowerPoint

Read [references/native-powerpoint.md](references/native-powerpoint.md).

Use `python-pptx` or a comparable native authoring library. Use separate pictures and native text boxes. For reliable macro-free feedback, create linked answer-state slides. Apply native transitions/entrance effects through PresentationML where the library lacks a high-level API. Embed video and audio bytes; include explicit skip/home links.

Build all slides before resolving internal links. Add teacher notes explaining correct answers, edit requirements and compatibility. Do not silently flatten every slide into an image.

### 4. Build a faithful HTML edition

Read [references/offline-html.md](references/offline-html.md).

Reuse the approved PowerPoint asset kit and question bank. Use a fixed-ratio landscape stage with a deliberate portrait layout. Embed media as data URLs for a single-file offline deliverable. Add guarded state transitions, optional sound, completed-question protection and a lightweight question editor where requested.

An HTML edition may add local save/resume, but those capabilities must not be attributed to the PPTX edition.

### 5. Verify the actual outputs

Read [references/verification-and-sharing.md](references/verification-and-sharing.md).

- PPTX: reopen package, validate links/media/timing targets, render every slide through an office engine, inspect and fix visual issues, then test native PowerPoint playback when available.
- HTML: open the actual `file://` artifact with HTTP(S) blocked, play a full game, test both media clips, wrong/correct paths, repeated actions, persistence, editor/export and mobile geometry.
- Reopen a customised HTML export in a fresh path/context. It must contain the new questions and all assets, not the old session.
- Report tested and untested boundaries honestly. Keep a local preview as evidence, not as a replacement for the requested artifact.

## Shared question data

Use one UTF-8 JSON bank for both builds. In the accompanying kit it is `source/crash-powerpoint/questions.json`:

```json
{
  "text": "Question text; a newline may separate two lines",
  "options": ["First answer", "Second answer", "Third answer"],
  "correct": 1,
  "explanation": "Why the second answer is correct",
  "category": "Subject"
}
```

`correct` is zero-based. The included layout supports exactly eight questions, each with two or three choices. To change the count or allowed choices, update layout, validation, navigation, completion logic and tests together.

## Definition of done

- Requested native/HTML files exist and open.
- The result matches the reference rather than just its feature list.
- Editable text, navigation and embedded media are real.
- A complete game path was exercised where the runtime exists.
- At least one visual fix-and-recheck cycle was performed.
- Limitations, ownership of third-party characters/assets and verification boundaries are stated without exaggeration.

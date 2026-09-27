# Working on this game kit

Read `.claude/skills/reference-game-builder/SKILL.md` before changing the project. The skill has references for image generation, assets/motion, native PPTX, offline HTML, and verification/sharing.

## Source of truth

- Questions: `source/crash-powerpoint/questions.json`.
- Prepared shared assets: `source/crash-powerpoint/assets/`.
- Raw generated inputs: `source/crash-powerpoint/raw-assets/`.
- PowerPoint generator: `source/crash-powerpoint/build_deck.py`.
- HTML source: `source/crash-html/template.html`.
- Build both: `python scripts/build_all.py`.
- Check both: `python scripts/check_all.py`.

Do not directly edit the huge embedded-data HTML if the editable template/build path is available. Do not edit only a single PPTX feedback copy when regenerating can update all states consistently. Preserve the original example in a copy before a redesign.

## Product constraints

A requested PowerPoint must remain a real `.pptx`. If both outputs are requested, preserve the same scene, props, character placement and question content across both. Do not replace the theme with a generic dashboard or invent automatic scores in the macro-free PPTX. The HTML can have its own explicitly described persistence.

## Execution and verification

Use the included assets first; rebuilding does not require image generation. New image generation depends on an authorised tool or manual image inputs. Do not claim access to a tool that is not configured and do not incur unapproved costs.

Run relevant tests, render/inspect the outputs and state what you actually verified. PowerPoint XML validation and LibreOffice rendering do not prove Microsoft slideshow playback. Do not weaken tests just to get green; update fixed-answer fixtures when intentionally changing the bank while retaining equivalent behavioral checks.

Keep third-party licences. Never bundle credentials, browser state, original-machine paths or proprietary fonts. No public uploads, deployments or account operations without a specific user request.

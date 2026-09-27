# Contributing

## Setup

Follow README.md to install Python dependencies and Playwright Chromium. Node.js is required for JavaScript syntax checks; image generation is not required. Prepared artwork and clips are committed for reproducible builds.

## Change the game

- Edit `source/crash-powerpoint/questions.json` for the shared question bank.
- Edit `source/crash-powerpoint/build_deck.py` for native PowerPoint layout/navigation.
- Edit `source/crash-html/template.html` for browser behavior/layout. Do not edit generated embedded-data HTML directly.
- Keep the requested format and approved visual design. Label deliberate differences between formats.
- Do not redistribute proprietary fonts or imply ownership of third-party characters.

## Before a pull request

```bash
python scripts/build_all.py
python scripts/check_all.py
python scripts/audit_bundle.py --tracked
```

Visually inspect changed screens too. Tests check the real browser game and PPTX structure, not live Microsoft PowerPoint. Test the actual PowerPoint application when changing media, timing or links, or explicitly report that boundary as untested.

The audit is a bounded check for common secret patterns and local paths, not a guarantee that arbitrary content is safe to publish. Review every added asset/document and never commit `.env`, credentials or browser state.

## Release

Generated standalone files are Git-ignored, not committed repeatedly. Stage intended source changes before local packaging, because the packager selects tracked source files.

```bash
python scripts/package_release.py
```

This creates `dist/Crash-Game-Kit.zip` (source, skill and built files), verifies its manifest in a fresh extraction, and writes `dist/SHA256SUMS.txt`. Review changes, commit, push `main`, then create/push a version tag such as `v1.0.0`. The GitHub workflow rebuilds, tests and packages that exact tag before publishing a release. Do not claim a release passed until its workflow and downloadable assets are verified.

No secrets are needed by build/test jobs. Only the tag-release job gets repository content-write permission through GitHub's built-in token. Fork pull requests cannot publish releases.

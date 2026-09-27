# Verification and sharing

## Two outputs, two verification boundaries

**PowerPoint:** package integrity, relationship/animation checks and office rendering are required. Native PowerPoint slideshow testing is separate. If the application is unavailable, say so. Do not claim a LibreOffice PDF or an assembled preview proves Microsoft media playback.

**HTML:** test the delivered single file, not just a local server. Block HTTP(S), confirm videos actually advance, play every question and reopen an edited export. Test desktop and portrait geometry; do not equate emulation with a physical-phone test.

## Portable rebuild

In the example bundle, `scripts/build_all.py` runs the native deck and HTML builds and copies outputs to `deliverables/`. Both consume `source/crash-powerpoint/questions.json`. The already-prepared asset kit means recipients can rebuild without an image-generation service or rerendering videos.

Use `scripts/check_all.py` for the provided five PPTX and eight HTML tests. The tests are regression fixtures for the original eight-question bank. If the bank changes, preserve behavioral coverage while updating answer-specific fixture expectations.

Optional layers:

- regenerate keyed assets from the included raw image outputs;
- rerender WebGL clips with Playwright and ffmpeg;
- export the deck to PDF with an installed office engine;
- inspect resulting slide/browser screenshots;
- verify actual PowerPoint playback on an available desktop.

## Export boundary

Build the public bundle in a separate directory. Include only the explicitly requested deliverables, portable source, documentation, generated artwork and libraries/licenses needed to reproduce the example. Do not copy `.git`, browser profiles, login state, API credentials, source-machine caches, raw chat logs, private screenshots, databases or user-specific configuration.

Scrub both text files and ZIP-contained Office XML metadata. Remove creator/last-editor identity where not intended for sharing. Convert hardcoded executable paths to PATH lookup and raw asset paths to bundle-relative paths or explicit arguments. Do not redistribute proprietary fonts.

The example contains third-party character/brand imagery. Document that this does not grant a commercial licence. The shared skill explains a reusable workflow; use original characters or properly licensed assets for resale.

## Archive and upload

1. Audit the staging tree for private paths and secret-shaped values.
2. Run builds/tests from the portable tree.
3. Produce a manifest of files, sizes and SHA-256 hashes.
4. Create the ZIP without runtime caches or tool environments.
5. Extract the actual archive into a fresh directory; verify manifest, audit again, rebuild and rerun the tests there.
6. Only then upload through the authorised sharing service.
7. Keep any returned management/guest token in a private local receipt, never in the public archive or chat.
8. Read the exact uploaded target back. Prefer a fresh public download and checksum comparison, not merely an upload success response.
9. Give the user a public download link plus a local attachment fallback. Explain free-host retention uncertainty; never promise permanent storage.

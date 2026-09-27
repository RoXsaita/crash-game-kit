# Verification record and boundaries

## Executed successfully during packaging

- Created a fresh Python virtual environment and installed the pinned requirements.
- Rebuilt both deliverables from the portable source and included prepared assets.
- Ran five PPTX tests: native editable content, crate destinations, answer-state navigation, internal package/animation targets, and embedded media/timing/navigation properties.
- Ran eight HTML browser tests: actual embedded clip playback, complete game, retries/keyboard, progress/reset, editable export reopening, portrait layout, feedback/control separation, and fullscreen/audio toggle/duplicate protection.
- Audited public text and Office XML for private workstation markers and secret-shaped values.
- Inspected/repaired author metadata so the shared file does not carry the original operator identity or the authoring library's default last-editor name.

The original game-development pass also office-rendered all 36 slides, inspected full-size samples and contact sheets, decoded the embedded and preview videos, and visually checked desktop/portrait HTML. The provided screenshots come from those real output files, not invented UI.

## Meaning of these results

PowerPoint tests check file structure and link/media wiring. They do not exercise live Microsoft PowerPoint playback. Office rendering was performed with LibreOffice. Native PowerPoint, Keynote, Google Slides, physical iOS/Android devices and Windows builds were not executed in this environment.

HTML tests use real Chromium on the local-file path with HTTP(S) requests blocked. Portrait tests emulate a phone viewport; they are not physical-device tests. The sound toggle is tested, not a subjective loudspeaker listening review.

The example's 3D intro contains real rendered cubes and a character billboard, not a fully rigged character. The portal is a real procedural 3D/shader scene. Their prebuilt media is bundled, so normal rebuilds do not rerender frames or require an image service.

## Check your extracted copy

For a release ZIP (not a Git checkout), verify the archive manifest before building:

```bash
python scripts/audit_bundle.py --manifest
```

In a Git checkout, after installing requirements and Chromium:

```bash
python scripts/build_all.py
python scripts/check_all.py
python scripts/audit_bundle.py --tracked
```

A rebuild creates additional generated files and can change Office ZIP metadata, so exact manifest checks are meant for the untouched extracted archive, not a modified working tree.

For a production classroom delivery, open the PPTX in the actual target PowerPoint version and run the intro → menu → question → correct/wrong → home path. Test mobile delivery on the real device/browser if that is the intended audience.

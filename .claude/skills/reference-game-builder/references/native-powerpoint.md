# Native PowerPoint implementation

## Package structure and slide graph

Use a real Open XML `.pptx` package. The worked example uses Python `python-pptx`, editable native text boxes, reusable PNG/JPEG props, WAV transition sounds and embedded MP4 clips.

The slide graph is:

- `INTRO` with embedded studio clip and skip link;
- `TITLE` with a start link;
- `PORTAL` with embedded tunnel clip and skip link;
- `MENU` with eight crate links;
- `Q01` through `Q08`, plus one `Qxx_Ay` state per answer;
- `FINISH` and `TEACHER`.

Six three-choice and two two-choice questions produce 36 total slides including the surrounding screens. This implementation uses **linked feedback states**, not on-click reveal triggers or macros. When an option is selected, its link opens a visually identical state with the appropriate feedback. Wrong states keep the answer links available. Fruit returns to the menu.

This approach is reliable and editable, but manually changing a question requires updating its related states too. The provided generator loads a shared question JSON and updates all states consistently. Do not promise persistent team scores or used-crate tracking in this macro-free deck.

## Geometry and editable text

Use 16:9, approximately 13.3333×7.5 inches. Keep the left character region clear, place a large hanging sign in the upper right, and place three wooden answer planks vertically below it. Place a separate fruit navigation image near the bottom.

Pictures and text must be separate native shapes. Add links to both the plank and its text so clicking either works. Keep question and option shape names stable for tests. Use real clickable image targets, not a screenshot pretending to be interactive.

For Arabic:

- set paragraph RTL;
- set run language to `ar-SA` and explicit complex-script font;
- set Latin title language/direction separately;
- use real fonts available on the target system;
- remove default textbox padding when aligning to a prop;
- inspect line wrapping and question-board bounds after office rendering.

A good image does not prevent typography failure. In the example, an unavailable renderer font made a chunky title look like a serif logo. Fix the font configuration and rerender rather than accepting it as close enough.

## Links and transitions

Create slides first, collect pending `(shape, target_name)` links, then resolve them after every target exists using `shape.click_action.target_slide`.

Set `p:transition/@advClick="0"` for game navigation. Use authored links rather than arbitrary click-to-advance. Timed film slides additionally set `advTm`. Kiosk-style show properties can keep the presentation link-driven. Preserve an escape path and clear restart/home controls.

For native fades where a library lacks a public animation API, construct `p:timing` with:

- a `tmRoot` time node;
- a `mainSeq`;
- standard after-previous wrappers;
- an entrance preset and `animEffect transition="in" filter="fade"`;
- `spTgt` references to actual shape IDs;
- unique timing node IDs within each slide.

The included `fade()` implementation is concrete and inspectable. Do not claim that merely writing animation XML proves playback. Validate references and inspect the native application when available.

## Embedded media

Use `add_movie()` with H.264 MP4, a real poster image and `video/mp4`. Set the movie timing start condition to delay zero. Include a skip link above the movie. An auto-advance after the clip is useful, but platform-specific playback must still be checked.

For feedback sounds, create media parts, relate them with the Office audio relationship type and reference them from a transition sound action. No external URLs or local-machine file paths may remain in the deck.

## Verification

Reopen the saved file and test:

- expected slide names and native question text;
- eight native crate targets;
- each answer link and corresponding check/cross state;
- one correct option per question;
- home links;
- ZIP integrity and all internal relationship targets;
- no external relationships or macros;
- unique timing IDs and valid shape targets;
- both MP4s, both WAVs and movie autoplay conditions.

Render all slides through PowerPoint or LibreOffice and inspect contact sheets plus full-size samples. On macOS, a task-local fontconfig file can point a headless LibreOffice build at system font directories without changing global settings. Keep proprietary fonts out of the shared bundle.

LibreOffice rendering is a compatibility/rendering check. It is **not** proof of Microsoft PowerPoint slideshow playback, timing or media behavior. Keep that boundary in the delivery note.

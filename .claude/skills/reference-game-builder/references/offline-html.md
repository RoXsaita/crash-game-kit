# Faithful standalone HTML edition

## Preserve the approved visual design

Reuse the actual PPTX backgrounds, character cutouts, wooden boards, crates, fruit, sounds, question bank and embedded clips. Do not replace a reference-driven game with a generic dashboard theme. A few HTML-only conveniences should not dominate the screen.

The worked implementation uses semantic HTML, plain CSS and JavaScript. Three.js was used to create the clips, not as a runtime dependency of the delivered game.

## Offline packaging

Keep an editable `template.html` with placeholders for question JSON and an asset JSON mapping. The builder reads all PNG/JPEG/WAV/MP4 bytes and replaces placeholders with MIME-typed base64 data URLs. Embed the resulting finished application as a single HTML file.

Check inline JavaScript syntax with Node, then test the actual `file://` artifact. Abort all HTTP(S) requests in browser tests; a page that loads from a local dev server can hide a missing dependency.

The HTML may be larger than a multi-file web app because video/assets are embedded. This is an intentional portability tradeoff. Do not claim that an iOS/Telegram file preview necessarily executes local JavaScript. Desktop Chrome/Edge is the simplest launch path; hosting the exact HTML can be a separately authorised step.

## State and media

The screens are intro, title, portal, crate menu, question and finish. Validate question data and saved state before using them. Track completed questions and attempted option indices. Disable repeated wrong options and all choices after a correct answer. Make completion idempotent and never count a double click twice.

Use muted autoplay with an always-visible skip button for video. Confirm real playback with advancing `currentTime` and nonzero `videoWidth`; a poster is not proof. Start feedback sound only after a user gesture.

Use localStorage for optional save/resume. Handle storage denial gracefully. Starting a new round should confirm before clearing progress. The HTML's persistence does not imply the PowerPoint has equivalent state.

## Layout

For desktop, fit a 16:9 stage to both viewport width and height. Use stage-relative positions and container-relative typography so it resembles the presentation.

Create a deliberate portrait layout rather than shrinking an entire slide to unreadable phone size. Reflow the eight crates to two columns. Keep question text, feedback and fruit navigation separate. On image grids, use `min-height:0` on children and `minmax(0,1fr)` tracks; intrinsic image sizing can overflow a seemingly fixed grid. Measure the last item against the next actual control, not only the grid's own box.

Give explanation text a contrasting backing if the portrait crop places it on dark or busy scenery. Test hitboxes and feedback collisions at real viewport sizes, and distinguish viewport emulation from physical-device testing.

## Safe editing and portable exports

- Validate question count, text limits, two/three option counts, unique nonempty choices and correct-answer indices.
- Use `textContent` for displayed question/feedback text; escape editable values before HTML templates.
- Capture pristine source HTML before runtime mutations.
- To export a customised game, parse a fresh copy, replace only the embedded question JSON, escape `<` as `\u003c`, and download a new HTML Blob.
- Never serialise the live mutated page as the export: it may contain an open modal, completed state, wrong button attributes or old text.
- Reopen the exported file in a fresh path/context and play it with the network blocked. Confirm literal HTML/script-like input remains text.

## Tests

Exercise real clips, the complete eight-question path, both question formats, wrong/correct retry, keyboard navigation, no double counting, completed-crate locking, save/resume/reset cancellation, editor validation, exported-copy gameplay, fullscreen, sound toggle and mobile geometry. Take actual browser screenshots, fix problems, then rerun the suite.

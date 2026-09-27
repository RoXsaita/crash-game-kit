# Paste this into Claude Code

Open Claude Code in the extracted kit directory, then use:

```text
/reference-game-builder

Read the skill, README.md and CLAUDE.md. Inspect both finished examples and the shared asset/question architecture before making changes.

Explain briefly how the native PowerPoint and the HTML edition work, especially linked answer-state slides versus JavaScript state, embedded media, editable text, and portable exports.

Then create a copy for this new brief:
- Theme / reference: [describe theme or paste video URL]
- Audience / subject: [age group and subject]
- Language: [language]
- Deliverables: [PowerPoint, HTML, or both]
- Question bank: [supply eight questions, or ask me for them]
- Visual elements to preserve: [list]

Use the existing assets for an initial faithful prototype unless I approve new art. If you do not have an image-generation tool, say so and give me the exact prompts and required filenames instead of inventing outputs.

Keep questions editable, preserve the requested medium and reference layout, and do not replace the experience with a generic quiz UI. Build real files. Run the package/navigation/browser checks and visually inspect them. Report tested versus untested boundaries, especially native PowerPoint playback and physical mobile devices. Do not upload anything publicly unless I ask.
```

For just changing the topic while keeping the art, ask Claude to edit `source/crash-powerpoint/questions.json`, regenerate both files and update any answer-specific regression fixtures. For understanding the original method only, stop after the explanation and do not request a redesign.

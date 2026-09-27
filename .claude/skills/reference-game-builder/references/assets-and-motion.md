# Assets and motion

## Reference evidence

Inspect the full video before writing the layout. Extract a coarse contact sheet, then full-resolution frames around important events. Use a local working directory and filenames you can carry into the source package. A command pattern is:

```bash
yt-dlp --write-info-json -o 'reference.%(ext)s' REFERENCE_URL
ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate -of json reference.mp4
ffmpeg -i reference.mp4 -vf 'fps=1/3,scale=320:-1,tile=5x4' -frames:v 1 contact.jpg
ffmpeg -ss 10.5 -i reference.mp4 -frames:v 1 question-frame.png
```

Change tile dimensions to cover the real duration. Do not call black unused contact-sheet cells black video frames. Download only through permitted access paths; do not evade access denials.

## Layer inventory

For the worked example, the source assets are:

- a sunny jungle question background, with a mascot at the left and UI-safe space at the right;
- a beach menu background with central empty sand and a small character in one corner;
- a clean beach variant without the background mascot, preventing two mascots on the title;
- a full-body jumping character cutout;
- a blank hanging wooden title/question board;
- a blank answer plank;
- a question-mark crate and fruit navigation icon;
- drawn check/cross icons and short synthesised confirmation/error WAVs;
- short embedded intro/portal MP4s and poster PNGs.

The images in the example were generated with an available GPT Image tool. Claude Code does not automatically have that tool. The included outputs allow rebuilding without a generation account. To make new art, use an available image tool or provide exported PNGs manually.

## Sprite-sheet keying

A single sprite sheet can contain several reusable props. A flat magenta background is suitable when the assets do not contain magenta. Inspect the actual image before choosing crops: the example returned 1672×941 even when a different nominal size was requested.

The included crop recipe is specific to that sheet. It is not universal. Normalise a new sheet to the expected dimensions only if its object arrangement really matches, otherwise change each crop.

For magenta extraction, compare `min(red, blue) - green`, produce a soft alpha boundary, suppress key-color spill at partial-alpha edges, then crop to the alpha bounding box. Review every PNG against both light and dark backgrounds. Thin ropes and leaves are common casualties.

Generated backgrounds and props are raster images, not editable 3D models. Native text is added later. Avoid text/logos baked into backgrounds unless specifically desired. Preserve commercial-use limitations for recognisable third-party characters.

## Motion rendering

`animation-renderer.html` contains two deterministic Three.js scenes:

1. White studio: textured 3D cubes, floor, lights/shadows and a transparent character billboard. The character is a cutout, not a rigged 3D model.
2. Portal: torus rings, a stone gate, star particles and a procedural vortex shader with a moving camera.

Expose `renderFrame(mode, time)` and wait for all textures to load. Use a temporary loopback HTTP server for ES modules, render at fixed time steps, and save frames before encoding. The included scenes use 96 frames at 24 fps, giving four-second clips.

```bash
ffmpeg -framerate 24 -i frames/%04d.png -c:v libx264 -crf 20 \
  -pix_fmt yuv420p -movflags +faststart clip.mp4
ffmpeg -v error -i clip.mp4 -f null -
```

Keep Three.js modules local and preserve their MIT license. Software-rendering flags, if necessary, belong only to the isolated QA browser; never weaken the user's normal browser settings. Embedded finished clips do not require Three.js on the recipient's computer.

Do not claim a still-image cutout animation is generated full-character animation. Do not claim a preview assembled from clips and slide images is a live PowerPoint screen recording.

from pathlib import Path
import subprocess
ROOT=Path(__file__).parent
out=ROOT/'preview-parts';out.mkdir(exist_ok=True)
# Demonstration assembled from actual office-rendered slides and the embedded MP4s.
# This is not represented as a recording of Microsoft PowerPoint playback.
sequence=[('intro.mp4',4,None),('slide-02.png',2,None),('portal.mp4',4,None),('slide-04.png',2,None),('slide-05.png',2,None),('slide-06.png',1.5,'wrong'),('slide-07.png',2,'correct'),('slide-04.png',1.5,None),('slide-21.png',2,None),('slide-22.png',2,'correct'),('slide-35.png',2,None)]
for i,(name,duration,audio) in enumerate(sequence):
    source=ROOT/('assets' if name.endswith('.mp4') else 'rendered')/name
    cmd=['ffmpeg','-y','-v','error']
    if name.endswith('.png'):cmd+=['-loop','1']
    cmd+=['-i',str(source)]
    if audio:cmd+=['-i',str(ROOT/'assets'/f'{audio}.wav')]
    else:cmd+=['-f','lavfi','-i','anullsrc=r=44100:cl=stereo']
    cmd+=['-t',str(duration),'-vf','scale=1280:720,setsar=1','-r','24','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-af','apad','-c:a','aac','-ar','44100','-ac','2','-b:a','128k','-map','0:v:0','-map','1:a:0',str(out/f'{i:02d}.mp4')]
    subprocess.run(cmd,check=True)
(out/'concat.txt').write_text(''.join(f"file '{i:02d}.mp4'\n" for i in range(len(sequence))))
subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(out/'concat.txt'),'-c','copy','-movflags','+faststart',str(ROOT/'Crash-PowerPoint-Preview.mp4')],check=True)
print('Deck-render preview assembled:',ROOT/'Crash-PowerPoint-Preview.mp4')

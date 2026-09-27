from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import wave, math, struct, argparse
ROOT=Path(__file__).parent
A=ROOT/'assets';A.mkdir(exist_ok=True)
parser=argparse.ArgumentParser()
parser.add_argument('--raw-dir',type=Path,default=ROOT/'raw-assets')
parser.add_argument('--font',type=Path,help='Optional local TTF/OTF font for crate texture')
args=parser.parse_args()
S=args.raw_dir
inputs={name:name+'.png' for name in ['jungle','beach','sprites','crash']}
def key(im):
    im=im.convert('RGBA'); pixels=[]
    for r,g,b,a in im.get_flattened_data():
        d=min(r,b)-g
        alpha=max(0,min(255,round((155-d)*255/75)))
        if alpha and alpha<255:
            r=min(r,g+70);b=min(b,g+45)
        pixels.append((r,g,b,alpha))
    im.putdata(pixels)
    box=im.getbbox()
    return im.crop(box) if box else im
for n in ['jungle','beach']:
    Image.open(S/inputs[n]).convert('RGB').resize((1920,1080),Image.Resampling.LANCZOS).save(A/f'{n}.jpg',quality=94)
Image.open(A/'beach.jpg').crop((0,0,1460,1080)).resize((1920,1080),Image.Resampling.LANCZOS).save(A/'beach-clean.jpg',quality=94)
sheet=Image.open(S/inputs['sprites'])
for n,box in {'sign':(0,0,1672,395),'plank':(0,407,1672,548),'crate':(125,552,560,941),'fruit':(1100,553,1490,941)}.items():
    key(sheet.crop(box)).save(A/f'{n}.png')
key(Image.open(S/inputs['crash'])).save(A/'crash.png')
for name,color,mark in [('correct','#66bd42','✓'),('wrong','#e74b3e','×')]:
    im=Image.new('RGBA',(220,220));d=ImageDraw.Draw(im)
    d.ellipse((8,8,212,212),fill=color,outline='#f7ffe8',width=8)
    if name=='correct':d.line([(52,111),(91,148),(168,67)],fill='white',width=23)
    else:
        d.line([(65,65),(156,156)],fill='white',width=22);d.line([(156,65),(65,156)],fill='white',width=22)
    im.save(A/f'{name}.png')
for name,freqs in [('correct',[523.25,659.25,783.99]),('wrong',[220,164.81])]:
    sr=22050; samples=[]
    for f in freqs:
        for k in range(int(sr*.18)):
            t=k/sr; env=min(1,t/.01)*max(0,1-t/.18)
            samples.append(int(8000*env*math.sin(2*math.pi*f*t)))
    with wave.open(str(A/f'{name}.wav'),'w') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(struct.pack('<'+'h'*len(samples),*samples))
# Front-facing crate texture for real 3D intro cubes.
im=Image.new('RGB',(512,512),'#984318');d=ImageDraw.Draw(im)
for y in range(0,512,12):d.line((0,y,512,y+8),fill='#783912',width=3)
for xy in [(0,0,512,42),(0,470,512,512),(0,0,42,512),(470,0,512,512)]:d.rectangle(xy,fill='#edb44e')
d.line((42,42,470,470),fill='#c88230',width=26);d.line((470,42,42,470),fill='#c88230',width=26)
font=ImageFont.truetype(str(args.font),330) if args.font else ImageFont.load_default(size=330)
d.text((260,260),'?',font=font,anchor='mm',fill='#fff081',stroke_width=7,stroke_fill='#67330e')
im.save(A/'crate-face.png')
print('Assets prepared:',[(p.name,p.stat().st_size) for p in A.iterdir()])

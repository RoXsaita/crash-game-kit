from pathlib import Path
import fitz,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).parent;D=ROOT/'rendered';doc=fitz.open(D/'Crash-Classroom.pdf')
report={'pages':len(doc),'links':0,'empty_pages':[]}
for i,page in enumerate(doc):
    pix=page.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False)
    pix.save(D/f'slide-{i+1:02d}.png')
    report['links']+=len(page.get_links())
    if not page.get_text().strip():report['empty_pages'].append(i+1)
for batch in range(3):
    sheet=Image.new('RGB',(1600,3*249),'#172122');draw=ImageDraw.Draw(sheet)
    for k in range(12):
        i=batch*12+k
        if i>=len(doc):break
        im=Image.open(D/f'slide-{i+1:02d}.png').resize((400,225))
        x=(k%4)*400;y=(k//4)*249
        sheet.paste(im,(x,y));draw.text((x+8,y+228),str(i+1),fill='white')
    sheet.save(D/f'contact-{batch+1}.jpg',quality=95)
print(json.dumps(report))

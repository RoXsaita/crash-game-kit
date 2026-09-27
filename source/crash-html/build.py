from pathlib import Path
import base64,json,mimetypes,re,subprocess,shutil
ROOT=Path(__file__).parent
SOURCE=ROOT.parent/'crash-powerpoint'
FILES={'beach-clean':'beach-clean.jpg','beach':'beach.jpg','jungle':'jungle.jpg','crash':'crash.png','sign':'sign.png','crate':'crate.png','plank':'plank.png','fruit':'fruit.png','correct':'correct.png','wrong':'wrong.png','correctSound':'correct.wav','wrongSound':'wrong.wav','intro':'intro.mp4','portal':'portal.mp4','introPoster':'intro-poster.png','portalPoster':'portal-poster.png'}
assets={}
for key,name in FILES.items():
    mime=mimetypes.guess_type(name)[0]
    assets[key]='data:'+mime+';base64,'+base64.b64encode((SOURCE/'assets'/name).read_bytes()).decode()
quiz=json.loads((SOURCE/'questions.json').read_text(encoding='utf-8'))
template=(ROOT/'template.html').read_text(encoding='utf-8')
html=template.replace('__ASSETS__',json.dumps(assets,separators=(',',':'))).replace('__QUIZ__',json.dumps(quiz,ensure_ascii=False).replace('<','\\u003c'))
assert '__ASSETS__' not in html and '__QUIZ__' not in html
script=re.search(r'<script>\s*(.*?)</script>',html,re.S)[1]
subprocess.run([shutil.which('node') or 'node','--check'],input=script,text=True,check=True)
(ROOT/'Crash-Classroom.html').write_text(html,encoding='utf-8')
print('Standalone HTML built:',len(html.encode()),'bytes; embedded assets:',len(assets))

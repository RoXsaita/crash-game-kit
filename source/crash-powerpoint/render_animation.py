from pathlib import Path
import threading, http.server, functools, subprocess
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).parent
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        page=browser.new_page(viewport={'width':1280,'height':720})
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(f'http://127.0.0.1:{server.server_port}/animation-renderer.html')
        page.wait_for_function('window.ready===true',timeout=60000)
        for mode in ['intro','portal']:
            directory=ROOT/'render-frames'/mode;directory.mkdir(parents=True,exist_ok=True)
            for n in range(96):
                page.evaluate('([m,t])=>window.renderFrame(m,t)',[mode,n/24])
                page.screenshot(path=str(directory/f'{n:04d}.png'))
            page.evaluate('([m,t])=>window.renderFrame(m,t)',[mode,1.7])
            page.screenshot(path=str(ROOT/'assets'/f'{mode}-poster.png'))
            subprocess.run(['ffmpeg','-y','-v','error','-framerate','24','-i',str(directory/'%04d.png'),'-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(ROOT/'assets'/f'{mode}.mp4')],check=True)
            print(mode,'rendered 96 genuine WebGL frames',flush=True)
        assert not errors,errors
        browser.close()
finally:server.shutdown()

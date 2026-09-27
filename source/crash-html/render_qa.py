from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).parent
D=ROOT/'qa';D.mkdir(exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(headless=True)
    c=b.new_context(viewport={'width':1440,'height':900},reduced_motion='reduce')
    page=c.new_page();page.goto((ROOT/'Crash-Classroom.html').as_uri())
    page.locator('#skip-film').click();page.screenshot(path=str(D/'01-title.png'))
    page.locator('#play').click();page.locator('#skip-film').click();page.screenshot(path=str(D/'02-menu.png'))
    page.locator('[data-crate="0"]').click();page.screenshot(path=str(D/'03-question.png'))
    page.locator('[data-choice="0"]').click();page.screenshot(path=str(D/'04-wrong.png'))
    page.locator('[data-choice="1"]').click();page.screenshot(path=str(D/'05-correct.png'))
    page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(D/'06-mobile-feedback.png'),full_page=True)
    page.locator('#question-home').click();page.screenshot(path=str(D/'07-mobile-menu.png'),full_page=True)
    page.locator('#menu-home').click();page.screenshot(path=str(D/'08-mobile-title.png'),full_page=True)
    c.close();b.close()
print('Rendered desktop and mobile QA screenshots.')

from pathlib import Path
import unittest
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).parent
class CrashHTMLTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p=sync_playwright().start();cls.browser=cls.p.chromium.launch(headless=True)
    @classmethod
    def tearDownClass(cls):cls.browser.close();cls.p.stop()
    def setUp(self):
        self.assertTrue((ROOT/'Crash-Classroom.html').exists(),'Faithful HTML version is not implemented')
        self.context=self.browser.new_context(viewport={'width':1440,'height':900},reduced_motion='reduce',accept_downloads=True)
        self.page=self.context.new_page();self.errors=[];self.network=[]
        self.page.on('pageerror',lambda e:self.errors.append(str(e)))
        self.page.route('http**/*',lambda r:(self.network.append(r.request.url),r.abort()))
        self.page.goto((ROOT/'Crash-Classroom.html').as_uri())
    def tearDown(self):
        if hasattr(self,'context'):
            self.context.close();self.assertEqual(self.errors,[]);self.assertEqual(self.network,[])
    def start(self):
        self.page.locator('#skip-film').click();self.page.locator('#play').click();self.page.locator('#skip-film').click()
    def bank(self):return self.page.evaluate('JSON.parse(document.getElementById("quiz-data").textContent)')
    def test_real_embedded_video_playback_and_offline_assets(self):
        self.page.wait_for_function('document.getElementById("film").currentTime > .2')
        self.assertGreater(self.page.locator('#film').evaluate('(v)=>v.videoWidth'),0)
        self.page.locator('#skip-film').click();self.page.locator('#play').click()
        self.page.wait_for_function('document.getElementById("film").currentTime > .2')
        self.page.locator('#skip-film').click()
        self.assertEqual(self.page.locator('[data-crate]').count(),8)
        self.assertTrue(self.page.locator('.scene-image').first.evaluate('(im)=>im.naturalWidth>0'))
    def test_full_game_correct_answers_and_finale(self):
        bank=self.bank();self.start()
        for i,q in enumerate(bank):
            self.page.locator(f'[data-crate="{i}"]').click()
            self.assertEqual(self.page.locator('[data-choice]').count(),len(q['options']))
            self.page.locator(f'[data-choice="{q["correct"]}"]').click()
            self.assertIn('أحسنت',self.page.locator('#feedback-message').inner_text())
            self.assertEqual(self.page.locator('[data-choice]:not([disabled])').count(),0)
            self.page.locator('#question-home').click()
            if i<7:self.assertTrue(self.page.locator(f'[data-crate="{i}"]').is_disabled())
        self.assertTrue(self.page.locator('#finish-screen').is_visible())
        self.assertIn('٨',self.page.locator('#finish-stats').inner_text())
    def test_wrong_answer_retry_and_keyboard(self):
        self.start();self.page.locator('[data-crate="0"]').click()
        self.page.keyboard.press('1')
        self.assertIn('حاول',self.page.locator('#feedback-message').inner_text())
        self.assertTrue(self.page.locator('[data-choice="0"]').is_disabled())
        self.page.keyboard.press('2')
        self.assertIn('أحسنت',self.page.locator('#feedback-message').inner_text())
        self.page.keyboard.press('Escape')
        self.assertTrue(self.page.locator('[data-crate="0"]').is_disabled())
    def test_save_resume_and_explicit_reset(self):
        self.start();self.page.locator('[data-crate="0"]').click();self.page.locator('[data-choice="1"]').click();self.page.locator('#question-home').click()
        self.page.reload();self.page.locator('#skip-film').click()
        self.assertTrue(self.page.locator('#resume').is_visible())
        self.page.locator('#resume').click();self.assertTrue(self.page.locator('[data-crate="0"]').is_disabled())
        self.page.locator('#menu-home').click();self.page.locator('#play').click()
        self.assertTrue(self.page.locator('#reset-dialog').is_visible())
        self.page.locator('#cancel-reset').click();self.assertTrue(self.page.locator('#resume').is_visible())
        self.page.locator('#play').click();self.page.locator('#confirm-reset').click();self.page.locator('#skip-film').click()
        self.assertFalse(self.page.locator('[data-crate="0"]').is_disabled())
    def test_editor_validation_and_portable_export(self):
        self.page.locator('#skip-film').click();self.page.locator('#edit').click()
        self.page.locator('[data-q="0"] [data-field="text"]').fill('')
        self.page.locator('#save-edit').click()
        self.assertNotEqual(self.page.locator('#edit-error').inner_text(),'')
        custom='ما عاصمة اليابان؟ <b>اختبار</b>'
        self.page.locator('[data-q="0"] [data-field="text"]').fill(custom)
        self.page.locator('[data-q="0"] [data-option="0"]').fill('طوكيو')
        self.page.locator('[data-q="0"] [data-field="correct"]').select_option('0')
        with self.page.expect_download() as info:self.page.locator('#download-custom').click()
        path=ROOT/'qa-custom.html';info.value.save_as(path)
        self.page.goto(path.as_uri());self.start();self.page.locator('[data-crate="0"]').click()
        self.assertEqual(self.page.locator('#question-text').inner_text(),custom)
        self.assertEqual(self.page.locator('#question-text b').count(),0)
        self.page.locator('[data-choice="0"]').click();self.assertIn('أحسنت',self.page.locator('#feedback-message').inner_text())
        path.unlink()
    def test_portrait_mobile_all_controls_accessible(self):
        self.page.set_viewport_size({'width':390,'height':844});self.start()
        self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'),390)
        self.assertEqual(self.page.locator('[data-crate]').count(),8)
        self.page.locator('[data-crate="4"]').click()
        self.assertEqual(self.page.locator('[data-choice]').count(),2)
        for selector in ['#question-text','[data-choice="0"]','[data-choice="1"]','#question-home']:
            box=self.page.locator(selector).bounding_box();self.assertGreaterEqual(box['y'],0);self.assertLessEqual(box['y']+box['height'],844)
    def test_mobile_feedback_and_menu_controls_do_not_overlap(self):
        self.page.set_viewport_size({'width':390,'height':844});self.start()
        crate=self.page.locator('[data-crate="7"]').bounding_box()
        finish=self.page.locator('#finish-early').bounding_box()
        self.assertLessEqual(crate['y']+crate['height']+8,finish['y'])
        self.page.locator('[data-crate="0"]').click();self.page.locator('[data-choice="1"]').click()
        explanation=self.page.locator('#explanation').bounding_box()
        home=self.page.locator('#question-home').bounding_box()
        self.assertLessEqual(explanation['y']+explanation['height']+8,home['y'])
    def test_fullscreen_audio_toggle_and_no_duplicate_score(self):
        self.page.locator('#skip-film').click();self.page.locator('#sound').click()
        self.assertEqual(self.page.locator('#sound').get_attribute('aria-pressed'),'true')
        self.page.locator('#fullscreen').click();self.page.wait_for_function('document.fullscreenElement!==null')
        self.page.locator('#fullscreen').click();self.page.locator('#play').click();self.page.locator('#skip-film').click()
        self.page.locator('[data-crate="0"]').click();self.page.keyboard.press('2');self.page.keyboard.press('2')
        self.page.locator('#question-home').click();self.assertEqual(self.page.locator('#progress').inner_text(),'١ / ٨')
if __name__=='__main__':unittest.main(verbosity=2)

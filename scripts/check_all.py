from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parent.parent
for relative in ["source/crash-powerpoint/test_deck.py","source/crash-html/test_game.py"]:
    subprocess.run([sys.executable,str(ROOT/relative)],cwd=ROOT,check=True)
print("PowerPoint structure/navigation and offline browser suites passed.")

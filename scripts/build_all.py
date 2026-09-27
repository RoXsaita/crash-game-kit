from pathlib import Path
import shutil, subprocess, sys
ROOT=Path(__file__).resolve().parent.parent
if not shutil.which("node"):
    raise SystemExit("Node.js must be installed and available on PATH for inline JavaScript syntax validation.")
for relative in ["source/crash-powerpoint/build_deck.py", "source/crash-html/build.py"]:
    subprocess.run([sys.executable,str(ROOT/relative)],cwd=ROOT,check=True)
out=ROOT/"deliverables";out.mkdir(exist_ok=True)
for folder,name in [("crash-powerpoint","Crash-Classroom.pptx"),("crash-html","Crash-Classroom.html")]:
    shutil.copy2(ROOT/"source"/folder/name,out/name)
print("Built deliverables/Crash-Classroom.pptx and deliverables/Crash-Classroom.html")

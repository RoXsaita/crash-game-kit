from pathlib import Path
import argparse,hashlib,json,re,zipfile,subprocess
parser=argparse.ArgumentParser()
parser.add_argument("root",nargs="?",type=Path,default=Path(__file__).resolve().parent.parent)
parser.add_argument("--forbid",action="append",default=[],help="Additional private text that must not appear")
parser.add_argument("--manifest",action="store_true")
parser.add_argument("--tracked",action="store_true",help="Audit only Git-tracked files in a development checkout")
args=parser.parse_args();root=args.root.resolve();errors=[];checked=0
text_ext={".md",".py",".html",".js",".json",".txt",".xml",".rels",".conf",".yaml",".yml"}
home=re.compile(r"/(?:Users|home)/[A-Za-z0-9_.-]+|[A-Z]:\\Users\\[A-Za-z0-9_.-]+")
secrets=re.compile(r"(?:sk-proj-[A-Za-z0-9_-]{24,}|ghp_[A-Za-z0-9]{30,}|AKIA[A-Z0-9]{16})")
def check_text(name,raw):
    try:text=raw.decode("utf-8")
    except UnicodeDecodeError:return
    text=re.sub(r"data:[^\s\"]*;base64,[A-Za-z0-9+/=]+","[embedded media]",text)
    for needle in args.forbid:
        if needle.lower() in text.lower():errors.append(name+": forbidden private marker")
    if home.search(text):errors.append(name+": machine-specific home path")
    if secrets.search(text):errors.append(name+": secret-shaped value")
paths = [root/p for p in subprocess.check_output(["git","ls-files","-z"],cwd=root).decode().split("\0") if p] if args.tracked else root.rglob("*")
for path in paths:
    if not path.is_file():continue
    rel=path.relative_to(root).as_posix();checked+=1
    if any(part in {".git",".venv","node_modules","__pycache__"} for part in path.relative_to(root).parts) or path.name==".env" or path.suffix.lower() in {".db",".sqlite",".pyc",".ttf",".otf"}:
        errors.append(rel+": forbidden runtime/credential/font file")
    if path.suffix.lower() in text_ext:check_text(rel,path.read_bytes())
    if path.suffix.lower()==".pptx":
        with zipfile.ZipFile(path) as z:
            if z.testzip():errors.append(rel+": corrupt Office package")
            for member in z.namelist():
                if member.endswith((".xml",".rels")):check_text(rel+":"+member,z.read(member))
if args.manifest:
    manifest=json.loads((root/"MANIFEST.json").read_text(encoding="utf-8"))
    for item in manifest["files"]:
        path=root/item["path"]
        if not path.is_file() or path.stat().st_size!=item["bytes"] or hashlib.sha256(path.read_bytes()).hexdigest()!=item["sha256"]:
            errors.append(item["path"]+": manifest mismatch")
    expected={item["path"] for item in manifest["files"]}|{"MANIFEST.json"}
    actual={p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
    if actual!=expected:errors.append("Archive file set differs from manifest")
print(json.dumps({"files_checked":checked,"errors":errors},indent=2))
raise SystemExit(1 if errors else 0)

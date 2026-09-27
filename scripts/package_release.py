"""Package only tracked source + explicitly named built deliverables."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "dist"
DELIVERABLES = ["deliverables/Crash-Classroom.html", "deliverables/Crash-Classroom.pptx"]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    subprocess.run([sys.executable, str(ROOT / "scripts/audit_bundle.py"), "--tracked"], check=True)
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
    paths = sorted(set(p for p in tracked if p) | set(DELIVERABLES))
    for name in paths:
        path = ROOT / name
        if not path.is_file() or path.is_symlink():
            raise SystemExit(f"Missing or unsafe release input: {name}. Build both outputs first.")
    OUTPUT.mkdir(exist_ok=True)
    archive = OUTPUT / "Crash-Game-Kit.zip"
    manifest = {"format_version": 1, "files": [
        {"path": name, "bytes": (ROOT / name).stat().st_size, "sha256": sha256(ROOT / name)}
        for name in paths
    ]}
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=8) as z:
        for name in paths:
            z.write(ROOT / name, "Crash-Game-Kit/" + name)
        z.writestr("Crash-Game-Kit/MANIFEST.json", json.dumps(manifest, indent=2))
    with tempfile.TemporaryDirectory(prefix="crash-release-", dir=os.environ.get("TMPDIR")) as directory:
        with zipfile.ZipFile(archive) as z:
            if z.testzip() is not None:
                raise SystemExit("Corrupt release ZIP")
            z.extractall(directory)
        extracted = Path(directory) / "Crash-Game-Kit"
        subprocess.run([sys.executable, str(extracted / "scripts/audit_bundle.py"),
                        str(extracted), "--manifest"], check=True)
    checksum_paths = [archive, *(ROOT / name for name in DELIVERABLES)]
    (OUTPUT / "SHA256SUMS.txt").write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in checksum_paths), encoding="utf-8")
    print(f"Release verified: {archive.name} ({archive.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

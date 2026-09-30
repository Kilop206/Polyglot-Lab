from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]

targets = [
    ROOT / "build",
    ROOT / "out",
    ROOT / ".tmp",
]

for target in targets:
    if target.exists():
        shutil.rmtree(target)
        print(f"removed {target.relative_to(ROOT)}")

for cache in ROOT.rglob("__pycache__"):
    shutil.rmtree(cache, ignore_errors=True)
    print(f"removed {cache.relative_to(ROOT)}")

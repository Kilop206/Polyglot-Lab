from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IMPL = ROOT / "implementations"

def call(cmd, cwd):
    print(f"\n==> {cwd.relative_to(ROOT)}: {' '.join(cmd)}")
    return subprocess.call(cmd, cwd=cwd)

def main():
    if not IMPL.exists():
        print("No implementations directory yet.")
        return 0

    failures = 0
    discovered = 0

    for cargo in IMPL.rglob("Cargo.toml"):
        discovered += 1
        failures += call(["cargo", "test"], cargo.parent) != 0

    for gomod in IMPL.rglob("go.mod"):
        discovered += 1
        failures += call(["go", "test", "./..."], gomod.parent) != 0

    for cmake in IMPL.rglob("CMakeLists.txt"):
        build = cmake.parent / "build"
        if build.exists():
            discovered += 1
            failures += call(["ctest", "--test-dir", str(build), "--output-on-failure"], cmake.parent) != 0

    if discovered == 0:
        print("No recognized testable implementations found.")
    return 1 if failures else 0

if __name__ == "__main__":
    sys.exit(main())

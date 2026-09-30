from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", default=str(ROOT / "conformance" / "fixtures" / "implementation-matrix.example.json"))
    args = parser.parse_args()

    path = Path(args.matrix)
    if not path.exists():
        print(f"Matrix not found: {path}")
        print("Copy implementation-matrix.example.json and add server commands.")
        return 0

    matrix = json.loads(path.read_text(encoding="utf-8"))
    failures = 0
    for impl in matrix.get("implementations", []):
        if not impl.get("enabled", False):
            continue
        print(f"\n### {impl['name']}")
        cmd = [
            sys.executable,
            str(ROOT / "conformance" / "runner" / "netlab_conformance.py"),
            "--host", impl.get("host", "127.0.0.1"),
            "--port", str(impl.get("port", 7000)),
            "--server-command", impl["server_command"],
        ]
        failures += subprocess.call(cmd) != 0

    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7000)
    args = parser.parse_args()

    failures = 0
    for scenario in sorted((ROOT / "benchmarks" / "scenarios").glob("*.json")):
        print(f"\n### {scenario.stem}")
        cmd = [
            sys.executable,
            str(ROOT / "benchmarks" / "runners" / "netlab_benchmark.py"),
            "--scenario", str(scenario),
            "--host", args.host,
            "--port", str(args.port),
        ]
        failures += subprocess.call(cmd) != 0
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def fail(message):
    print(f"[FAIL] {message}")
    return 1

def main():
    failures = 0

    required = [
        "README.md",
        "VERSION",
        "spec/protocol.md",
        "spec/framing.md",
        "spec/messages.md",
        "spec/errors.md",
        "conformance/runner/netlab_conformance.py",
        "benchmarks/runners/netlab_benchmark.py",
    ]

    for rel in required:
        if not (ROOT / rel).exists():
            failures += fail(f"missing required file: {rel}")

    for path in ROOT.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures += fail(f"invalid JSON {path.relative_to(ROOT)}: {exc}")

    for metadata in (ROOT / "test-vectors").rglob("*.json"):
        obj = json.loads(metadata.read_text(encoding="utf-8"))
        binary = metadata.with_suffix(".bin")
        if binary.exists():
            data = binary.read_bytes()
            actual = hashlib.sha256(data).hexdigest()
            expected = obj.get("sha256")
            if expected != actual:
                failures += fail(
                    f"hash mismatch: {binary.relative_to(ROOT)} expected={expected} actual={actual}"
                )
            if obj.get("wire_hex") and bytes.fromhex(obj["wire_hex"]) != data:
                failures += fail(f"wire_hex mismatch: {metadata.relative_to(ROOT)}")

    if failures:
        print(f"\nRepository validation failed with {failures} issue(s).")
        return 1

    print("[PASS] repository structure")
    print("[PASS] JSON syntax")
    print("[PASS] test-vector hashes and wire hex")
    print("\nNetLab repository validation succeeded.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

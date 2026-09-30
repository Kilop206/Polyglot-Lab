from __future__ import annotations

import argparse
import json
import shlex
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from protocol import TYPES, encode_frame, recv_frame, decode_error_payload, decode_info

BASE = Path(__file__).resolve().parents[1]
SCENARIOS = BASE / "scenarios"
REPORTS = BASE / "reports"

ERROR_CODES = {
    "INVALID_MAGIC": 0x0001,
    "UNSUPPORTED_VERSION": 0x0002,
    "INVALID_MESSAGE_TYPE": 0x0003,
    "INVALID_LENGTH": 0x0004,
    "PAYLOAD_TOO_LARGE": 0x0005,
    "MALFORMED_PAYLOAD": 0x0006,
    "INVALID_STATE": 0x0007,
    "INVALID_FLAGS": 0x0008,
}

def connect(host: str, port: int, timeout: float) -> socket.socket:
    s = socket.create_connection((host, port), timeout=timeout)
    s.settimeout(timeout)
    return s

def payload_from_step(step):
    if "payload_utf8" in step:
        return step["payload_utf8"].encode("utf-8")
    if "payload_hex" in step:
        return bytes.fromhex(step["payload_hex"])
    return b""

def perform_handshake(sock, name="netlab-conformance"):
    sock.sendall(encode_frame("HELLO", 1, name.encode("utf-8")))
    response = recv_frame(sock)
    if response.message_type != TYPES["HELLO_ACK"] or response.request_id != 1:
        raise AssertionError(f"expected HELLO_ACK/1, got {response.type_name}/{response.request_id}")

def run_scenario(path: Path, host: str, port: int, timeout: float):
    scenario = json.loads(path.read_text(encoding="utf-8"))
    sock = None
    try:
        for step in scenario["steps"]:
            op = step["op"]

            if op == "connect":
                sock = connect(host, port, timeout)

            elif op == "handshake":
                if sock is None:
                    raise AssertionError("handshake without connection")
                perform_handshake(sock, step.get("client_name", "netlab-conformance"))

            elif op == "send":
                if sock is None:
                    raise AssertionError("send without connection")
                data = encode_frame(
                    step["type"],
                    step["request_id"],
                    payload_from_step(step),
                    version=step.get("version", 1),
                    flags=step.get("flags", 0),
                    magic=bytes.fromhex(step["magic_hex"]) if "magic_hex" in step else b"NL",
                )
                sock.sendall(data)

            elif op == "send_fragmented":
                if sock is None:
                    raise AssertionError("send_fragmented without connection")
                data = encode_frame(
                    step["type"],
                    step["request_id"],
                    payload_from_step(step),
                )
                cursor = 0
                for size in step["chunks"]:
                    if cursor >= len(data):
                        break
                    sock.sendall(data[cursor:cursor + size])
                    cursor += size
                    time.sleep(step.get("delay_ms", 5) / 1000.0)
                if cursor < len(data):
                    sock.sendall(data[cursor:])

            elif op == "send_combined":
                if sock is None:
                    raise AssertionError("send_combined without connection")
                blobs = []
                for item in step["frames"]:
                    blobs.append(encode_frame(item["type"], item["request_id"], payload_from_step(item)))
                sock.sendall(b"".join(blobs))

            elif op == "expect":
                if sock is None:
                    raise AssertionError("expect without connection")
                response = recv_frame(sock)
                expected_type = TYPES[step["type"]]
                if response.message_type != expected_type:
                    raise AssertionError(f"expected {step['type']}, got {response.type_name}")
                if "request_id" in step and response.request_id != step["request_id"]:
                    raise AssertionError(
                        f"expected request_id {step['request_id']}, got {response.request_id}"
                    )
                expected_payload = payload_from_step(step)
                if ("payload_utf8" in step or "payload_hex" in step) and response.payload != expected_payload:
                    raise AssertionError("response payload mismatch")

            elif op == "expect_info":
                response = recv_frame(sock)
                if response.message_type != TYPES["INFO_RESULT"]:
                    raise AssertionError(f"expected INFO_RESULT, got {response.type_name}")
                if response.request_id != step["request_id"]:
                    raise AssertionError("INFO_RESULT request_id mismatch")
                obj = decode_info(response.payload)
                required = {
                    "implementation": str,
                    "protocol_version": int,
                    "uptime_ms": int,
                    "active_connections": int,
                }
                for key, typ in required.items():
                    if key not in obj or not isinstance(obj[key], typ):
                        raise AssertionError(f"INFO_RESULT invalid field: {key}")
                if obj["protocol_version"] != 1:
                    raise AssertionError("protocol_version must be 1")

            elif op == "expect_error":
                response = recv_frame(sock)
                if response.message_type != TYPES["ERROR"]:
                    raise AssertionError(f"expected ERROR, got {response.type_name}")
                if "request_id" in step and response.request_id != step["request_id"]:
                    raise AssertionError("ERROR request_id mismatch")
                code, _ = decode_error_payload(response.payload)
                expected = ERROR_CODES[step["error"]]
                if code != expected:
                    raise AssertionError(f"expected error 0x{expected:04X}, got 0x{code:04X}")

            elif op == "close":
                if sock is not None:
                    sock.close()
                    sock = None

            else:
                raise ValueError(f"unknown operation: {op}")

        return {"name": scenario["name"], "status": "PASS", "error": None}
    except Exception as exc:
        return {"name": scenario["name"], "status": "FAIL", "error": str(exc)}
    finally:
        if sock is not None:
            try:
                sock.close()
            except OSError:
                pass

def wait_for_server(host, port, timeout=5.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.2):
                return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError(f"server did not become reachable at {host}:{port}")

def main():
    parser = argparse.ArgumentParser(description="NetLab conformance runner")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7000)
    parser.add_argument("--timeout", type=float, default=2.0)
    parser.add_argument("--server-command", help="optional command used to start the server")
    parser.add_argument("--scenario", action="append", help="run only the named scenario stem")
    args = parser.parse_args()

    process = None
    try:
        if args.server_command:
            process = subprocess.Popen(shlex.split(args.server_command))
            wait_for_server(args.host, args.port)

        paths = sorted(SCENARIOS.glob("*.json"))
        if args.scenario:
            wanted = set(args.scenario)
            paths = [p for p in paths if p.stem in wanted]

        results = [run_scenario(p, args.host, args.port, args.timeout) for p in paths]

        print("NetLab Conformance")
        print("=" * 60)
        for result in results:
            suffix = f" - {result['error']}" if result["error"] else ""
            print(f"[{result['status']}] {result['name']}{suffix}")

        REPORTS.mkdir(parents=True, exist_ok=True)
        report = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "host": args.host,
            "port": args.port,
            "results": results,
        }
        out = REPORTS / "latest.json"
        out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

        failed = [r for r in results if r["status"] != "PASS"]
        print("-" * 60)
        print(f"{len(results) - len(failed)}/{len(results)} scenarios passed")
        return 1 if failed else 0
    finally:
        if process is not None:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()

if __name__ == "__main__":
    sys.exit(main())

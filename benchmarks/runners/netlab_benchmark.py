from __future__ import annotations

import argparse
import json
import socket
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFORMANCE_RUNNER = ROOT / "conformance" / "runner"
sys.path.insert(0, str(CONFORMANCE_RUNNER))

from protocol import TYPES, encode_frame, recv_frame  # noqa: E402

def handshake(sock):
    sock.sendall(encode_frame("HELLO", 1, b"netlab-benchmark"))
    response = recv_frame(sock)
    if response.message_type != TYPES["HELLO_ACK"]:
        raise RuntimeError("handshake failed")

def percentile(values, p):
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int(round((p / 100) * (len(ordered) - 1)))))
    return ordered[index]

def main():
    parser = argparse.ArgumentParser(description="NetLab benchmark runner")
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7000)
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args()

    scenario = json.loads(Path(args.scenario).read_text(encoding="utf-8"))
    message_type = scenario["message_type"]
    response_type = scenario["response_type"]
    requests = scenario.get("requests", 1000)
    warmup = scenario.get("warmup_requests", 50)
    payload_size = scenario.get("payload_size", 0)
    payload = bytes((i % 251 for i in range(payload_size)))

    latencies_ms = []

    with socket.create_connection((args.host, args.port), timeout=args.timeout) as sock:
        sock.settimeout(args.timeout)
        handshake(sock)

        for i in range(warmup):
            request_id = 10_000 + i
            sock.sendall(encode_frame(message_type, request_id, payload))
            response = recv_frame(sock)
            if response.message_type != TYPES[response_type]:
                raise RuntimeError("unexpected warmup response")

        started = time.perf_counter()
        for i in range(requests):
            request_id = 100_000 + i
            t0 = time.perf_counter_ns()
            sock.sendall(encode_frame(message_type, request_id, payload))
            response = recv_frame(sock)
            t1 = time.perf_counter_ns()

            if response.message_type != TYPES[response_type]:
                raise RuntimeError(f"unexpected response: {response.type_name}")
            if response.request_id != request_id:
                raise RuntimeError("request ID mismatch")
            if message_type == "ECHO" and response.payload != payload:
                raise RuntimeError("ECHO payload mismatch")

            latencies_ms.append((t1 - t0) / 1_000_000)

        elapsed = time.perf_counter() - started

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scenario": scenario["name"],
        "host": args.host,
        "port": args.port,
        "requests": requests,
        "payload_size": payload_size,
        "elapsed_seconds": elapsed,
        "requests_per_second": requests / elapsed if elapsed else 0,
        "latency_ms": {
            "min": min(latencies_ms),
            "mean": statistics.fmean(latencies_ms),
            "median": statistics.median(latencies_ms),
            "p95": percentile(latencies_ms, 95),
            "p99": percentile(latencies_ms, 99),
            "max": max(latencies_ms),
        },
    }

    out_dir = ROOT / "benchmarks" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "latest.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

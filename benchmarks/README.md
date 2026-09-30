# Benchmarks

Benchmarks are meaningful only after an implementation passes conformance.

The benchmark runner uses the same external-wire approach for every language.
Scenarios define workload, not implementation details.

Example:

```bash
python benchmarks/runners/netlab_benchmark.py   --scenario benchmarks/scenarios/ping-latency.json   --host 127.0.0.1   --port 7000
```

Results are written to `benchmarks/results/` and are ignored by Git by default.

When publishing benchmark results, record hardware, OS, compiler/runtime
versions, build mode and scenario file.

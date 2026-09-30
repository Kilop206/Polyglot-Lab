# Running Benchmarks

First verify conformance.

Then:

```bash
python benchmarks/runners/netlab_benchmark.py   --scenario benchmarks/scenarios/ping-latency.json
```

For publishable comparisons, keep constant:

- hardware;
- operating system;
- network path;
- benchmark scenario;
- compiler/runtime optimization mode;
- server configuration.

Record compiler/runtime versions with the report.

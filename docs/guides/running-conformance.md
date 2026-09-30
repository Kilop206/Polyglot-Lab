# Running Conformance

Start a server on port 7000, then:

```bash
python conformance/runner/netlab_conformance.py
```

Run one scenario:

```bash
python conformance/runner/netlab_conformance.py --scenario ping
```

Start the server through the runner:

```bash
python conformance/runner/netlab_conformance.py   --server-command "./netlab-server --port 7000"
```

Inspect `conformance/reports/latest.json` after execution.

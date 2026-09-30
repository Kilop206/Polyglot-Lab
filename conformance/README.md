# Conformance Suite

The conformance suite tests a running NetLab server as an external black box.

It is intentionally language-neutral. The Python code here is tooling only; it
is not a production NetLab implementation.

Run against an already running server:

```bash
python conformance/runner/netlab_conformance.py --host 127.0.0.1 --port 7000
```

Or let the runner start a server process:

```bash
python conformance/runner/netlab_conformance.py   --server-command "./path/to/netlab-server --port 7000"
```

Reports are written to `conformance/reports/`.

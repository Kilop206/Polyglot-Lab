.PHONY: validate conformance benchmark clean

validate:
	python scripts/dev/validate-repo.py

conformance:
	python conformance/runner/netlab_conformance.py --host 127.0.0.1 --port 7000

benchmark:
	python benchmarks/runners/netlab_benchmark.py --scenario benchmarks/scenarios/ping-latency.json

clean:
	python scripts/dev/clean.py

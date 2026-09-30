# NetLab

**NetLab** is a multilingual laboratory for learning networking, protocol design,
systems programming, concurrency and library/framework trade-offs.

The project defines one protocol specification and expects every language
implementation to interoperate with every other implementation.

The repository is intentionally split between **normative protocol material**,
**test data**, **conformance tooling**, **benchmarks**, **automation** and
**educational documentation**. Product implementations live only under
`implementations/`.

## Goals

- Learn TCP/IP programming beyond high-level HTTP abstractions.
- Design and evolve a custom binary-framed protocol.
- Compare low-level and framework/library-based implementations.
- Keep C++, Rust, Go and future languages interoperable.
- Measure latency, throughput, memory use and implementation complexity.
- Make protocol behavior reproducible through shared vectors and conformance tests.

## Repository layout

```text
netlab/
├── spec/             # Normative protocol specification
├── test-vectors/     # Official valid and invalid wire examples
├── implementations/  # Language implementations (intentionally not generated here)
├── conformance/      # Cross-language protocol conformance runner
├── benchmarks/       # Fair, repeatable benchmark definitions
├── scripts/          # Build/test/development automation
├── docs/             # Architecture, concepts, ADRs, guides and roadmap
└── .github/          # CI workflows and contribution templates
```

## NetLab Protocol v0.1

Transport: **TCP**

Every frame begins with a fixed 14-byte header:

```text
Offset  Size  Field
0       2     Magic = "NL"
2       1     Version = 0x01
3       1     Message type
4       2     Flags = 0x0000
6       4     Payload length (uint32, big-endian)
10      4     Request ID (uint32, big-endian)
14      N     Payload
```

Multibyte integers use **network byte order (big-endian)**.

Initial messages:

| Code | Message |
|---:|---|
| `0x01` | `HELLO` |
| `0x02` | `HELLO_ACK` |
| `0x10` | `PING` |
| `0x11` | `PONG` |
| `0x20` | `ECHO` |
| `0x21` | `ECHO_RESULT` |
| `0x30` | `INFO` |
| `0x31` | `INFO_RESULT` |
| `0xFF` | `ERROR` |

See [`spec/`](spec/) for normative behavior.

## First implementation target

A conforming v0.1 server should:

1. listen on TCP port `7000` by default;
2. require `HELLO` as the first valid application frame;
3. return `HELLO_ACK` using the same `request_id`;
4. respond to `PING`, `ECHO` and `INFO`;
5. reject malformed or invalid frames with a defined `ERROR` whenever possible;
6. handle TCP fragmentation and multiple frames in a single read;
7. enforce the 1 MiB payload limit.

A conforming client should perform the handshake and correlate responses through
`request_id`.

## Interoperability target

The project is successful only when implementations can be mixed:

```text
C++ client  -> Rust server
Rust client -> Go server
Go client   -> C++ server
...
```

No implementation may rely on language-specific wire behavior.

## Tooling

Validate repository metadata and official test vectors:

```bash
python scripts/dev/validate-repo.py
```

Run conformance tests against a server already listening on `127.0.0.1:7000`:

```bash
python conformance/runner/netlab_conformance.py --host 127.0.0.1 --port 7000
```

Run the default benchmark suite:

```bash
python benchmarks/runners/netlab_benchmark.py \
  --scenario benchmarks/scenarios/ping-latency.json
```

## Adding a language

Read [`docs/guides/adding-a-language.md`](docs/guides/adding-a-language.md).
The implementation must follow the specification, pass official test vectors
and pass conformance tests before benchmark results are considered meaningful.

## Status

Current protocol target: **v0.1**

The repository scaffolding, specification, vectors and tooling are ready.
Language implementations are intentionally left for the learning exercise.

## License

MIT. See [`LICENSE`](LICENSE).

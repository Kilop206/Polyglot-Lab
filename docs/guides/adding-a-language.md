# Adding a Language

Create a directory under `implementations/<language>/`.

Recommended variants:

```text
implementations/<language>/
├── raw/
└── framework/
```

Names may differ when the language's ecosystem makes another distinction more
useful.

## Required work

1. Implement header encode/decode from `spec/framing.md`.
2. Pass all official valid and invalid test vectors.
3. Implement client and server behavior from `spec/messages.md`.
4. Implement the state machine.
5. Run the conformance suite.
6. Test interoperability with at least one other language.
7. Only then publish benchmark results.

Do not copy a different implementation line-for-line. The learning goal is to
express the same protocol idiomatically in each ecosystem.

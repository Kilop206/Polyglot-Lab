# Contributing

NetLab accepts protocol, tooling, documentation and implementation
contributions.

## Before opening a pull request

1. Read the normative documents in `spec/`.
2. Run `python scripts/dev/validate-repo.py`.
3. Run relevant language tests.
4. Run conformance tests for protocol-affecting changes.
5. Update documentation and test vectors when wire behavior changes.

## Protocol changes

Any change that modifies bytes on the wire, message semantics, state transitions,
limits, error behavior or compatibility rules must include:

- a specification update;
- an ADR when the decision is architectural;
- valid/invalid test vectors;
- updated conformance scenarios;
- a versioning assessment.

Do not change the protocol by modifying one implementation only.

## Pull requests

Keep changes focused. Explain:

- what changes;
- why it changes;
- whether the wire format changes;
- compatibility impact;
- tests performed.

## Implementations

New implementations should follow
`docs/guides/adding-a-language.md`.

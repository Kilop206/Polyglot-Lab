# Versioning

NetLab uses two related version concepts:

- repository/software version, such as `0.1.0`;
- wire protocol version, stored as one byte in every frame.

Protocol v0.1 uses wire version `0x01`.

## Compatibility rule

A change is protocol-breaking when it changes:

- header field positions or sizes;
- byte order;
- existing message codes;
- existing payload interpretation;
- mandatory state transitions;
- error semantics in a way that breaks conforming peers.

Breaking wire changes require a new wire protocol version.

Additive tooling, documentation and benchmark changes do not require a new
wire version.

## Unknown versions

A v0.1 peer receiving another wire version SHOULD return
`UNSUPPORTED_VERSION` when the header can safely be parsed, then MAY close the
connection.

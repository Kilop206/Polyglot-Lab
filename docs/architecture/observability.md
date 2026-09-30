# Observability

Implementations should expose development-time diagnostics for:

- accepted/closed connections;
- decoded message type;
- request ID;
- payload length;
- protocol errors;
- handler latency.

Logs must not be part of the wire protocol.

Future benchmark work can add standardized metrics, but v0.1 keeps observability
implementation-specific.

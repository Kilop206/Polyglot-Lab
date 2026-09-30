# Client Architecture

Recommended modules:

```text
CLI/API
  -> Connection
  -> Request manager
  -> Encoder/decoder
  -> Socket
```

The request manager owns request ID generation and response correlation.

A synchronous first implementation is acceptable. Async/pipelined behavior can
be added later without changing the protocol.

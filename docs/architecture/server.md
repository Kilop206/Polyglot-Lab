# Server Architecture

Recommended flow:

```text
accept
 -> connection context
 -> buffered reader
 -> frame decoder
 -> state validation
 -> dispatcher
 -> handler
 -> response encoder
 -> socket write
```

Handlers should not parse raw TCP bytes. Parsing and message semantics should be
testable independently.

# Protocol Stack

```text
Application command
      ↓
Message validation
      ↓
Encoder / Decoder
      ↓
Frame parser
      ↓
Buffered TCP I/O
      ↓
Operating-system socket
```

Keep these responsibilities separable. A framework-based implementation may
combine layers internally, but its observable wire behavior must remain the
same.

The decoder should not contain business behavior such as PING handling. The
dispatcher should receive already validated frames.

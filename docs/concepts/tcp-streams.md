# TCP Streams

TCP transports an ordered byte stream, not application messages.

If a sender writes two frames, the receiver may observe one read, many reads or
any split between them. Correct framing therefore requires buffering.

Never write logic equivalent to:

```text
recv() == one NetLab frame
```

Instead, accumulate bytes and decode frames while enough bytes are available.

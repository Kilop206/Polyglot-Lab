# Capabilities

Capabilities are reserved for a future protocol version.

v0.1 does not negotiate optional features. Implementations MUST NOT infer
support for compression, file transfer, authentication, multiplexing or RPC.

Provisional future capability bits:

| Bit | Name |
|---:|---|
| `0x00000001` | Compression |
| `0x00000002` | File transfer |
| `0x00000004` | Authentication |
| `0x00000008` | Multiplexing |

These values are informative until a later specification promotes them to
normative status.

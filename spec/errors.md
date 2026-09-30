# Error Registry

| Code | Name | Meaning |
|---:|---|---|
| `0x0001` | `INVALID_MAGIC` | Header magic is not `NL` |
| `0x0002` | `UNSUPPORTED_VERSION` | Frame version is unsupported |
| `0x0003` | `INVALID_MESSAGE_TYPE` | Message type is unknown or invalid |
| `0x0004` | `INVALID_LENGTH` | Length is inconsistent with message rules |
| `0x0005` | `PAYLOAD_TOO_LARGE` | Declared payload exceeds 1 MiB |
| `0x0006` | `MALFORMED_PAYLOAD` | Payload cannot be interpreted as required |
| `0x0007` | `INVALID_STATE` | Message is invalid in the current connection state |
| `0x0008` | `INVALID_FLAGS` | Reserved flags are non-zero |

## Error handling

When a request ID is known, an `ERROR` SHOULD preserve it.

For framing failures that make request correlation impossible, request ID `0`
MAY be used.

An implementation MAY close the connection after protocol errors, especially
when continuing would make framing ambiguous.

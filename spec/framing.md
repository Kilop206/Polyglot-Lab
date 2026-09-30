# Framing

## Fixed header

Each frame starts with exactly 14 bytes.

| Offset | Size | Type | Field | v0.1 value/meaning |
|---:|---:|---|---|---|
| 0 | 2 | bytes | Magic | ASCII `NL` (`4E 4C`) |
| 2 | 1 | uint8 | Version | `0x01` |
| 3 | 1 | uint8 | Message Type | See `messages.md` |
| 4 | 2 | uint16 | Flags | `0x0000` |
| 6 | 4 | uint32 | Payload Length | Big-endian, max 1 MiB |
| 10 | 4 | uint32 | Request ID | Big-endian |
| 14 | N | bytes | Payload | Message-specific |

Total frame size:

```text
14 + payload_length
```

## Decode order

A decoder SHOULD:

1. buffer until at least 14 bytes are available;
2. validate magic;
3. validate version;
4. validate flags;
5. read payload length;
6. reject length above 1 MiB;
7. buffer until `14 + payload_length` bytes are available;
8. extract exactly one frame;
9. leave additional buffered bytes for the next frame.

## Example: PING request ID 42

```text
4E 4C 01 10 00 00 00 00 00 00 00 00 00 2A
```

Breakdown:

```text
4E 4C       magic "NL"
01          version
10          PING
00 00       flags
00 00 00 00 payload length
00 00 00 2A request ID = 42
```

## Invalid length

A header declaring more than 1 MiB MUST be rejected immediately.
A connection MAY be closed after the corresponding error is sent.

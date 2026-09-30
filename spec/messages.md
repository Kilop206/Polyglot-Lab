# Messages

## Registry

| Code | Name | Direction | Payload |
|---:|---|---|---|
| `0x01` | `HELLO` | Client -> Server | UTF-8 implementation name |
| `0x02` | `HELLO_ACK` | Server -> Client | UTF-8 implementation name |
| `0x10` | `PING` | Client -> Server | Empty |
| `0x11` | `PONG` | Server -> Client | Empty |
| `0x20` | `ECHO` | Client -> Server | Opaque bytes |
| `0x21` | `ECHO_RESULT` | Server -> Client | Exact opaque bytes from request |
| `0x30` | `INFO` | Client -> Server | Empty |
| `0x31` | `INFO_RESULT` | Server -> Client | UTF-8 JSON |
| `0xFF` | `ERROR` | Either direction | Error code + UTF-8 message |

Unknown message types MUST result in `INVALID_MESSAGE_TYPE` when a valid frame
can otherwise be parsed.

## HELLO

Payload: non-empty UTF-8 implementation identifier, maximum 64 bytes.

Examples:

```text
cpp-raw
rust-std
go-std
```

The server responds with `HELLO_ACK`, preserving the request ID.

## PING

Payload MUST be empty.

The server responds with empty `PONG`.

## ECHO

Payload is any byte sequence from 0 to 1 MiB.

The server MUST respond with `ECHO_RESULT` containing exactly the same payload
bytes.

## INFO

Request payload MUST be empty.

`INFO_RESULT` payload MUST be a UTF-8 encoded JSON object containing at least:

```json
{
  "implementation": "rust-std",
  "protocol_version": 1,
  "uptime_ms": 12345,
  "active_connections": 1
}
```

Additional fields are allowed.

## ERROR

Payload:

```text
0..1   uint16 error code, big-endian
2..N   UTF-8 human-readable message
```

The message is diagnostic and MUST NOT be parsed as a stable machine identifier.
Use the numeric error code for logic.

# NetLab Protocol v0.1

## 1. Purpose

NetLab Protocol is a compact educational application protocol designed to
exercise TCP networking, binary framing, parsing, request/response correlation,
error handling and cross-language interoperability.

## 2. Transport

Version 0.1 uses TCP.

Default TCP port: `7000`.

The port is configurable and is not part of the wire protocol.

## 3. Connection lifecycle

A normal connection is:

```text
TCP connect
  -> HELLO
  <- HELLO_ACK
  -> requests
  <- responses
  -> TCP close
```

`HELLO` MUST be the first valid application frame sent by the client.
A server MUST NOT process ordinary requests before the handshake completes.

## 4. Byte order

All multibyte integer fields MUST use big-endian byte order.

## 5. Encoding

The frame header is binary.

Message payload encoding depends on the message type. Text payloads MUST use
UTF-8. `ECHO` payloads are opaque bytes and need not be text.

## 6. Request IDs

Client requests MUST use a non-zero 32-bit request ID.

A direct response MUST copy the request ID of its request.

A server-generated error that cannot be associated with a request MAY use
request ID `0`.

Clients SHOULD avoid reusing a request ID while a previous request with that ID
is still outstanding.

## 7. Limits

Maximum payload length: `1,048,576` bytes (1 MiB).

An implementation MUST reject frames whose declared payload exceeds this limit
without allocating memory proportional to the declared value.

## 8. Flags

All flags are reserved in v0.1.

Clients MUST send `0x0000`.
Servers MUST reject non-zero flags with `INVALID_FLAGS`.

## 9. TCP semantics

TCP is a byte stream. Implementations MUST NOT assume that one `send` equals one
`recv`.

A frame may arrive in multiple reads. Multiple frames may arrive in one read.
Parsers MUST preserve incomplete bytes until enough data exists to decode a
complete frame.

## 10. Security

v0.1 has no authentication, encryption or integrity protection.
See `security-considerations.md`.

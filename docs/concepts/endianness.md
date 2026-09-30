# Endianness

A multibyte integer can be represented in different byte orders.

NetLab uses big-endian (network byte order).

For value `42` as uint32:

```text
00 00 00 2A
```

Every implementation must convert explicitly rather than relying on host
endianness.

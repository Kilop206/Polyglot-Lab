# Debugging the Protocol

Useful workflow:

1. capture the exact frame as hexadecimal bytes;
2. compare the first 14 bytes with `spec/framing.md`;
3. verify big-endian length and request ID;
4. compare against `test-vectors/`;
5. check connection state;
6. verify that partial reads are buffered;
7. verify that trailing bytes are preserved.

A hex dump is often more useful than a high-level log for interoperability
bugs.

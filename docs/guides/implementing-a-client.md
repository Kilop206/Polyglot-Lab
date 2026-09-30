# Implementing a Client

Minimum sequence:

1. open TCP connection;
2. send `HELLO` with non-zero request ID;
3. receive matching `HELLO_ACK`;
4. generate request IDs;
5. send `PING`, `ECHO` or `INFO`;
6. read complete framed responses;
7. correlate `request_id`;
8. handle `ERROR`;
9. close cleanly.

Start synchronously. Add pipelining or async behavior only after the baseline is
correct.

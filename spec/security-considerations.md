# Security Considerations

Protocol v0.1 is intentionally minimal and must not be considered secure for
untrusted production networks.

## No confidentiality

Payloads are plaintext.

## No authentication

Any reachable peer can identify itself using any implementation name.

## No integrity protection

TCP detects transport corruption but does not provide application-level peer
authentication or cryptographic integrity.

## Denial of service

Implementations MUST validate the declared payload length before allocating a
payload-sized buffer. The 1 MiB limit is mandatory.

Servers SHOULD define sensible connection, idle and read timeouts even though
specific timeout values are implementation policy in v0.1.

## Parser safety

Implementations should prefer bounded arithmetic and avoid integer overflow when
computing `HEADER_SIZE + payload_length`.

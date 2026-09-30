# UDP Datagrams

UDP preserves datagram boundaries, unlike TCP, but does not provide reliable,
ordered delivery.

NetLab v0.1 does not use UDP. A later version may use UDP for discovery,
telemetry or experiments. Such additions must define their own loss,
duplication and ordering semantics.

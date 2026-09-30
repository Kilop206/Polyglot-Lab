# Buffers

A receive buffer holds bytes that have arrived but do not yet form complete
frames.

A robust parser should:

1. avoid discarding incomplete bytes;
2. avoid repeated unbounded allocations;
3. consume exactly one complete frame at a time;
4. preserve trailing bytes for later decoding;
5. enforce the payload limit before allocating a payload-sized buffer.

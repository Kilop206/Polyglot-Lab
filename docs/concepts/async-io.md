# Async I/O

Async I/O is an implementation technique, not a protocol feature.

Compare a low-level blocking implementation against an async/library version
only after both pass the same conformance suite. This prevents throughput gains
from hiding wire incompatibilities.

# ADR: Use big-endian integers

## Status

Accepted

## Context

Implementations may run on architectures with different native byte order.

## Decision

Encode all multibyte integers in network byte order.

## Consequences

Every language must convert explicitly, making wire bytes portable.

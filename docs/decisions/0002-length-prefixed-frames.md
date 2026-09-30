# ADR: Use length-prefixed frames

## Status

Accepted

## Context

TCP does not preserve application message boundaries.

## Decision

Use a fixed header with a uint32 payload length.

## Consequences

Parsers can handle fragmentation and coalescing deterministically.

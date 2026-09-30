# ADR: Use a 14-byte fixed header

## Status

Accepted

## Context

The first protocol version should be easy to inspect and parse.

## Decision

Use magic, version, type, flags, length and request ID in a fixed 14-byte header.

## Consequences

Parsing is simple at the cost of a small constant overhead per frame.

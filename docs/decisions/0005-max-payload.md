# ADR: Limit payloads to 1 MiB

## Status

Accepted

## Context

Unbounded declared lengths can cause excessive memory allocation and denial of service.

## Decision

Reject payload lengths greater than 1,048,576 bytes.

## Consequences

Large transfers will later require chunking rather than one oversized frame.

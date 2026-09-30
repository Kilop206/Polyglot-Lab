# ADR: Use a custom protocol

## Status

Accepted

## Context

NetLab exists to expose framing, parsing and protocol decisions that HTTP frameworks often hide.

## Decision

Define a small custom application protocol over TCP.

## Consequences

More protocol code must be written, but the project directly exercises the intended systems concepts.

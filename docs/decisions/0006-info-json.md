# ADR: Use JSON for INFO_RESULT

## Status

Accepted

## Context

INFO is diagnostic and benefits from extensible fields.

## Decision

Encode INFO_RESULT as UTF-8 JSON while keeping the transport frame binary.

## Consequences

Implementations exercise a common serialization library and may add fields without changing the header.

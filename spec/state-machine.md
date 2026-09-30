# Connection State Machine

## Server states

```text
CONNECTED
   |
   | valid HELLO
   v
READY
   |
   | TCP close / fatal protocol error
   v
CLOSED
```

## CONNECTED

Allowed:

- `HELLO`

All other valid message types MUST produce `INVALID_STATE`.

## READY

Allowed client requests:

- `PING`
- `ECHO`
- `INFO`

A second `HELLO` MUST produce `INVALID_STATE`.

## CLOSED

No application processing occurs.

## Client behavior

A client MUST wait for `HELLO_ACK` before treating the connection as ready.

A client SHOULD treat a mismatched request ID or unexpected response type as a
protocol failure.

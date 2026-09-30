# Concurrency

Protocol v0.1 does not mandate a concurrency model.

Possible implementations:

- one thread per connection;
- fixed worker pool;
- event loop;
- async runtime;
- OS-specific I/O completion mechanisms.

Benchmark concurrency models separately and document the model used. Do not
alter protocol semantics merely to fit a framework.

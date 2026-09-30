# Threading

Thread-per-connection is often the easiest server architecture to understand.
Worker pools and event loops can scale differently.

Use NetLab to compare:

- implementation complexity;
- synchronization needs;
- memory per connection;
- latency under load;
- shutdown behavior.

# Implementing a Server

Minimum sequence:

1. bind/listen on a configurable TCP port;
2. accept a connection;
3. maintain connection state;
4. buffer stream bytes;
5. decode complete frames;
6. validate header, limits and state;
7. dispatch messages;
8. encode responses;
9. keep reading until close or fatal error.

Do not assume reads align with frames. Use the fragmented-frame conformance
scenario during development.

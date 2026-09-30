# Serialization

Serialization converts in-memory values into wire bytes.

NetLab v0.1 deliberately mixes:

- fixed-width binary header fields;
- UTF-8 text for selected messages;
- opaque bytes for ECHO;
- UTF-8 JSON for INFO_RESULT.

This exposes implementations to multiple data representation tasks without
requiring a full schema compiler.

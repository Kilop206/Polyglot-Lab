# Security Policy

NetLab is an educational protocol laboratory and is not intended for production
security-sensitive deployment.

## Reporting

Do not publish exploit details for a newly discovered repository-specific
vulnerability before maintainers have had a reasonable opportunity to review it.
Use a private maintainer contact when one is available.

## Scope

Security-relevant issues include:

- memory-safety defects in implementations;
- denial-of-service from malformed frames;
- payload-length bypasses;
- state-machine bypasses;
- unsafe benchmark/conformance command execution.

Protocol v0.1 does **not** provide confidentiality, integrity, authentication or
replay protection. Those properties are planned for later versions.

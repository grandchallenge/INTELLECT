# Security

Do not report security-sensitive details in public issues. Use the repository owner's private security reporting channel when available.

The current foundation is not approved for safety-critical autonomous deployment. It does not bundle secret management, model sandboxing, cryptographic artifact verification, distributed consensus, or live execution fencing.

Credentials must be supplied through process configuration. They must never be placed in event payloads, examples, tests, or committed configuration.

See `docs/THREAT_MODEL.md` for the current analysis.

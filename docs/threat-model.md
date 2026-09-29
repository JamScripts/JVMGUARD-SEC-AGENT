# JVMGuard Threat Model

## Goal

JVMGuard explores whether an independent controller can reduce risk when an AI agent proposes tool actions based on user input or eventually untrusted external content.

## Assets to protect

- Local files and secrets
- Credentials and tokens
- Tool execution authority
- Host integrity
- User intent
- Security logs and provenance metadata

## Threats in scope

- Prompt injection
- Indirect prompt injection
- Unauthorized tool use
- Sensitive-resource access
- Data exfiltration attempts
- Privilege-escalation indicators
- Agent behavior that diverges from the user's stated goal

## Trust boundaries

The language model is not treated as an authorization authority. Tool proposals cross a trust boundary into the JVMGuard controller before execution.

Version 0.4 includes `source` and `trust_level` metadata, but these values are not yet independently verified and should be considered prototype metadata.

## Out of scope for v0.4

- Production-grade sandboxing
- Strong identity or cryptographic provenance
- Network isolation
- Multi-tenant isolation
- Complete prompt-injection detection
- Automated risk-based execution policy
- Formal verification

## Security assumption

Tests should run only in controlled environments with synthetic secrets and non-destructive tools unless the operator has explicit authorization and isolation appropriate for the experiment.

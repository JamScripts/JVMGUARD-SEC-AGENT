# Security Policy

JVMGuard is an experimental research project and is not production-ready security software.

## Safe testing scope

Use JVMGuard only with controlled environments, synthetic credentials, synthetic secrets, sandboxed files, and systems you are authorized to test.

Do not use destructive test cases against production systems, real credentials, or third-party infrastructure without explicit authorization.

## Reporting a vulnerability

If you discover a vulnerability in JVMGuard itself, avoid posting exploit details publicly before the issue is understood. Contact the repository owner through GitHub with a concise description, affected version, reproduction steps, impact, and any suggested mitigation.

## Current security limitations

Version 0.4 provides action interception, deterministic risk scoring, and explicit tool allowlisting. Risk scores are informational in v0.4 and are not yet connected to the final execution policy. Provenance and trust metadata are also currently limited and should not be treated as production-grade verification.

# JVMGuard Architecture

## v0.4 execution path

1. The user gives the local agent a goal.
2. The Ollama-backed language model may propose a tool call.
3. JVMGuard converts the proposal into an `ActionRequest`.
4. The deterministic risk engine evaluates explicit signals in the action metadata and arguments.
5. The controller checks whether the requested tool is explicitly registered and allowlisted.
6. Unauthorized tools are blocked. Authorized tools may execute.
7. Tool output is returned to the agent loop.

The core design rule is that the language model proposes actions but does not directly own execution authority.

## Current modules

- `jvmguard.agent`: agent loop, tool registry, interception, and v0.4 authorization flow.
- `jvmguard.security.action`: structured `ActionRequest` representation.
- `jvmguard.security.risk`: deterministic risk assessment.
- `jvmguard.tools.system_info`: current read-only system-information tool.

## Current boundary

Version 0.4 intentionally keeps risk assessment separate from execution policy. A dedicated policy engine is planned for v0.5 and is not part of this cleanup branch.

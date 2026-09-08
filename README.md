# JVMGuard

JVMGuard is an experimental runtime security layer for AI agents. It explores how agent-proposed tool actions can be intercepted, structured, risk-scored, authorized, blocked, and eventually logged before execution.

> Status: early-stage research prototype. APIs, policies, and risk rules will change as the project develops.

## Current version

**v0.4.0**

Current capabilities:

- Local Ollama-powered agent
- Tool calling with controller-owned execution authority
- Runtime interception of proposed tool calls
- Structured `ActionRequest` objects
- User-goal, source, trust, and timestamp metadata
- Explicit tool allowlisting
- Deterministic risk scoring
- Explainable risk reasons
- Real local system-information tool

## Security model

```text
User
  |
  v
Local AI Agent
  |
  | proposes tool call
  v
JVMGuard Controller
  |
  v
ActionRequest
  |
  v
Deterministic Risk Engine
  |
  v
Current Allowlist Check
  |
  +--> BLOCK unauthorized tools
  |
  +--> ALLOW authorized tools
          |
          v
        Tool
```

The language model may propose an action, but it does not directly own execution authority. JVMGuard's controller sits between the model and its tools.

In v0.4, the risk engine calculates risk independently from the language model. Risk score is not yet connected to the final policy decision; v0.5 will address that separately.

## Requirements

Current development target:

- Python 3.13
- `uv`
- Ollama
- Git
- Arch Linux is the primary tested environment

Other operating systems have not yet been fully tested.

## Installation

```bash
git clone https://github.com/JamScripts/JVMGUARD-SEC-AGENT.git
cd JVMGUARD-SEC-AGENT
uv python install 3.13
uv sync
ollama pull qwen3.5:0.8b
```

Make sure the Ollama server is running, then start JVMGuard:

```bash
uv run jvmguard
```

You should see output similar to:

```text
JVMGuard v0.4.0
Model:   qwen3.5:0.8b
Backend: Ollama
```

Example prompt:

```text
Inspect this computer and tell me the hostname and current time.
```

## Project structure

```text
JVMGUARD-SEC-AGENT/
├── README.md
├── SECURITY.md
├── LICENSE
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
├── src/
│   └── jvmguard/
│       ├── __init__.py
│       ├── agent.py
│       ├── security/
│       │   ├── __init__.py
│       │   ├── action.py
│       │   └── risk.py
│       └── tools/
│           ├── __init__.py
│           └── system_info.py
├── tests/
└── docs/
    ├── architecture.md
    └── threat-model.md
```

## v0.4 risk engine

Current deterministic signals include:

- Untrusted action source
- Sensitive-resource references
- Dangerous tool capability
- Privilege-escalation indicators

Risk levels:

```text
0-24    LOW
25-49   MEDIUM
50-74   HIGH
75-100  CRITICAL
```

The current version calculates risk but does not yet enforce policy directly from that score.

## Testing

Run the deterministic test suite with:

```bash
uv run python -m unittest discover -s tests -v
```

The Ollama connectivity check is treated as an integration test and requires a running local Ollama service.

## Roadmap

### v0.5 — Policy Engine

Planned separately:

```text
LOW       -> ALLOW
MEDIUM    -> WARN
HIGH      -> REQUIRE_APPROVAL
CRITICAL  -> BLOCK
```

Longer-term research areas include security event logging, sandboxed filesystem tools, provenance tracking, indirect prompt-injection detection, tool-output inspection, victim/attacker agent testing, benchmarks, evaluation datasets, external agent integrations, and an API/SDK.

## Safety

Use synthetic credentials, synthetic secrets, sandboxed files, and controlled local environments. Do not test destructive actions against production systems or real credentials.

See `SECURITY.md` and `docs/threat-model.md` for the current research boundaries.

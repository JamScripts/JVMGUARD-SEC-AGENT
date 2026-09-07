JVMGuard is an experimental runtime security layer for AI agents.

The project explores how agent actions can be intercepted, inspected,
risk-scored, authorized, blocked, and eventually logged before tools
are allowed to execute.

JVMGuard is currently being developed as a local-first AI security lab
using Python and Ollama.

## Current Version

**JVMGuard v0.4.0**

Current milestone:

- Local Ollama-powered AI agent
- Agent tool calling
- Runtime tool interception
- Structured ActionRequest objects
- User-goal capture
- Source and trust metadata
- Tool allowlisting
- Deterministic risk scoring
- Explainable risk reasons
- Real system information tool

## Current Architecture

```text
User
  |
  v
Local AI Agent
  |
  | proposes tool call
  v
JVMGuard Interceptor
  |
  v
ActionRequest
  |
  +-- Agent
  +-- Tool
  +-- Arguments
  +-- User Goal
  +-- Source
  +-- Trust Level
  +-- Timestamp
  |
  v
Deterministic Risk Engine
  |
  +-- Risk Score
  +-- Risk Level
  +-- Reasons
  |
  v
Current Allowlist Policy
  |
  +-- ALLOW
  |
  v
Authorized Tool

The language model proposes actions.

The language model does not directly own execution authority.

JVMGuard's controller sits between the agent and its tools.

Example

A safe system-information request currently produces an interception
similar to:

JVMGUARD INTERCEPT

Agent:       jvmguard-agent
Tool:        get_system_info
Arguments:   {}
Source:      user
Trust:       trusted

Risk Score:  0/100
Risk Level:  LOW

Decision:    ALLOW
Requirements

The current version has been developed and tested on Arch Linux.

You will need:

Python 3.13
uv
Ollama
Git
Approximately 2 GB of free memory for the default development model

Other operating systems have not yet been fully tested.

Installation
1. Clone the repository
git clone <repository-clone-url>
cd JVMGuard
2. Install or verify uv
uv --version

Install uv using its official installation documentation if it is not
already available.

3. Install Python

The project currently targets Python 3.13.

uv python install 3.13
4. Install project dependencies
uv sync
5. Install and start Ollama

Verify Ollama:

ollama --version

Make sure the Ollama server is running.

6. Download the development model
ollama pull qwen3.5:0.8b

Verify:

ollama list
7. Run JVMGuard
uv run python agent.py

You should see:

JVMGuard v0.4.0
Model: qwen3.5:0.8b
Backend: Ollama

Try:

Inspect this computer and tell me the hostname and current time.
Project Structure
JVMGuard/
├── agent.py
├── pyproject.toml
├── uv.lock
├── .python-version
│
├── security/
│   ├── __init__.py
│   ├── action.py
│   └── risk.py
│
└── tools/
    ├── __init__.py
    └── system_info.py
Risk Engine

JVMGuard v0.4 uses deterministic Python rules rather than asking the
language model to decide whether an action is safe.

Current example signals include:

Untrusted action source
Sensitive resource references
Dangerous tools
Privilege escalation indicators

Risk is currently classified as:

0-24     LOW
25-49    MEDIUM
50-74    HIGH
75-100   CRITICAL

The current version calculates risk but does not yet enforce policy
based directly on the risk score.

Roadmap
v0.5 — Policy Engine

Convert risk assessments into execution decisions:

LOW       -> ALLOW
MEDIUM    -> WARN
HIGH      -> REQUIRE_APPROVAL
CRITICAL  -> BLOCK
Planned Development
Security event logging
Read-only sandboxed filesystem tools
Sensitive-resource classification
Trust and provenance tracking
Indirect prompt-injection detection
Tool-output inspection
Victim-agent testing
Attacker-agent testing
Protected vs. unprotected benchmarks
Security evaluation datasets
External agent integrations
API / SDK
Long-Term Goal

The target JVMGuard scenario is:

An AI agent consumes malicious instructions through an indirect prompt
injection, attempts a dangerous tool action, and JVMGuard intercepts the
action before execution, evaluates its provenance and risk, blocks it,
explains why it was blocked, and records the security event.

Safety

JVMGuard is currently an experimental research and learning project.

Current development should use:

Synthetic credentials
Synthetic secrets
Sandboxed files
Controlled local environments

Do not test destructive actions against production systems or real
credentials.

Status

Early-stage research prototype.

The architecture, APIs, policies, and risk scoring system are expected
to change significantly as the project develops.

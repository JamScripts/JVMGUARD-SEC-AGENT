from dataclasses import asdict, dataclass
from enum import Enum

from jvmguard.security.action import ActionRequest


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class RiskAssessment:
    score: int
    level: RiskLevel
    reasons: list[str]

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["level"] = self.level.value
        return data


SENSITIVE_PATTERNS = [
    ".ssh/id_rsa",
    ".ssh/id_ed25519",
    ".env",
    "api_key",
    "apikey",
    "password",
    "passwd",
    "credential",
    "secret",
    "token",
]

DANGEROUS_TOOLS = [
    "delete_file",
    "execute_shell",
    "run_command",
    "send_data",
    "upload_file",
]


def _flatten_arguments(arguments: dict) -> str:
    return " ".join(f"{key}={value}" for key, value in arguments.items()).lower()


def _level_from_score(score: int) -> RiskLevel:
    if score >= 75:
        return RiskLevel.CRITICAL
    if score >= 50:
        return RiskLevel.HIGH
    if score >= 25:
        return RiskLevel.MEDIUM
    return RiskLevel.LOW


def assess_action(action: ActionRequest) -> RiskAssessment:
    """Assess an action using deterministic v0.4 risk rules."""

    score = 0
    reasons: list[str] = []
    argument_text = _flatten_arguments(action.arguments)

    if action.trust_level.lower() == "untrusted":
        score += 25
        reasons.append("Action originated from an untrusted source.")

    for pattern in SENSITIVE_PATTERNS:
        if pattern in argument_text:
            score += 45
            reasons.append(
                f"Action references sensitive resource pattern: {pattern}"
            )
            break

    if action.tool in DANGEROUS_TOOLS:
        score += 40
        reasons.append(
            f"Tool '{action.tool}' is classified as a dangerous capability."
        )

    if "sudo" in argument_text:
        score += 40
        reasons.append("Action contains privilege-escalation behavior.")

    score = min(score, 100)

    if not reasons:
        reasons.append("No significant deterministic risk indicators detected.")

    return RiskAssessment(
        score=score,
        level=_level_from_score(score),
        reasons=reasons,
    )

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class ActionRequest:
    """Structured representation of an agent-requested tool action."""

    agent: str
    tool: str
    arguments: dict[str, Any]
    user_goal: str = ""
    source: str = "user"
    trust_level: str = "trusted"
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

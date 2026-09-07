from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any


@dataclass
class ActionRequest:
    agent: str
    tool: str
    arguments: dict[str, Any]

    user_goal: str = ""
    source: str = "user"
    trust_level: str = "trusted"

    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self):
        return asdict(self)

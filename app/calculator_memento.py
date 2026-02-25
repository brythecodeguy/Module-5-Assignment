from dataclasses import dataclass, field
import datetime
from typing import Any, Dict, List

from app.calculation import Calculation


@dataclass
class CalculatorMemento:
    history: List[Calculation]
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "history": [c.to_dict() for c in self.history],
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CalculatorMemento":
        return cls(
            history=[Calculation.from_dict(x) for x in data["history"]],
            timestamp=datetime.datetime.fromisoformat(data["timestamp"]),
        )
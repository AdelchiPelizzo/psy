from dataclasses import dataclass

@dataclass
class UserFrame:
    # topic: str
    claim: str
    # emotion: str
    confidence: float | None = None

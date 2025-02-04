from dataclasses import dataclass
from typing import Dict, Any, Optional, List

@dataclass
class ProcessingResult:
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None
    raw_response: Optional[str] = None

@dataclass
class LTLResult:
    formula: str
    atomic_propositions: List[str]
    success: bool
    error: Optional[str] = None

@dataclass
class WindowInfo:
    window_start: int
    window_end: int
    current_action: str
    current_index: int
    previous_actions: List[str]
    next_actions: List[str]
    full_window: List[str]
"""Module with the base Step abstraction."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Step(ABC):
    """Abstract interface for the step, an unit of work."""

    def __init__(
        self,
        name: str,
        path: str,
        depends_on: List[str] = None,
        inputs: Dict[str, Any] = None,
        outputs: List[str] = None
    ) -> None:
        """Initialize attributes for the step."""
        self.name = name
        self.path = path
        self.depends_on = depends_on or []
        self.inputs = inputs or {}
        self.outputs = outputs or []

    @abstractmethod
    def execute(self, inputs_override: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the step and return a dictionary with the outputs."""

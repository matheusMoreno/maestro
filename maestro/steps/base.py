"""Module with the base Step abstraction."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, List


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

    def execute(self, inputs_override: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the step and return a dictionary with the outputs."""
        outputs_values = self._execute(inputs_override)
        return self._pack_outputs(outputs_values)

    def _pack_outputs(self, outputs: Any) -> Dict[str, Any]:
        """Pack outputs into the desired output mapping."""
        outputs = outputs if isinstance(outputs, Iterable) else [outputs]
        return dict(zip(self.outputs, outputs))

    @abstractmethod
    def _execute(self, inputs_override: Dict[str, Any]) -> Any:
        """Execute the step and return the raw outputs."""

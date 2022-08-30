"""Module with factory method for building steps."""

from typing import Any, Callable, Dict

from maestro.steps.base import Step


class StepFactory:
    """Step factory abstraction."""

    def __init__(self) -> None:
        """Initialize step types dictionary."""
        self._step_types: Dict[str, Callable] = {}

    def register(self, step_type: str, step_obj: Callable) -> None:
        """Register type class."""
        self._step_types[step_type] = step_obj

    def create(self, step_spec: Dict[str, Any]) -> Step:
        """Create a step class based on its type."""
        try:
            step_type = step_spec.pop("type")
            step_class = self._step_types[step_type]
        except ValueError as exc:
            raise TypeError(f"Step type {step_type} does not exist.") from exc

        return step_class(**step_spec)

"""Module with factory method for building steps."""

import logging
from typing import Any, Callable, Dict

from maestro.steps.base import Step


LOGGER = logging.getLogger(__name__)


class StepFactory:
    """Step factory abstraction."""

    def __init__(self) -> None:
        """Initialize step types dictionary."""
        self.step_types: Dict[str, Callable] = {}

    def register(self, step_type: str, step_obj: Callable) -> None:
        """Register type class."""
        LOGGER.debug("Registering step of type %s.", step_type)
        self.step_types[step_type] = step_obj

    def create(self, step_spec: Dict[str, Any]) -> Step:
        """Create a step class based on its type."""
        try:
            step_spec = step_spec.copy()
            step_type = step_spec.pop("type")
            step_class = self.step_types[step_type]
        except KeyError as exc:
            raise TypeError(f"Step type {step_type} does not exist.") from exc

        LOGGER.debug("Building step %s with params %s.", step_type, step_spec)
        return step_class(**step_spec)

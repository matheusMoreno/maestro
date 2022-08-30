"""Module with the Python function step implementation."""

from __future__ import annotations
from importlib import import_module
import logging
from typing import Any, Callable, Dict, Tuple

from maestro.steps.base import Step
from maestro.exceptions import FailedStepException


LOGGER = logging.getLogger(__name__)


class PythonStep(Step):
    """Step that executes a Python function."""

    def _execute(self, inputs_override: Dict[str, Any]) -> Any:
        """Execute a Python function based on it's path."""
        inputs = {**self.inputs, **inputs_override}
        LOGGER.debug("Running function %s with inputs %s.", self.path, inputs)

        try:
            function = self._import_function()
            outputs_values = function(*inputs.values())
            LOGGER.info("Function %s ran successfully.", self.path)
            return outputs_values
        except Exception as exc:  # pylint: disable=broad-except
            LOGGER.error("Fuction %s failed: %s", self.path, str(exc))
            raise FailedStepException(str(exc)) from exc

    def _import_function(self) -> Callable:
        """Get the function object from a Python path."""
        module_path, function_name = self._get_function_module_and_name()
        module = import_module(module_path)
        return getattr(module, function_name)

    def _get_function_module_and_name(self) -> Tuple[str, str]:
        """Split Python path into the full module path and function name."""
        *submodules, function_name = self.path.split('.')
        return '.'.join(submodules), function_name

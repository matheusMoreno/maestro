"""Module with the Python function step implementation."""

from __future__ import annotations
from importlib import import_module
import logging
from typing import Any, Dict, Iterable, Tuple

from maestro.steps.base import Step
from maestro.exceptions import FailedStepException


LOGGER = logging.getLogger(__name__)


class PythonStep(Step):
    """Step that executes a Python function."""

    def execute(self, inputs_override: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a Python function based on it's path."""
        module_path, function_name = self._get_function_module_and_name()
        inputs = {**self.inputs, **inputs_override}
        LOGGER.debug(
            "Running Python function %s from module %s with inputs %s.",
            function_name, module_path, inputs
        )

        try:
            module = import_module(module_path)
            function = getattr(module, function_name)
            outputs_values = function(*inputs.values())
        except Exception as exc:  # pylint: disable=broad-except
            raise FailedStepException(str(exc)) from exc

        if not isinstance(outputs_values, Iterable):
            outputs_values = [outputs_values]

        LOGGER.debug("Fuction %s ran successfully.", function_name)
        return dict(zip(self.outputs, outputs_values))

    def _get_function_module_and_name(self) -> Tuple[str, str]:
        """Split Python path into the full module path and function name."""
        *submodules, function_name = self.path.split('.')
        return '.'.join(submodules), function_name

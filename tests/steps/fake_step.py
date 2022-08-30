"""Module with FakeStep class for testing purposes."""

from typing import Any, Dict

from maestro.steps import Step


class FakeStep(Step):
    """Fake implementation of a Step class for testing purposes."""

    def _execute(self, inputs_update: Dict[str, Any] = None) -> Any:
        """Return the value in the 'outputs' key."""
        return inputs_update["outputs"] if inputs_update else None

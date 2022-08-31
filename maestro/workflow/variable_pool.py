"""Module with the variable pool abstraction."""

import logging
from typing import Any, Dict


LOGGER = logging.getLogger(__name__)


class VariablePool:
    """The variable pool stores paths and values for workflow variables."""

    def __init__(self) -> None:
        """Initialize object with an empty pool."""
        self._pool: Dict[str, Any] = {}

    def set_inputs(self, entity_name: str, inputs: Dict[str, Any]) -> None:
        """Update pool with inputs of a given entity."""
        self._set_values(entity_name, "inputs", inputs)

    def set_outputs(self, entity_name: str, outputs: Dict[str, Any]) -> None:
        """Update pool with outputs of a given entity."""
        self._set_values(entity_name, "outputs", outputs)

    def get_values(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve a dictionary of variables with possible references."""
        return {
            name: self._pool.get(value, value)
            for name, value in variables.items()
        }

    def _set_values(
        self, entity: str, interface: str, values: Dict[str, Any]
    ) -> None:
        """Set values in the pool given a specific entity and interface."""
        LOGGER.debug("Setting %s %s for entity %s.", interface, values, entity)
        self._pool.update({
            f"{{{{ {entity}.{interface}.{name} }}}}": value
            for name, value in values.items()
        })

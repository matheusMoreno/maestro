"""Module with the base Workflow abstraction."""

from __future__ import annotations
import logging
from typing import Any, Dict, List

from maestro.steps import Step, step_factory
from maestro.exceptions import FailedStepException
from maestro.workflow.execution_context import ExecutionContext
from maestro.workflow.variable_pool import VariablePool


LOGGER = logging.getLogger(__name__)


class Workflow:
    """Abstraction of the workflow, a DAG of steps."""

    def __init__(
        self,
        name: str,
        steps: List[Step] = None,
        inputs: Dict[str, Any] = None,
        outputs: Dict[str, Any] = None,
    ) -> None:
        """Initialize workflow attributes."""
        self.name = name
        self.steps = steps or []
        self.inputs = inputs or {}
        self.outputs = outputs or {}
        self.last_context = ExecutionContext()
        self.last_variable_pool = VariablePool()

    def execute(self) -> Dict[str, Any]:
        """Execute the workflow and return its outputs."""
        LOGGER.info("Executing workflow %s.", self.name)
        self._initialize_context_and_pool()

        while not self.last_context.finished:
            current_step = self.last_context.get_next_step()
            inputs = self.last_variable_pool.get_values(current_step.inputs)
            try:
                LOGGER.debug("Executing step %s.", current_step.name)
                outputs = current_step.execute(inputs)
                self.last_context.set_current_step_as_successful()
                self.last_variable_pool.set_outputs(current_step.name, outputs)
            except FailedStepException as exc:
                LOGGER.warning("%s failed: %s", current_step.name, str(exc))
                self.last_context.set_current_step_as_failed(str(exc))

        outputs = self.last_variable_pool.get_values(self.outputs)
        LOGGER.debug("Workflow execution outputs: %s", outputs)
        return outputs

    def _initialize_context_and_pool(self) -> None:
        """Initialize a new context and variable pool for the execution."""
        self.last_context = ExecutionContext()
        self.last_variable_pool = VariablePool()

        self.last_variable_pool.set_inputs(self.name, self.inputs)
        for step in self.steps:
            LOGGER.debug("Registering step %s.", step.name)
            self.last_variable_pool.set_inputs(step.name, step.inputs)
            self.last_context.register_step(step)

    @classmethod
    def from_dict(cls, spec: Dict[str, Any]) -> Workflow:
        """Build workflow from a dictionary specification."""
        workflow_spec = spec.copy()
        steps_spec = workflow_spec.pop("steps", [])
        steps = [step_factory.create(step_spec) for step_spec in steps_spec]
        return cls(**workflow_spec, steps=steps)

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
        self.last_execution = ExecutionContext()

    def execute(self) -> Dict[str, Any]:
        """Execute the workflow and return its outputs."""
        LOGGER.info("Executing workflow %s.", self.name)
        execution = ExecutionContext()
        variable_pool = VariablePool()

        # Initialize variable pool and execution context
        variable_pool.set_inputs(self.name, self.inputs)
        for step in self.steps:
            LOGGER.debug("Registering step %s.", step.name)
            variable_pool.set_inputs(step.name, step.inputs)
            execution.register_step(step)

        while not execution.finished:
            current_step = execution.get_next_step()
            execution_inputs = variable_pool.get_values(current_step.inputs)
            try:
                LOGGER.debug("Executing step %s.", current_step.name)
                outputs = current_step.execute(execution_inputs)
                execution.set_current_step_as_successful()
                variable_pool.set_outputs(current_step.name, outputs)
            except FailedStepException as exc:
                LOGGER.warning("%s failed: %s", current_step.name, str(exc))
                execution.set_current_step_as_failed(str(exc))

        self.last_execution = execution

        outputs = variable_pool.get_values(self.outputs)
        LOGGER.debug("Workflow execution outputs: %s", outputs)
        return outputs

    @classmethod
    def from_dict(cls, spec: Dict[str, Any]) -> Workflow:
        """Build workflow from a dictionary specification."""
        workflow_spec = spec.copy()
        steps_spec = workflow_spec.pop("steps", [])
        steps = [step_factory.create(step_spec) for step_spec in steps_spec]
        return cls(**workflow_spec, steps=steps)

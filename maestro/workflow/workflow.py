"""Module with the base Workflow abstraction."""

from __future__ import annotations
from typing import Any, Dict, List

from maestro.steps import Step, step_factory
from maestro.exceptions import FailedStepException
from maestro.workflow.execution_context import ExecutionContext
from maestro.workflow.variable_pool import VariablePool


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

    def execute(self) -> Dict[str, Any]:
        """Execute the workflow and return its outputs."""
        context = ExecutionContext()
        variable_pool = VariablePool()

        # Initialize variable pool and execution context
        variable_pool.set_inputs(self.name, self.inputs)
        for step in self.steps:
            variable_pool.set_inputs(step.name, step.inputs)
            context.register_step(step)

        while not context.finished:
            current_step = context.get_next_step()
            execution_inputs = variable_pool.get_values(current_step.inputs)
            try:
                outputs = current_step.execute(execution_inputs)
                context.set_current_step_as_successful(outputs)
                variable_pool.set_outputs(current_step.name, outputs)
            except FailedStepException as exc:
                context.set_current_step_as_failed(str(exc))

        return variable_pool.get_values(self.outputs)

    @classmethod
    def from_dict(cls, spec: Dict[str, Any]) -> Workflow:
        """Build workflow from a dictionary specification."""
        workflow_spec = spec.copy()
        steps_spec = workflow_spec.pop("steps", [])
        steps = [step_factory.create(step_spec) for step_spec in steps_spec]
        return cls(**workflow_spec, steps=steps)

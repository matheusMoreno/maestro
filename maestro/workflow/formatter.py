"""Module with the execution log formatter."""

from typing import Any, Dict

from maestro.workflow.execution_context import ExecutionContext


class ExecutionLogFormatter:
    """Class to format results about an workflow execution."""

    def __init__(
        self,
        workflow_name: str,
        workflow_inputs: Dict[str, Any],
        execution_context: ExecutionContext,
        execution_outputs: Dict[str, Any]
    ) -> None:
        """Initialize attributes for the formatter."""
        self._wf_name = workflow_name
        self._wf_inputs = workflow_inputs
        self._context = execution_context
        self._outputs = execution_outputs

    def format(self) -> str:
        """Format output for a given execution."""
        return "\n\n".join([
            self._format_title(),
            self._format_inputs(),
            self._format_steps(),
            self._format_outputs(),
        ])

    def _format_title(self) -> str:
        """Format title of results log."""
        title = f'     Workflow "{self._wf_name}"     '
        ornament = "=" * len(title)
        return "\n".join([ornament, title, ornament])

    def _format_inputs(self) -> str:
        """Format inputs section of the result log."""
        header = "Inputs:"
        elements = [f"    - {k}: {v}" for k, v in self._wf_inputs.items()]
        return "\n".join([header, *elements])

    def _format_steps(self) -> str:
        """Format steps section of the result log."""
        header = "Steps:"
        step_list = self._context.successful_steps + self._context.failed_steps
        elements = [
            f"    - {s.step.name}: SUCCESSFUL" if not s.failed_reason else
            f"    - {s.step.name}: FAILED\n      |_ Reason: {s.failed_reason}"
            for s in step_list
        ]
        return "\n".join([header, *elements])

    def _format_outputs(self) -> str:
        """Format outputs section of the result log."""
        header = "Outputs:"
        elements = [f"    - {k}: {v}" for k, v in self._outputs.items()]
        return "\n".join([header, *elements])

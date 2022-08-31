"""Module with the execution log formatter."""

from typing import Any, Dict, List

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
            self._format_header(),
            self._format_inputs(),
            self._format_steps(),
            self._format_outputs(),
        ])

    def _format_header(self) -> str:
        """Format title of results log."""
        title = f'     Workflow "{self._wf_name}"     '
        ornament = "=" * len(title)
        return "\n".join([ornament, title, ornament])

    def _format_inputs(self) -> str:
        """Format inputs section of the result log."""
        elements = [f"{k}: {v}" for k, v in self._wf_inputs.items()]
        return self._format_as_list("Inputs", elements)

    def _format_steps(self) -> str:
        """Format steps section of the result log."""
        step_list = self._context.successful_steps + self._context.failed_steps
        elements = [
            f"{s.step.name}: SUCCESSFUL" if not s.failed_reason else
            f"{s.step.name}: FAILED\n      |_ Reason: {s.failed_reason}"
            for s in step_list
        ]
        return self._format_as_list("Steps", elements)

    def _format_outputs(self) -> str:
        """Format outputs section of the result log."""
        elements = [f"{k}: {v}" for k, v in self._outputs.items()]
        return self._format_as_list("Outputs", elements)

    @staticmethod
    def _format_as_list(title: str, elements: List[str]) -> str:
        """Format section as a list with a title."""
        elements = [f"    - {e}" for e in elements]
        return "\n".join([f"{title}:", *elements])

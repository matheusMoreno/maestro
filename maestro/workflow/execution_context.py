"""Module with the execution context abstraction."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set

from maestro.steps import Step


@dataclass
class StepContext:
    """Data class for a step running in an workflow."""

    step: Step
    depends_on: List[str]
    failed_reason: Optional[str] = None

    def __hash__(self) -> int:
        """Return the step name as a hash."""
        return hash(self.step.name)

    def __eq__(self, __o: object) -> bool:
        """Compare two steps."""
        return self.step.name == getattr(__o, "step").name


class ExecutionContext:
    """Context manager for an workflow execution."""

    def __init__(self) -> None:
        """Initialize execution context attributes."""
        self._ready_steps: Set[StepContext] = set()
        self._blocked_steps: Set[StepContext] = set()
        self._successful_steps: Set[StepContext] = set()
        self._failed_steps: Set[StepContext] = set()
        self._current_step: StepContext

    @property
    def finished(self) -> bool:
        """Check if the workflow has finished its execution."""
        return not bool(self._ready_steps)

    def register_step(self, step: Step) -> None:
        """Register a new step in the execution context."""
        step_ctx = StepContext(step=step, depends_on=step.depends_on)
        queue = self._blocked_steps if step.depends_on else self._ready_steps
        queue.add(step_ctx)

    def get_next_step(self) -> Step:
        """Get next step ready for execution."""
        self._current_step = self._ready_steps.pop()
        return self._current_step.step

    def set_current_step_as_successful(self, outputs: Dict[str, Any]) -> None:
        """Set current running step as successful."""
        self._update_current_step(outputs, successful=True)
        self._update_steps_dependent_on_successful_current_step()

    def set_current_step_as_failed(self, reason: str) -> None:
        """Set current running step as failed."""
        self._update_current_step(reason, successful=False)
        self._update_steps_dependent_on_failed_current_step()

    def _update_current_step(self, attribute: Any, successful: bool) -> None:
        """Update the running step as successful or failed."""
        attribute_to_set = "outputs" if successful else "failed_reason"
        queue = self._successful_steps if successful else self._failed_steps
        setattr(self._current_step, attribute_to_set, attribute)
        queue.add(self._current_step)

    def _get_dependent_steps(self, step_ctx: StepContext) -> Set[StepContext]:
        """Get set of dependent steps of a given step."""
        return set(
            blocked_step_ctx for blocked_step_ctx in self._blocked_steps
            if step_ctx.step.name in blocked_step_ctx.depends_on
        )

    def _update_steps_dependent_on_failed_current_step(self) -> None:
        """Set steps that depend on failed step as failed."""
        reason = f"Depended on failed step {self._current_step.step.name}"
        for step_ctx in self._get_dependent_steps(self._current_step):
            step_ctx.failed_reason = reason
            self._blocked_steps.remove(step_ctx)
            self._failed_steps.add(step_ctx)

    def _update_steps_dependent_on_successful_current_step(self) -> None:
        """Update dependencies and queue newly indepedent steps."""
        for step_ctx in self._get_dependent_steps(self._current_step):
            step_ctx.depends_on.remove(self._current_step.step.name)
            if not step_ctx.depends_on:
                self._blocked_steps.remove(step_ctx)
                self._ready_steps.add(step_ctx)

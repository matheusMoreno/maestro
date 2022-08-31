"""Module with the execution context abstraction."""

from dataclasses import dataclass
import logging
from typing import List, Optional

from maestro.steps import Step


LOGGER = logging.getLogger(__name__)


@dataclass
class StepContext:
    """Data class for a step in a running workflow."""

    step: Step
    depends_on: List[str]
    failed_reason: Optional[str] = None


class ExecutionContext:
    """Context manager for an workflow execution."""

    def __init__(self) -> None:
        """Initialize execution context attributes."""
        self.ready_steps: List[StepContext] = []
        self.blocked_steps: List[StepContext] = []
        self.successful_steps: List[StepContext] = []
        self.failed_steps: List[StepContext] = []
        self.current_step: StepContext

    @property
    def finished(self) -> bool:
        """Check if the workflow has finished its execution."""
        return not bool(self.ready_steps)

    def register_step(self, step: Step) -> None:
        """Register a new step in the execution context."""
        LOGGER.debug("Registering step %s.", step.name)
        step_ctx = StepContext(step=step, depends_on=step.depends_on)
        queue = self.blocked_steps if step.depends_on else self.ready_steps
        queue.append(step_ctx)

    def get_next_step(self) -> Step:
        """Get next step ready for execution."""
        self.current_step = self.ready_steps.pop(0)
        return self.current_step.step

    def set_current_step_as_successful(self) -> None:
        """Set current running step as successful."""
        self._update_current_step(failed=False)
        self._update_steps_dependent_on_successful_current_step()

    def set_current_step_as_failed(self, reason: str) -> None:
        """Set current running step as failed."""
        self._update_current_step(failed=True, reason=reason)
        self._update_steps_dependent_on_failed_current_step()

    def _update_current_step(self, failed: bool, reason: str = None) -> None:
        """Update the running step as successful or failed."""
        queue = self.successful_steps if not failed else self.failed_steps
        self.current_step.failed_reason = reason
        queue.append(self.current_step)

    def _get_dependent_steps(self, step_ctx: StepContext) -> List[StepContext]:
        """Get set of dependent steps of a given step."""
        return [
            blocked_step_ctx for blocked_step_ctx in self.blocked_steps
            if step_ctx.step.name in blocked_step_ctx.depends_on
        ]

    def _update_steps_dependent_on_failed_current_step(self) -> None:
        """Set steps that depend on failed step as failed."""
        reason = f"Depended on failed step {self.current_step.step.name}"
        for step_ctx in self._get_dependent_steps(self.current_step):
            LOGGER.debug("%s failed: %s", step_ctx.step.name, reason)
            step_ctx.failed_reason = reason
            self.blocked_steps.remove(step_ctx)
            self.failed_steps.append(step_ctx)

    def _update_steps_dependent_on_successful_current_step(self) -> None:
        """Update dependencies and queue newly indepedent steps."""
        for step_ctx in self._get_dependent_steps(self.current_step):
            step_ctx.depends_on.remove(self.current_step.step.name)
            if not step_ctx.depends_on:
                LOGGER.debug("Step %s ready.", step_ctx.step.name)
                self.blocked_steps.remove(step_ctx)
                self.ready_steps.append(step_ctx)

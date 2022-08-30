"""Module with Steps implementations."""

# pylama: ignore=W0611

from maestro.steps.factory import StepFactory
from maestro.steps.base import Step
from maestro.steps.python import PythonStep

# Create and register steps
step_factory = StepFactory()
step_factory.register("python_function", PythonStep)

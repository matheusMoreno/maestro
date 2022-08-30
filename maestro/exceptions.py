"""Exceptions raised by the Maestro library."""


class MaestroException(Exception):
    """Base exception for all other exceptions."""


class FailedStepException(MaestroException):
    """Exception for when a step failed."""

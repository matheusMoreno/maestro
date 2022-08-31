"""Module with simple mathematical operations."""


def add(*args) -> float:
    """Add a list of numbers."""
    return sum(args)


def square(value: float) -> float:
    """Square a value."""
    return value * value

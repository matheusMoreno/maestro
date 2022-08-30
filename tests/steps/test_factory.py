"""Unit tests for the step factory class."""

import unittest

from maestro.steps import StepFactory
from tests.steps.fake_step import FakeStep


class TestStepFactoryClass(unittest.TestCase):
    """Suite of unit tests for the StepFactory class."""

    def setUp(self) -> None:
        """Set up a StepFactory."""
        self.step_factory = StepFactory()

    def test_register(self) -> None:
        """Test if the factory correctly registers a class."""
        # Arrange
        type_name = "fake_step"

        # Act
        self.step_factory.register(type_name, FakeStep)

        # Assert
        self.assertEqual(FakeStep, self.step_factory.step_types.get(type_name))

    def test_create(self) -> None:
        """Test if the Step object is correctly created."""
        # Arrange
        type_name = "fake_step"
        self.step_factory.register(type_name, FakeStep)
        step_spec = {"name": "test_step", "path": "test_path"}
        step_expected = FakeStep(step_spec["name"], step_spec["path"])

        # Act
        step_created = self.step_factory.create(
            {"type": type_name, **step_spec}
        )

        # Assert
        self.assertEqual(type(step_expected), type(step_created))
        self.assertEqual(step_expected.name, step_created.name)
        self.assertEqual(step_expected.path, step_created.path)

    def test_raises_value_error_when_inexistent_type(self) -> None:
        """Test if the factory raises ValueError when a type doesn't exist."""
        # Act, assert
        with self.assertRaises(TypeError):
            self.step_factory.create({"type": "inexistent_type"})


if __name__ == '__main__':
    unittest.main()

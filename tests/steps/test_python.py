"""Unit tests for the Python Step class."""

import unittest

from maestro.steps import PythonStep
from maestro.exceptions import FailedStepException


class TestPythonStepClass(unittest.TestCase):
    """Suite of unit tests for the PythonStep class."""

    def setUp(self) -> None:
        """Set up a PythonStep."""
        self.step = PythonStep("floor_float", "math.floor")

    def test_execute(self) -> None:
        """Test if the class correctly executes the function."""
        # Arrange
        self.step.inputs = {"x": 3.14}
        self.step.outputs = ["value"]
        outputs_expected = {"value": 3}

        # Act
        outputs = self.step.execute()

        # Assert
        self.assertEqual(outputs_expected, outputs)

    def test_raises_failed_step_when_exception_occurs(self) -> None:
        """Test if FailedStepException is raised when Exception occurs."""
        # Arrange
        self.step.inputs = {"x": "not a number"}

        # Act, assert
        with self.assertRaises(FailedStepException):
            self.step.execute()


if __name__ == '__main__':
    unittest.main()

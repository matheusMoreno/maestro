"""Unit tests for the base step class."""

import unittest

from tests.steps.fake_step import FakeStep


class TestStepClass(unittest.TestCase):
    """Suite of unit tests for the Step class."""

    def setUp(self) -> None:
        """Set up a Step with required parameters."""
        self.step = FakeStep("test_step", "test_path")

    def test_execute(self) -> None:
        """Test if the execute method correctly calls _pack_outputs."""
        # Arrange
        inputs = {"outputs": (1, 2)}
        self.step.outputs = ["x", "y"]

        # Act
        outputs = self.step.execute(inputs)

        # Assert
        self.assertEqual(outputs, {"x": 1, "y": 2})

    def test_execute_with_single_output(self) -> None:
        """Test if a single output is packed by _pack_outputs."""
        # Arrange
        inputs = {"outputs": 1}
        self.step.outputs = ["x"]

        # Act
        outputs = self.step.execute(inputs)

        # Assert
        self.assertEqual(outputs, {"x": 1})


if __name__ == '__main__':
    unittest.main()

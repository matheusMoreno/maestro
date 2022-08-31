"""Unit tests for the variable pool class."""

# pylint: disable=protected-access

import unittest

from maestro.workflow.variable_pool import VariablePool


class TestVariablePoolClass(unittest.TestCase):
    """Suite of unit tests for the VariablePool class."""

    def setUp(self) -> None:
        """Set up a VariablePool instance."""
        self.variable_pool = VariablePool()

    def test_set_inputs(self) -> None:
        """Test if the set_inputs method works as expected."""
        # Arrange
        entity_name = "test"
        inputs = {"x": 1}
        expected_pool = {"{{ test.inputs.x }}": 1}

        # Act
        self.variable_pool.set_inputs(entity_name, inputs)

        # Assert
        self.assertEqual(expected_pool, self.variable_pool._pool)

    def test_set_outputs(self) -> None:
        """Test if the set_inputs method works as expected."""
        # Arrange
        entity_name = "test"
        outputs = {"y": 1}
        expected_pool = {"{{ test.outputs.y }}": 1}

        # Act
        self.variable_pool.set_outputs(entity_name, outputs)

        # Assert
        self.assertEqual(expected_pool, self.variable_pool._pool)

    def test_get_reference_value(self) -> None:
        """Test if a reference value is correctly resolved by the pool."""
        # Arrange
        self.variable_pool.set_outputs("test", {"y": 1})
        inputs_reference = {"x": "{{ test.outputs.y }}"}
        inputs_expected = {"x": 1}

        # Act
        inputs = self.variable_pool.get_values(inputs_reference)

        # Assert
        self.assertEqual(inputs_expected, inputs)

    def test_return_same_value_if_not_reference(self) -> None:
        """Test if the pool returns the original value if no match exists."""
        # Arrange
        inputs_expected = {"x": 1}

        # Act
        inputs = self.variable_pool.get_values(inputs_expected)

        # Assert
        self.assertEqual(inputs_expected, inputs)


if __name__ == '__main__':
    unittest.main()

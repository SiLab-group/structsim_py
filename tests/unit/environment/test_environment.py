import pytest
from structsim.experimenthandling.environment import Environment
from structsim.experimenthandling.parameter import Parameter


class TestEnvironment:

    delta = 1e-9

    def test_constructor_should_not_change_the_original_env_when_constructing_new_env(self):
        # Arrange
        p1 = Parameter("val1", 0)
        v = [p1]
        e1 = Environment(1, v, 0.3)
        e2 = Environment(2, e1)
        e2.get_set_of_parameters()[0].set_value(1)

        # Act
        expected_e1_value = e1.get_set_of_parameters()[0].get_value()
        expected_e2_value = e2.get_set_of_parameters()[0].get_value()

        # Assert
        assert expected_e1_value == pytest.approx(0, abs=self.delta)
        assert expected_e2_value == pytest.approx(1, abs=self.delta)

    def test_compare_to_should_return_correct_value_when_comparing_environments(self):
        # Arrange
        low  = Environment(1, [], 0.3)
        high = Environment(2, [], 0.5)
        low2 = Environment(2, [], 0.3)

        # Act
        should_be_negative = low.compare_to(high)
        should_be_positive = high.compare_to(low)
        should_be_zero     = low.compare_to(low2)

        # Assert
        assert should_be_negative < 0
        assert should_be_positive > 0
        assert should_be_zero == 0

    def test_to_string_modifier_should_return_correct_string_when_displaying_the_env_as_a_string(self):
        # Arrange
        e = Environment(1, [], 0.3)
        trace = ["m1", "m2"]
        e.set_trace(trace)

        # Act
        expected_string = "Simulation ID : 1\t Probability : 0.3\t Modifier implemented :    m1   m2"
        actual_string = e.to_string_modifier()

        # Assert
        assert expected_string == actual_string

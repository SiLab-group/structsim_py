import pytest
from structsim.experimenthandling.environment import Environment
from structsim.experimenthandling.parameter import Parameter
from structsim.gluecode.concrete_modifier import ConcreteModifier


class TestConcreteModifier:

    delta = 1e-9

    @pytest.mark.parametrize("operator,value", [
        ('+', 1),
        ('-', 2),
        ('*', 3),
        ('/', 4),
    ])
    def test_apply_modifier_should_update_the_environment_correctly(self, operator, value):
        # Arrange
        e = Environment()
        v = [Parameter("val1", 1)]
        e.set_set_of_parameters(v)

        modifier = ConcreteModifier("val1", operator, value)

        # Act
        e = modifier.apply_modifier(e)

        # Assert
        if operator == '+':
            assert e.get_set_of_parameters()[0].get_value() == pytest.approx(2, abs=self.delta)
        elif operator == '-':
            assert e.get_set_of_parameters()[0].get_value() == pytest.approx(-1, abs=self.delta)
        elif operator == '*':
            assert e.get_set_of_parameters()[0].get_value() == pytest.approx(3, abs=self.delta)
        elif operator == '/':
            assert e.get_set_of_parameters()[0].get_value() == pytest.approx(0.25, abs=self.delta)

    def test_findvalue_should_find_the_value_in_a_vector(self):
        # Arrange
        params = [
            Parameter("val1", 3),
            Parameter("val2", 10),
            Parameter("val3", 7),
        ]

        # Act
        result = ConcreteModifier.find_value(params, "val2")

        # Assert
        assert result == pytest.approx(10, abs=self.delta)

    def test_findvalue_should_return_minus1_when_nothing_is_found(self):
        # Arrange
        params = [
            Parameter("val1", 3),
            Parameter("val2", 10),
            Parameter("val3", 7),
        ]

        # Act
        result = ConcreteModifier.find_value(params, "val31416")

        # Assert
        assert result == pytest.approx(-1, abs=self.delta)

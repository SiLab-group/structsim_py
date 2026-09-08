import logging
from typing import List

from structsim.experimenthandling.environment import Environment
from structsim.experimenthandling.parameter import Parameter
from structsim.interfaces.a_modifier import AModifier

logger = logging.getLogger(__name__)


class ConcreteModifier(AModifier):
    """Concrete modifier that applies arithmetic operations (+, -, *, /) to a named parameter."""

    def __init__(
        self,
        key_to_change="val1",
        operator: str = "*",
        delta: float = 1.0,
        probability: float = 1.0,
    ) -> None:
        # Mirror the Java single-float constructor ConcreteModifier(double delta)
        if isinstance(key_to_change, (int, float)):
            delta = float(key_to_change)
            key_to_change = "val1"
            operator = "*"
            probability = delta
        super().__init__(probability, operator + str(delta))
        self.key_to_change = key_to_change
        self.operator = operator
        self.delta = delta

    @classmethod
    def from_delta(cls, delta: float) -> "ConcreteModifier":
        """Convenience constructor mirroring ConcreteModifier(double delta)."""
        return cls("val1", "*", delta, delta)

    def apply_modifier(self, env: Environment) -> Environment:
        params: List[Parameter] = env.get_set_of_parameters()
        for p in params:
            logger.debug(f"param={p.get_key()} key_to_change={self.key_to_change}")
            if p.get_key() == self.key_to_change:
                if self.operator == "+":
                    p.set_value(p.get_value() + self.delta)
                elif self.operator == "-":
                    p.set_value(p.get_value() - self.delta)
                elif self.operator == "*":
                    p.set_value(p.get_value() * self.delta)
                elif self.operator == "/":
                    p.set_value(p.get_value() / self.delta)
        return env

    @staticmethod
    def find_value(params: List[Parameter], key: str) -> float:
        """Return the value of the parameter with the given key, or -1 if not found."""
        for p in params:
            if p.get_key() == key:
                return p.get_value()
        return -1.0

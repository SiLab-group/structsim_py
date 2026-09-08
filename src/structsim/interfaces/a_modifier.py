from abc import ABC, abstractmethod

from structsim.experimenthandling.environment import Environment


class AModifier(ABC):
    """Abstract base class for parameter modifiers."""

    def __init__(self, probability: float = 0.0, name: str = "AModifier") -> None:
        self._probability = probability
        self._name = name

    @abstractmethod
    def apply_modifier(self, env: Environment) -> Environment:
        """Apply the modifier algorithm to an environment and return the modified environment."""

    def get_probability(self) -> float:
        return self._probability

    def set_probability(self, probability: float) -> None:
        self._probability = probability

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    @property
    def probability(self) -> float:
        return self._probability

    @probability.setter
    def probability(self, value: float) -> None:
        self._probability = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

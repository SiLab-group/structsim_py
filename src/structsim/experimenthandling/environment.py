from typing import List
from structsim.experimenthandling.parameter import Parameter


class Environment:
    """Simulation state at instant T: holds an ID, parameters, probability, and trace."""

    def __init__(
        self,
        id: int = 1,
        set_of_parameters: List[Parameter] = None,
        probability: float = 1.0,
    ) -> None:
        if isinstance(set_of_parameters, Environment):
            source = set_of_parameters
            self.id = id
            self.set_of_parameters = [Parameter.from_parameter(p) for p in source.set_of_parameters]
            self.probability = source.probability
            self.path_save_result = ""
            self.trace = list(source.trace)
            return
        self.id = id
        self.set_of_parameters: List[Parameter] = (
            set_of_parameters if set_of_parameters is not None else []
        )
        self.probability = probability
        self.path_save_result: str = ""
        self.trace: List[str] = []

    @classmethod
    def from_environment(cls, id: int, e: "Environment") -> "Environment":
        """Copy constructor: creates a new environment by copying another."""
        new_env = cls(id, [], e.probability)
        new_env.set_of_parameters = [Parameter.from_parameter(p) for p in e.set_of_parameters]
        new_env.trace = list(e.trace)
        return new_env

    def get_id(self) -> int:
        return self.id

    def get_set_of_parameters(self) -> List[Parameter]:
        return self.set_of_parameters

    def set_set_of_parameters(self, set_of_parameters: List[Parameter]) -> None:
        self.set_of_parameters = set_of_parameters

    def get_probability(self) -> float:
        return self.probability

    def set_probability(self, probability: float) -> None:
        self.probability = probability

    def get_path_save_result(self) -> str:
        return self.path_save_result

    def set_path_save_result(self, path_save_result: str) -> None:
        self.path_save_result = path_save_result

    def get_trace(self) -> List[str]:
        return self.trace

    def set_trace(self, trace: List[str]) -> None:
        self.trace = trace

    def to_string_modifier(self) -> str:
        result = ""
        for s in self.trace:
            result += "   " + s
        return (
            f"Simulation ID : {self.id}\t Probability : {self.probability}"
            f"\t Modifier implemented : {result}"
        )

    def compare_to(self, other: "Environment") -> int:
        if self.probability < other.probability:
            return -1
        elif self.probability > other.probability:
            return 1
        return 0

    def __lt__(self, other: "Environment") -> bool:
        return self.probability < other.probability

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Environment):
            return False
        return self.probability == other.probability

    def __le__(self, other: "Environment") -> bool:
        return self.probability <= other.probability

    def __gt__(self, other: "Environment") -> bool:
        return self.probability > other.probability

    def __ge__(self, other: "Environment") -> bool:
        return self.probability >= other.probability

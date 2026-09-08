from abc import ABC, abstractmethod
from typing import IO, List

from structsim.experimenthandling.parameter import Parameter


class IManageParametersFile(ABC):
    """Interface defining methods to manage parameter files."""

    @abstractmethod
    def read_parameters_file(self, parameters_file_path: str) -> List[Parameter]:
        """Read a parameters file and return the list of parameters."""

    @abstractmethod
    def read_parameters_file_from_stream(self, input_stream: IO[bytes]) -> List[Parameter]:
        """Read parameters from an IO stream."""

    @abstractmethod
    def write_parameters_file(self, set_of_parameters: List[Parameter], location_to_store: str) -> None:
        """Write a parameters file for the simulator."""

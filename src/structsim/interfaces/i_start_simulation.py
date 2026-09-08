from abc import ABC, abstractmethod


class IStartSimulation(ABC):
    """Interface defining the method to start a simulation."""

    @abstractmethod
    def start_simulation(self, path_to_input_file: str) -> None:
        """Start the simulation using the given input file path."""

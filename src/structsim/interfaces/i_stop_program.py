from abc import ABC, abstractmethod


class IStopProgram(ABC):
    """Interface defining the method to stop the program."""

    @abstractmethod
    def stop_program(self) -> None:
        """Stop the program."""

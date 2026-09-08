from abc import ABC, abstractmethod
from typing import List


class IManageModifier(ABC):
    """Interface defining the method to manage modifiers."""

    @abstractmethod
    def initiate_modifier_list(self) -> List:
        """Initiate the list of modifier instances."""

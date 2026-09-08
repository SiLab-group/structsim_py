from abc import ABC, abstractmethod
from typing import List

from structsim.experimenthandling.measure import Measure


class IExtractMeasures(ABC):
    """Interface defining the method to extract measures from result files."""

    @abstractmethod
    def extract_measures(self, results_file_path: str) -> List[Measure]:
        """Extract measures from a results file path."""

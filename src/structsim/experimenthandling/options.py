from typing import Optional
from datetime import timedelta


class Options:
    """Configuration settings for running the simulation."""

    def __init__(self) -> None:
        self.path_parameters: Optional[str] = None
        self.folder_path_out: Optional[str] = None
        self.path_simulator: Optional[str] = None
        self.cuttof_planning: int = 0
        self.cuttof_planning_delta: Optional[timedelta] = None
        self.type_of_cuttof_planning: Optional[str] = None
        self.stop_criteria: float = 0.0
        self.path_to_simulator_result_file: Optional[str] = None

    def get_path_parameters(self) -> Optional[str]:
        return self.path_parameters

    def set_path_parameters(self, path_parameters: str) -> None:
        self.path_parameters = path_parameters

    def get_folder_path_out(self) -> Optional[str]:
        return self.folder_path_out

    def set_folder_path_out(self, folder_path_out: str) -> None:
        self.folder_path_out = folder_path_out

    def get_path_simulator(self) -> Optional[str]:
        return self.path_simulator

    def set_path_simulator(self, path_simulator: str) -> None:
        self.path_simulator = path_simulator

    def get_cuttof_planning(self) -> int:
        return self.cuttof_planning

    def set_cuttof_planning(self, cuttof_planning: int) -> None:
        self.cuttof_planning = cuttof_planning

    def get_cuttof_planning_h(self) -> Optional[timedelta]:
        return self.cuttof_planning_delta

    def set_cuttof_planning_h(self, cuttof_planning_delta: timedelta) -> None:
        self.cuttof_planning_delta = cuttof_planning_delta

    def get_type_of_cuttof_planning(self) -> Optional[str]:
        return self.type_of_cuttof_planning

    def set_type_of_cuttof_planning(self, type_of_cuttof_planning: str) -> None:
        self.type_of_cuttof_planning = type_of_cuttof_planning

    def get_stop_criteria(self) -> float:
        return self.stop_criteria

    def set_stop_criteria(self, stop_criteria: float) -> None:
        self.stop_criteria = stop_criteria

    def get_path_to_simulator_result_file(self) -> Optional[str]:
        return self.path_to_simulator_result_file

    def set_path_to_simulator_result_file(self, path_to_simulator_result_file: str) -> None:
        self.path_to_simulator_result_file = path_to_simulator_result_file

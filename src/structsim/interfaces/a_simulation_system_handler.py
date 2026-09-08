from typing import List, Optional

from structsim.interfaces.i_start_simulation import IStartSimulation
from structsim.interfaces.i_stop_program import IStopProgram
from structsim.interfaces.i_manage_parameters_file import IManageParametersFile
from structsim.interfaces.i_extract_measures import IExtractMeasures
from structsim.interfaces.i_manage_modifier import IManageModifier
from structsim.interfaces.a_modifier import AModifier
from structsim.experimenthandling.options import Options


class ASimulationSystemHandler(
    IStartSimulation,
    IStopProgram,
    IManageParametersFile,
    IExtractMeasures,
    IManageModifier,
):
    """Abstract class combining all handler interfaces for the glue code layer.

    Replaces Java's 'implements I1, I2, I3, I4, I5' with Python multiple
    inheritance from ABC classes. Any concrete subclass must implement:
    start_simulation, stop_program, read_parameters_file,
    read_parameters_file_from_stream, write_parameters_file,
    extract_measures, and initiate_modifier_list.
    """

    def __init__(self) -> None:
        self._options: Optional[Options] = None
        self._list_modifier_class: List[AModifier] = []

    @property
    def options(self) -> Optional[Options]:
        """The simulation options."""
        return self._options

    @options.setter
    def options(self, options: Options) -> None:
        self._options = options

    @property
    def list_modifier_class(self) -> List[AModifier]:
        """The list of modifier instances."""
        return self._list_modifier_class

    @list_modifier_class.setter
    def list_modifier_class(self, list_modifier_class: List[AModifier]) -> None:
        self._list_modifier_class = list_modifier_class

    def get_options(self) -> Optional[Options]:
        return self._options

    def set_options(self, options: Options) -> None:
        self._options = options

    def get_list_modifier_class(self) -> List[AModifier]:
        return self._list_modifier_class

    def set_list_modifier_class(self, list_modifier_class: List[AModifier]) -> None:
        self._list_modifier_class = list_modifier_class

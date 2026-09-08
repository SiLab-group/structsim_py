import os
from typing import IO, List

from structsim.experimenthandling.measure import Measure
from structsim.experimenthandling.parameter import Parameter
from structsim.interfaces.a_modifier import AModifier
from structsim.interfaces.a_simulation_system_handler import ASimulationSystemHandler


class SimpleSimulationHandler(ASimulationSystemHandler):
    """Concrete handler providing file-based I/O for parameters and measures."""

    def __init__(self, modifiers: List[AModifier] = None) -> None:
        super().__init__()
        self._modifiers: List[AModifier] = modifiers if modifiers is not None else []

    def extract_measures(self, results_file_path: str) -> List[Measure]:
        separator = "="
        measures_list: List[Measure] = []
        try:
            with open(results_file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.rstrip("\n")
                    pos = line.index(separator)
                    measure_key = line[:pos]
                    measure_value = line[pos + 1:]
                    measures_list.append(Measure(measure_key, measure_value))
        except OSError as e:
            import traceback
            traceback.print_exc()
        return measures_list

    def initiate_modifier_list(self) -> List[AModifier]:
        self._list_modifier_class = self._modifiers
        return self._list_modifier_class

    def read_parameters_file(self, parameters_file_path: str) -> List[Parameter]:
        if hasattr(parameters_file_path, "read"):
            return self.read_parameters_file_from_stream(parameters_file_path)
        separator = "="
        parameters_list: List[Parameter] = []
        try:
            with open(parameters_file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.rstrip("\n")
                    pos = line.index(separator)
                    key = line[:pos]
                    value = float(line[pos + 1:])
                    parameters_list.append(Parameter(key, value))
        except OSError:
            import traceback
            traceback.print_exc()
        return parameters_list

    def read_parameters_file_from_stream(self, input_stream: IO[bytes]) -> List[Parameter]:
        separator = "="
        parameters_list: List[Parameter] = []
        try:
            content = input_stream.read()
            if isinstance(content, bytes):
                content = content.decode("utf-8")
            for line in content.splitlines():
                if not line.strip():
                    continue
                pos = line.index(separator)
                key = line[:pos]
                value = float(line[pos + 1:])
                parameters_list.append(Parameter(key, value))
            input_stream.close()
        except OSError:
            import traceback
            traceback.print_exc()
        return parameters_list

    def write_parameters_file(self, set_of_parameters: List[Parameter], location_to_store: str) -> None:
        try:
            with open(os.path.join(location_to_store, "myParamFile.txt"), "w", encoding="utf-8") as f:
                for p in set_of_parameters:
                    f.write(f"{p.get_key()}={float(p.get_value())}\n")
        except Exception:
            import traceback
            traceback.print_exc()

    def start_simulation(self, path_to_input_file: str) -> None:
        result_file = self._options.get_path_to_simulator_result_file()
        os.makedirs(os.path.dirname(result_file), exist_ok=True)
        try:
            open(result_file, "a").close()
        except OSError:
            import traceback
            traceback.print_exc()

    def stop_program(self) -> None:
        pass

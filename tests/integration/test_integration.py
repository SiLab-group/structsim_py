import io
import os
import shutil
import tempfile
import time
from pathlib import Path

import pytest

from structsim.gluecode.concrete_modifier import ConcreteModifier
from structsim.gluecode.simple_simulation_handler import SimpleSimulationHandler
from structsim.gluecode.simulation import Simulation
from structsim.interfaces.a_modifier import AModifier


_PATH_PARAMETERS = os.path.join(
    os.environ["STRUCTSIM_PROJECT_DIR"], "resources", "parameters.txt"
).replace("\\", "/")


class TestIntegration:

    pathOUT = tempfile.gettempdir().replace("\\", "/") + "/structsim-results"
    pathSIM = tempfile.gettempdir().replace("\\", "/") + "/structsim-simulator"

    def _return_modifiers_from_scenario(self, scenario):
        modifiers = []
        if scenario == 1:
            modifiers.append(ConcreteModifier(0.5))
        elif scenario == 2:
            modifiers.append(ConcreteModifier(0.2))
            modifiers.append(ConcreteModifier(0.5))
        elif scenario == 4:
            modifiers.append(ConcreteModifier(0.1))
            modifiers.append(ConcreteModifier(0.8))
            modifiers.append(ConcreteModifier(0.5))
            modifiers.append(ConcreteModifier(0.2))
        return modifiers

    def _return_expected_lines_from_scenario(self, scenario):
        if scenario == 1:
            return [
                "Simulation ID : 1\t Probability : 0.5\t Modifier implemented :    *0.5",
                "Simulation ID : 2\t Probability : 0.25\t Modifier implemented :    *0.5   *0.5",
                "Simulation ID : 3\t Probability : 0.125\t Modifier implemented :    *0.5   *0.5   *0.5",
                "Simulation ID : 4\t Probability : 0.0625\t Modifier implemented :    *0.5   *0.5   *0.5   *0.5",
            ]
        elif scenario == 2:
            return [
                "Simulation ID : 1\t Probability : 0.2\t Modifier implemented :    *0.2",
                "Simulation ID : 2\t Probability : 0.5\t Modifier implemented :    *0.5",
                "Simulation ID : 3\t Probability : 0.1\t Modifier implemented :    *0.5   *0.2",
                "Simulation ID : 4\t Probability : 0.25\t Modifier implemented :    *0.5   *0.5",
                "Simulation ID : 5\t Probability : 0.05\t Modifier implemented :    *0.5   *0.5   *0.2",
                "Simulation ID : 6\t Probability : 0.125\t Modifier implemented :    *0.5   *0.5   *0.5",
                "Simulation ID : 7\t Probability : 0.04000000000000001\t Modifier implemented :    *0.2   *0.2",
                "Simulation ID : 8\t Probability : 0.1\t Modifier implemented :    *0.2   *0.5",
                "Simulation ID : 9\t Probability : 0.025\t Modifier implemented :    *0.5   *0.5   *0.5   *0.2",
                "Simulation ID : 10\t Probability : 0.0625\t Modifier implemented :    *0.5   *0.5   *0.5   *0.5",
                "Simulation ID : 11\t Probability : 0.020000000000000004\t Modifier implemented :    *0.5   *0.2   *0.2",
                "Simulation ID : 12\t Probability : 0.05\t Modifier implemented :    *0.5   *0.2   *0.5",
                "Simulation ID : 13\t Probability : 0.020000000000000004\t Modifier implemented :    *0.2   *0.5   *0.2",
                "Simulation ID : 14\t Probability : 0.05\t Modifier implemented :    *0.2   *0.5   *0.5",
            ]
        elif scenario == 4:
            return [
                "Simulation ID : 1\t Probability : 0.1\t Modifier implemented :    *0.1",
                "Simulation ID : 2\t Probability : 0.8\t Modifier implemented :    *0.8",
                "Simulation ID : 3\t Probability : 0.5\t Modifier implemented :    *0.5",
                "Simulation ID : 4\t Probability : 0.2\t Modifier implemented :    *0.2",

                "Simulation ID : 5\t Probability : 0.08000000000000002\t Modifier implemented :    *0.8   *0.1",
                "Simulation ID : 6\t Probability : 0.6400000000000001\t Modifier implemented :    *0.8   *0.8",
                "Simulation ID : 7\t Probability : 0.4\t Modifier implemented :    *0.8   *0.5",
                "Simulation ID : 8\t Probability : 0.16000000000000003\t Modifier implemented :    *0.8   *0.2",

                "Simulation ID : 9\t Probability : 0.06400000000000002\t Modifier implemented :    *0.8   *0.8   *0.1",
                "Simulation ID : 10\t Probability : 0.5120000000000001\t Modifier implemented :    *0.8   *0.8   *0.8",
                "Simulation ID : 11\t Probability : 0.32000000000000006\t Modifier implemented :    *0.8   *0.8   *0.5",
                "Simulation ID : 12\t Probability : 0.12800000000000003\t Modifier implemented :    *0.8   *0.8   *0.2",

                "Simulation ID : 13\t Probability : 0.051200000000000016\t Modifier implemented :    *0.8   *0.8   *0.8   *0.1",
                "Simulation ID : 14\t Probability : 0.40960000000000013\t Modifier implemented :    *0.8   *0.8   *0.8   *0.8",
                "Simulation ID : 15\t Probability : 0.25600000000000006\t Modifier implemented :    *0.8   *0.8   *0.8   *0.5",
                "Simulation ID : 16\t Probability : 0.10240000000000003\t Modifier implemented :    *0.8   *0.8   *0.8   *0.2",

                "Simulation ID : 17\t Probability : 0.05\t Modifier implemented :    *0.5   *0.1",
                "Simulation ID : 18\t Probability : 0.4\t Modifier implemented :    *0.5   *0.8",
                "Simulation ID : 19\t Probability : 0.25\t Modifier implemented :    *0.5   *0.5",
                "Simulation ID : 20\t Probability : 0.1\t Modifier implemented :    *0.5   *0.2",
            ]
        return None

    def _clean_output_directory(self):
        results_path = Path(self.pathOUT)
        if results_path.exists():
            shutil.rmtree(str(results_path), ignore_errors=True)

    def _run_and_assert_summary_file(
            self,
            cuttof_planning,
            type_cuttof_planning,
            modifiers,
            expected_lines,
    ):
        # Arrange
        self._clean_output_directory()
        Path(self.pathOUT).mkdir(parents=True, exist_ok=True)
        Path(self.pathSIM).mkdir(parents=True, exist_ok=True)

        temp_dir = tempfile.mkdtemp(prefix="structsim-test")
        temp_config = os.path.join(temp_dir, "config.properties")

        config_content = (
            f"pathOUT = {self.pathOUT}\n"
            f"pathParameters = {_PATH_PARAMETERS}\n"
            f"pathSimulator = {self.pathSIM}\n"
            f"pathToSimulatorResultFile = {self.pathSIM}/results/results.txt\n"
            f"cuttOfPlanning = {cuttof_planning}\n"
            f"typeCuttOfPlanning = {type_cuttof_planning}\n"
        )
        with open(temp_config, 'w') as f:
            f.write(config_content)

        with open(temp_config, 'rb') as path_config_file:
            ssh = SimpleSimulationHandler(modifiers)

            # Act
            s = Simulation()
            s.start_program(path_config_file, ssh)

        # Poll
        summary_file = Path(self.pathOUT) / "SummaryFile.txt"
        timeout = 15.0
        start = time.time()
        lines = []

        while time.time() - start < timeout:
            if summary_file.exists():
                lines = []
                found_blank_line = False
                try:
                    with open(str(summary_file), 'r') as br:
                        for line in br:
                            if line.strip() == '':
                                found_blank_line = True
                                break
                            lines.append(line.rstrip('\n'))
                except OSError:
                    pass
                if found_blank_line:
                    break
            time.sleep(0.2)

        # Assert
        assert summary_file.exists(), "SummaryFile.txt should exist"
        assert len(expected_lines) == len(lines)
        for i, expected in enumerate(expected_lines):
            assert expected == lines[i], f"Incorrect content at line {i + 1}"

    @pytest.mark.parametrize("scenario_number,cuttof_planning", [
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 1),
        (2, 2),
        (2, 3),
        (2, 4),
        (2, 5),
        (2, 6),
        (2, 7),
        (4, 1),
        (4, 2),
        (4, 3),
        (4, 4),
        (4, 5),
    ])
    def test_int_cutoff_type(self, scenario_number, cuttof_planning):
        type_cuttof_planning = "INT"
        modifiers = self._return_modifiers_from_scenario(scenario_number)
        expected_lines = self._return_expected_lines_from_scenario(scenario_number)

        number_of_lines_to_keep = cuttof_planning * scenario_number
        exact_expected_lines = expected_lines[:number_of_lines_to_keep]

        self._run_and_assert_summary_file(
            str(cuttof_planning),
            type_cuttof_planning,
            modifiers,
            exact_expected_lines,
        )

    @pytest.mark.parametrize("scenario_number,cuttof_planning,expected_number_of_lines", [
        (1, 0.1,  4),
        (1, 0.2,  3),
        (1, 0.3,  2),
        (1, 0.4,  2),
        (1, 0.5,  1),
        (1, 0.6,  1),
        (1, 0.7,  1),
        (1, 0.8,  1),
        (1, 0.9,  1),
        (2, 0.1, 10),
        (2, 0.2,  6),
        (2, 0.3,  4),
        (2, 0.4,  4),
        (2, 0.5,  2),
        (2, 0.6,  2),
        (2, 0.7,  2),
        (2, 0.8,  2),
        (2, 0.9,  2),
        (4, 0.45, 20),
        (4, 0.5,  16),
        (4, 0.6,  12),
        (4, 0.7,   8),
        (4, 0.8,   4),
        (4, 0.9,   4),
    ])
    def test_criteria_cutoff_type(self, scenario_number, cuttof_planning, expected_number_of_lines):
        type_cuttof_planning = "CRITERIA"
        modifiers = self._return_modifiers_from_scenario(scenario_number)
        expected_lines = self._return_expected_lines_from_scenario(scenario_number)
        exact_expected_lines = expected_lines[:expected_number_of_lines]

        self._run_and_assert_summary_file(
            str(cuttof_planning),
            type_cuttof_planning,
            modifiers,
            exact_expected_lines,
        )

    @pytest.mark.parametrize("scenario_number,cuttof_planning,expected_number_of_lines", [
        (1, 1, 1),
        (2, 1, 2),
        (4, 1, 4),
    ])
    def test_criteria_cutoff_type_value_one(self, scenario_number, cuttof_planning, expected_number_of_lines):
        type_cuttof_planning = "CRITERIA"
        modifiers = self._return_modifiers_from_scenario(scenario_number)
        expected_lines = self._return_expected_lines_from_scenario(scenario_number)
        exact_expected_lines = expected_lines[:expected_number_of_lines]

        self._run_and_assert_summary_file(
            str(cuttof_planning),
            type_cuttof_planning,
            modifiers,
            exact_expected_lines,
        )

    def test_criteria_cutoff_type_value_zero(self):
        type_cuttof_planning = "CRITERIA"
        scenario_number = 1
        cuttof_planning = 0
        modifiers = self._return_modifiers_from_scenario(scenario_number)

        summary_file_path = Path(self.pathOUT) / "SummaryFile.txt"
        if summary_file_path.exists():
            summary_file_path.unlink()

        temp_dir = tempfile.mkdtemp(prefix="structsim-test")
        temp_config = os.path.join(temp_dir, "config.properties")

        config_content = (
            f"pathOUT = {self.pathOUT}\n"
            f"pathParameters = {_PATH_PARAMETERS}\n"
            f"pathSimulator = {self.pathSIM}\n"
            f"pathToSimulatorResultFile = {self.pathSIM}/results/results.txt\n"
            f"cuttOfPlanning = {cuttof_planning}\n"
            f"typeCuttOfPlanning = {type_cuttof_planning}\n"
        )
        with open(temp_config, 'w') as f:
            f.write(config_content)

        with open(temp_config, 'rb') as path_config_file:
            ssh = SimpleSimulationHandler(modifiers)

            # Act
            s = Simulation()
            s.start_program(path_config_file, ssh)

        summary_file = Path(self.pathOUT) / "SummaryFile.txt"

        # Assert
        assert not summary_file.exists(), "SummaryFile.txt should not exist"

from pathlib import Path
from unittest.mock import MagicMock, ANY
from structsim.experimenthandling.environment import Environment
from structsim.experimenthandling.options import Options
from .file_management_tests import FileManagementTests


def _parse_properties(text):
    props = {}
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith('#') and '=' in stripped:
            k, v = stripped.split('=', 1)
            props[k.strip()] = v.strip()
    return props


class TestFileManagementSimulation(FileManagementTests):

    def test_save_simultation_result_should_save_result_and_return_path_when_directory_exists(self):
        # Arrange
        options = Options()
        options.set_folder_path_out(str(self.tempDir))
        self.fileManagement.set_options(options)

        env = Environment()

        simulation_folder = self.tempDir / "_sim1"
        simulation_folder.mkdir(parents=True, exist_ok=True)

        expected_result = "SUCCESS"

        # Act
        returned_path = self.fileManagement.save_simultation_result(expected_result, env)

        # Assert
        expected_path = str(simulation_folder / "results.txt")

        assert Path(expected_path).resolve() == Path(returned_path).resolve()
        assert Path(returned_path).exists()

        props = _parse_properties(Path(returned_path).read_text())
        assert props.get("Result") == expected_result

    def test_create_new_folder_should_create_result_and_simulator_folders(self):
        # Arrange
        options = Options()
        options.set_folder_path_out(str(self.tempDir / "results"))
        options.set_path_simulator(str(self.tempDir / "simulator"))

        self.fileManagement.set_options(options)

        (self.tempDir / "results").mkdir(parents=True, exist_ok=True)
        (self.tempDir / "simulator").mkdir(parents=True, exist_ok=True)

        env = Environment()

        # Act
        returned_path = self.fileManagement.create_new_folder(env)

        expected_result_folder    = self.tempDir / "results" / "_sim1"
        expected_simulator_folder = self.tempDir / "simulator" / "_sim1"

        # Assert
        assert expected_result_folder.resolve() == Path(returned_path).resolve()

        assert expected_result_folder.exists()
        assert expected_result_folder.is_dir()

        assert expected_simulator_folder.exists()
        assert expected_simulator_folder.is_dir()

    def test_create_new_folder_simulation_should_create_simulation_folder_and_write_parameters_file(self):
        # Arrange
        options = Options()
        options.set_folder_path_out(str(self.tempDir / "results"))
        options.set_path_simulator(str(self.tempDir / "simulator"))

        self.fileManagement.set_options(options)

        env = Environment()

        glue_code = MagicMock()

        (self.tempDir / "results").mkdir(parents=True, exist_ok=True)
        (self.tempDir / "simulator").mkdir(parents=True, exist_ok=True)

        # Act
        self.fileManagement.create_new_folder_simulation(env, glue_code)

        # Assert
        glue_code.write_parameters_file.assert_called_once_with(
            env.get_set_of_parameters(), ANY)

        assert env.get_path_save_result() is not None
        assert "_sim" in env.get_path_save_result()

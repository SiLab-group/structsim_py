import io
import pytest
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


class TestFileManagementProperties(FileManagementTests):

    def test_load_data_from_properties_file_should_load_properties_file(self):
        # Arrange
        properties_content = (
            "pathParameters=params.txt\n"
            "pathOUT=C:/output\n"
            "pathSimulator=simulator.exe\n"
            "pathToSimulatorResultFile=result.txt\n"
            "cuttOfPlanning=10\n"
            "typeCuttOfPlanning=INT\n"
        )
        input_stream = io.BytesIO(properties_content.encode('utf-8'))

        # Act
        options = self.fileManagement.load_data_from_properties_file(input_stream)

        # Assert
        assert options.get_path_parameters() == "params.txt"
        assert options.get_folder_path_out() == "C:/output"
        assert options.get_path_simulator() == "simulator.exe"
        assert options.get_path_to_simulator_result_file() == "result.txt"
        assert options.get_type_of_cuttof_planning() == "INT"
        assert options.get_cuttof_planning() == 10

    def test_load_data_from_properties_file_should_load_criteria_planning_type(self):
        # Arrange
        properties_content = (
            "cuttOfPlanning=0.95\n"
            "typeCuttOfPlanning=CRITERIA\n"
        )
        input_stream = io.BytesIO(properties_content.encode('utf-8'))

        # Act
        options = self.fileManagement.load_data_from_properties_file(input_stream)

        # Assert
        assert options.get_type_of_cuttof_planning() == "CRITERIA"
        assert options.get_stop_criteria() == pytest.approx(0.95, abs=self.delta)

    @pytest.mark.parametrize("type_,value", [
        ("DAY", 15),
        ("HOURS", 10),
        ("MINUTES", 45),
    ])
    def test_load_data_from_properties_file_should_load_calendar_based_planning_types(self, type_, value):
        # Arrange
        properties_content = (
            f"cuttOfPlanning={value}\n"
            f"typeCuttOfPlanning={type_}\n"
        )
        input_stream = io.BytesIO(properties_content.encode('utf-8'))

        # Act
        options = self.fileManagement.load_data_from_properties_file(input_stream)

        # Assert
        assert options.get_type_of_cuttof_planning() == type_

        calendar = options.get_cuttof_planning_h()

        if type_ == "DAY":
            assert calendar.day == value
        elif type_ == "HOURS":
            assert calendar.hour == value
        elif type_ == "MINUTES":
            assert calendar.minute == value

    def test_write_data_in_properties_file_should_create_and_write_properties_file(self):
        # Arrange
        data = {"key1": "value1", "key2": "value2"}
        file = self.tempDir / "test.properties"

        # Act
        self.fileManagement.write_data_in_properties_file(data, str(file), False)

        # Assert
        assert file.exists()

        props = _parse_properties(file.read_text())
        assert props.get("key1") == "value1"
        assert props.get("key2") == "value2"

    def test_write_data_in_properties_file_should_overwrite_existing_file(self):
        # Arrange
        file = self.tempDir / "test.properties"

        first_data = {"oldKey": "oldValue"}
        self.fileManagement.write_data_in_properties_file(first_data, str(file), False)

        second_data = {"newKey": "newValue"}

        # Act
        self.fileManagement.write_data_in_properties_file(second_data, str(file), False)

        props = _parse_properties(file.read_text())

        # Assert
        assert props.get("oldKey") is None
        assert props.get("newKey") == "newValue"

    def test_write_data_in_properties_file_should_create_file_if_it_does_not_exist(self):
        # Arrange
        file = self.tempDir / "newFile.properties"
        data = {"test": "value"}

        # Act
        self.fileManagement.write_data_in_properties_file(data, str(file), False)

        # Assert
        assert file.exists()

    def test_write_data_in_properties_file_should_not_create_file_when_parent_directory_does_not_exist(self):
        # Arrange
        file = self.tempDir / "unknown" / "folder" / "test.properties"
        data = {"key": "value"}

        # Act
        self.fileManagement.write_data_in_properties_file(data, str(file), False)

        # Assert
        assert not file.exists()

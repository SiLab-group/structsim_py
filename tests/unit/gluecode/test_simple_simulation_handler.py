import io
import pytest
from structsim.experimenthandling.measure import Measure
from structsim.experimenthandling.parameter import Parameter
from structsim.gluecode.simple_simulation_handler import SimpleSimulationHandler


class TestSimpleSimulationHandler:

    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        self.handler = SimpleSimulationHandler()
        self.tempDir = tmp_path

    def test_extract_measures_should_parse_file_correctly(self):
        # Arrange
        file = self.tempDir / "results.txt"
        file.write_text("throughput=12\nlatency=50\n")

        # Act
        result = self.handler.extract_measures(str(file))

        # Assert
        assert len(result) == 2

        assert result[0].get_key() == "throughput"
        assert result[0].get_value() == "12"

        assert result[1].get_key() == "latency"
        assert result[1].get_value() == "50"

    def test_read_parameters_file_should_parse_file_from_path(self):
        # Arrange
        file = self.tempDir / "params.txt"
        file.write_text("val1=10\nval2=20.5\n")

        # Act
        result = self.handler.read_parameters_file(str(file))

        # Assert
        assert len(result) == 2

        assert result[0].get_key() == "val1"
        assert result[0].get_value() == 10.0

        assert result[1].get_key() == "val2"
        assert result[1].get_value() == 20.5

    def test_read_parameters_file_should_parse_from_input_stream(self):
        # Arrange
        content = "val1=1\nval2=2.5\n"
        is_ = io.BytesIO(content.encode('utf-8'))

        # Act
        result = self.handler.read_parameters_file(is_)

        # Assert
        assert len(result) == 2

        assert result[0].get_key() == "val1"
        assert result[0].get_value() == 1.0

        assert result[1].get_key() == "val2"
        assert result[1].get_value() == 2.5

    def test_write_parameters_file_should_create_file_with_correct_format(self):
        # Arrange
        params = [
            Parameter("val1", 10),
            Parameter("val2", 20.5),
        ]

        output_dir = str(self.tempDir)

        # Act
        self.handler.write_parameters_file(params, output_dir)

        # Assert
        file = self.tempDir / "myParamFile.txt"

        assert file.exists()

        lines = file.read_text().splitlines()

        assert len(lines) == 2
        assert lines[0] == "val1=10.0"
        assert lines[1] == "val2=20.5"

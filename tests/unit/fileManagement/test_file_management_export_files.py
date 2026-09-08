import pytest
from structsim.experimenthandling.measure import Measure
from .file_management_tests import FileManagementTests


class TestFileManagementExportFiles(FileManagementTests):

    def test_create_measures_file_should_create_measures_file(self, tmp_path):
        # Arrange
        measures = []
        m1 = Measure("throughput", "12")
        m2 = Measure("latency", "50")
        measures.append(m1)
        measures.append(m2)

        measures_file = tmp_path / "measures.txt"

        # Act
        self.fileManagement.create_measures_file(measures, str(measures_file))

        # Assert
        assert measures_file.exists()

        lines = measures_file.read_text().splitlines()

        assert len(lines) == 2
        assert lines[0] == "throughput=12"
        assert lines[1] == "latency=50"

    def test_create_modifier_file_should_create_summary_file(self, tmp_path):
        # Arrange
        modifier = "SIMULATION_FINISHED"

        # Act
        self.fileManagement.create_modifier_file(str(tmp_path), modifier)

        # Assert
        summary_file = tmp_path / "SummaryFile.txt"

        assert summary_file.exists()

        lines = summary_file.read_text().splitlines()

        assert len(lines) == 1
        assert lines[0] == modifier

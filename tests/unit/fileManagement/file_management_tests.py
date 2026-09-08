import pytest
from structsim.util.file_management import FileManagement


class FileManagementTests:

    @pytest.fixture(autouse=True)
    def _setup_base(self, tmp_path):
        self.tempDir = tmp_path
        self.fileManagement = FileManagement()
        self.delta = 1e-9

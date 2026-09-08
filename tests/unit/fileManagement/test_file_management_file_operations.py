from pathlib import Path
from .file_management_tests import FileManagementTests


class TestFileManagementFileOperations(FileManagementTests):

    def test_move_file_should_move_file_when_origin_exists(self):
        # Arrange
        origin      = self.tempDir / "origin.txt"
        destination = self.tempDir / "destination.txt"
        origin.write_text("fileContent")

        # Act
        self.fileManagement.move_file(str(origin), str(destination))

        # Assert
        assert not origin.exists()
        assert destination.exists()
        assert destination.read_text() == "fileContent"

    def test_move_file_should_replace_destination_when_destination_already_exists(self):
        # Arrange
        origin      = self.tempDir / "origin.txt"
        destination = self.tempDir / "destination.txt"
        origin.write_text("newContent")
        destination.write_text("oldContent")

        # Act
        self.fileManagement.move_file(str(origin), str(destination))

        # Assert
        assert not origin.exists()
        assert destination.read_text() == "newContent"

    def test_move_file_should_not_throw_when_origin_does_not_exist(self):
        # Arrange
        non_existent_origin = str(self.tempDir / "ghost.txt")
        destination         = str(self.tempDir / "destination.txt")

        # Act & Assert
        self.fileManagement.move_file(non_existent_origin, destination)
        assert not Path(destination).exists()

    def test_copy_file_should_copy_file_when_source_exists(self):
        # Arrange
        source      = self.tempDir / "source.txt"
        destination = self.tempDir / "destination.txt"
        source.write_text("file content")

        # Act
        self.fileManagement.copy_file(str(source), str(destination))

        # Assert
        assert source.exists(), "Source file must still exist after copy"
        assert destination.exists(), "Destination file must have been created"
        assert destination.read_text() == "file content"

    def test_copy_file_should_replace_destination_when_destination_already_exists(self):
        # Arrange
        source      = self.tempDir / "source.txt"
        destination = self.tempDir / "destination.txt"
        source.write_text("new content")
        destination.write_text("old content")

        # Act
        self.fileManagement.copy_file(str(source), str(destination))

        # Assert
        assert source.exists(), "Source file must still exist after copy"
        assert destination.read_text() == "new content"

    def test_copy_file_should_not_throw_when_source_does_not_exist(self):
        # Arrange
        non_existent_source = str(self.tempDir / "ghost.txt")
        destination         = str(self.tempDir / "destination.txt")

        # Act & Assert
        self.fileManagement.copy_file(non_existent_source, destination)
        assert not Path(destination).exists(), \
            "No destination file should be created if source does not exist"

    def test_create_folder_should_create_folder_when_path_is_valid(self):
        # Arrange
        new_folder = self.tempDir / "newFolder"

        # Act
        self.fileManagement.create_folder(str(new_folder))

        # Assert
        assert new_folder.exists(), "Folder must exist after creation"
        assert new_folder.is_dir(), "Created path must be a directory"

    def test_create_folder_should_not_throw_when_folder_already_exists(self):
        # Arrange
        existing_folder = self.tempDir / "existingFolder"
        existing_folder.mkdir()
        (existing_folder / "file.txt").write_text("existing content")

        # Act & Assert
        self.fileManagement.create_folder(str(existing_folder))
        assert (existing_folder / "file.txt").exists(), \
            "Existing folder content must remain intact"

    def test_create_folder_should_not_create_folder_when_parent_does_not_exist(self):
        # Arrange
        nested_folder = self.tempDir / "nonExistentParent" / "newFolder"

        # Act
        self.fileManagement.create_folder(str(nested_folder))

        # Assert
        assert not nested_folder.exists(), \
            "Folder must not be created if parent directory does not exist"

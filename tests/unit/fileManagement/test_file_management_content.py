from .file_management_tests import FileManagementTests


class TestFileManagementContent(FileManagementTests):

    def test_content_of_a_file_should_return_error_message_when_file_does_not_exist(self):
        # Arrange
        self.fileManagement.set_filename("/noFile.txt")

        # Act
        result = self.fileManagement.content_of_a_file()

        # Assert
        assert result == "this is not a file"

    def test_content_of_a_file_should_return_content_when_file_exists(self):
        # Arrange
        temp_file = self.tempDir / "test.txt"
        temp_file.write_text("Hello World")
        self.fileManagement.set_filename(str(temp_file))

        # Act
        result = self.fileManagement.content_of_a_file()

        # Assert
        assert result == "Hello World"

    def test_content_of_a_file_should_concatenate_lines_when_file_has_multiple_lines(self):
        # Arrange
        temp_file = self.tempDir / "multiline.txt"
        temp_file.write_text("line1\nline2\nline3")
        self.fileManagement.set_filename(str(temp_file))

        # Act
        result = self.fileManagement.content_of_a_file()

        # Assert
        assert result == "line1line2line3"

    def test_content_of_a_file_should_return_empty_string_when_file_is_empty(self):
        # Arrange
        temp_file = self.tempDir / "empty.txt"
        temp_file.write_text("")
        self.fileManagement.set_filename(str(temp_file))

        # Act
        result = self.fileManagement.content_of_a_file()

        # Assert
        assert result == ""

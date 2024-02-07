import pytest

from file_system.commands import FileSystemCommands
from file_system.exceptions import (DestinationPathDoesNotExist,
                                        SourceAndDestinationAreEquals,
                                        SourcePathDoesNotExist)
from settings import FolderSettingsDataClass


def test_create_file_with_source_that_does_not_exist(tmp_destination):
    folder_settings = FolderSettingsDataClass(
        source="not_exist", destination=str(tmp_destination)
    )
    with pytest.raises(SourcePathDoesNotExist):
        FileSystemCommands(folder_settings=folder_settings)


def test_create_file_with_destination_that_does_not_exist(tmp_source):
    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination="not_exist"
    )
    with pytest.raises(DestinationPathDoesNotExist):
        FileSystemCommands(folder_settings=folder_settings)


def test_error_when_source_and_destination_have_the_same_value(tmp_source):
    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_source)
    )
    with pytest.raises(SourceAndDestinationAreEquals):
        FileSystemCommands(folder_settings=folder_settings)

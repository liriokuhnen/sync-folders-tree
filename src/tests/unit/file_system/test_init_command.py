import pytest

from src.file_system.commands import FileSystemCommands
from src.file_system.exceptions import (DestinationPathDoesNotExist,
                                        SourceAndDestinationAreEquals,
                                        SourcePathDoesNotExist)


def test_create_file_with_source_that_does_not_exist(tmp_destination):
    with pytest.raises(SourcePathDoesNotExist):
        FileSystemCommands(source="not_exist", destination=str(tmp_destination))


def test_create_file_with_destination_that_does_not_exist(tmp_source):
    with pytest.raises(DestinationPathDoesNotExist):
        FileSystemCommands(source=str(tmp_source), destination="not_exist")


def test_error_when_source_and_destination_have_the_same_value(tmp_source):
    with pytest.raises(SourceAndDestinationAreEquals):
        FileSystemCommands(source=str(tmp_source), destination=str(tmp_source))

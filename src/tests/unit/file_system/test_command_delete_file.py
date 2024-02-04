import os
from unittest.mock import patch

import pytest

from src.file_system.commands import FileSystemCommands
from src.file_system.exceptions import (BlockDeleteOnSource, ErrorOnDelete,
                                        FileNotFoundOnDelete)
from src.settings import FolderSettingsDataClass
from src.tests.conftest import create_tmp_file

CONTENT = "File Content"


@pytest.mark.parametrize("file", ["not_exist.txt", "not_exist", "", ".", "./", "../"])
def test_delete_file_that_does_not_exist(tmp_source, tmp_destination, file):
    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    f_cli = FileSystemCommands(folder_settings=folder_settings)
    with pytest.raises(FileNotFoundOnDelete):
        f_cli.delete_file(filename=file)


def test_not_allow_delete_folder_instead_file(tmp_source, tmp_destination):
    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    f_cli = FileSystemCommands(folder_settings=folder_settings)

    with pytest.raises(FileNotFoundOnDelete):
        f_cli.delete_file(filename=str(tmp_destination))

    assert os.path.isdir(str(tmp_destination))


def test_delete_file_from_destination(tmp_source, tmp_destination):
    filename = "filename.txt"
    file_path_destination = os.path.join(str(tmp_destination), filename)

    create_tmp_file(tmp_destination, filename, CONTENT)

    assert os.path.isfile(file_path_destination)

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    f_cli = FileSystemCommands(folder_settings=folder_settings)
    f_cli.delete_file(filename=filename, path=str(tmp_destination))

    assert not os.path.isfile(file_path_destination)


def test_not_allow_delete_file_from_source(tmp_source, tmp_destination):
    path = "../source/"
    filename = "filename.txt"
    file_path_source = os.path.join(str(tmp_source), filename)

    create_tmp_file(tmp_source, filename, CONTENT)

    assert os.path.isfile(file_path_source)

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    f_cli = FileSystemCommands(folder_settings=folder_settings)
    with pytest.raises(BlockDeleteOnSource):
        f_cli.delete_file(filename=filename, path=path)

    assert os.path.isfile(file_path_source)


@patch("src.file_system.commands.os.remove")
def test_generic_exception_on_delete(mock_remove, tmp_source, tmp_destination):
    filename = "filename.txt"
    file_path_destination = os.path.join(str(tmp_destination), filename)
    mock_remove.side_effect = IOError()

    create_tmp_file(tmp_destination, filename, CONTENT)

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    f_cli = FileSystemCommands(folder_settings=folder_settings)
    with pytest.raises(ErrorOnDelete):
        f_cli.delete_file(filename=filename, path=str(tmp_destination))

    assert os.path.isfile(file_path_destination)

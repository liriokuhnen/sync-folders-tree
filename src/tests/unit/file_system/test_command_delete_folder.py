import logging
import os
from unittest.mock import patch

import pytest

from file_system.commands import FileSystemCommands
from file_system.exceptions import (BlockDeleteOfDestinationFolder,
                                    BlockDeleteOnSource, ErrorOnDelete,
                                    ErrorOnDeleteFolder, FileNotFoundOnDelete,
                                    FolderNotFoundOnDelete)
from settings import FolderSettingsDataClass
from tests.conftest import create_tmp_file

logger = logging.getLogger()

CONTENT = "File Content"


def test_delete_folder_that_does_not_exist(tmp_source, tmp_destination):
    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    f_cli = FileSystemCommands(folder_settings=folder_settings, logger=logger)
    folder = "not_exist"
    folder_path = os.path.join(str(tmp_destination), folder)

    with pytest.raises(FolderNotFoundOnDelete):
        f_cli.delete_folder(path=folder)

    assert not os.path.isdir(folder_path)


@pytest.mark.parametrize("folder", ["folder_to_delete", ".hidden_folder", "a"])
def test_delete_folder(tmp_source, tmp_destination, folder):
    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    f_cli = FileSystemCommands(folder_settings=folder_settings, logger=logger)
    tmp_destination = tmp_destination / folder
    tmp_destination.mkdir()

    assert os.path.isdir(str(tmp_destination))

    f_cli.delete_folder(path=folder)

    assert not os.path.isdir(str(tmp_destination))



@pytest.mark.parametrize("folder", ["", "/", "//", ".", "./", "..", "../"])
def test_try_delete_root_folder(tmp_source, tmp_destination, folder):
    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    f_cli = FileSystemCommands(folder_settings=folder_settings, logger=logger)

    with pytest.raises(BlockDeleteOfDestinationFolder):
        f_cli.delete_folder(path=folder)
    
    assert os.path.isdir(str(tmp_destination))


@patch("file_system.commands.shutil.rmtree")
def test_generic_exception_on_delete_folder(mock_rmtree, tmp_source, tmp_destination):
    mock_rmtree.side_effect = IOError()
    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    f_cli = FileSystemCommands(folder_settings=folder_settings, logger=logger)
    folder = "new_folder"
    tmp_destination = tmp_destination / folder
    tmp_destination.mkdir()

    with pytest.raises(ErrorOnDeleteFolder):
        f_cli.delete_folder(path=folder)

    assert os.path.isdir(str(tmp_destination))


def test_delete_folder_with_files_inside(tmp_source, tmp_destination):
    filename = "filename.txt"
    sub_folder = "sub_folder"
    folder_destination = os.path.join(str(tmp_destination), sub_folder)
    file_destination = os.path.join(str(tmp_destination), sub_folder, filename)

    create_tmp_file(tmp_destination, filename, CONTENT, sub_folder)

    assert os.path.isfile(file_destination)
    assert os.path.isdir(folder_destination)

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    f_cli = FileSystemCommands(folder_settings=folder_settings, logger=logger)
    f_cli.delete_folder(path=sub_folder)

    assert not os.path.isfile(file_destination)
    assert not os.path.isdir(folder_destination)

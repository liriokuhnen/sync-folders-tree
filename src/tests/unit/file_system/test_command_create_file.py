import logging
import os

import pytest

from file_system.commands import FileSystemCommands
from file_system.exceptions import FileOrDirectoryNotFound
from settings import FolderSettingsDataClass
from tests.conftest import create_tmp_file

logger = logging.getLogger()

CONTENT = "File Content"


def test_create_file_that_does_not_exist(tmp_source, tmp_destination):
    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    f_cli = FileSystemCommands(folder_settings=folder_settings, logger=logger)
    with pytest.raises(FileOrDirectoryNotFound):
        f_cli.create_file(path="does_not_exist_file.txt")


def test_create_file_on_destination(tmp_source, tmp_destination):
    filename = "filename.txt"
    file_path_source = os.path.join(str(tmp_source), filename)
    file_path_destination = os.path.join(str(tmp_destination), filename)

    create_tmp_file(tmp_source, filename, CONTENT)

    assert os.path.isfile(file_path_source)
    assert not os.path.isfile(file_path_destination)

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    f_cli = FileSystemCommands(folder_settings=folder_settings, logger=logger)
    f_cli.create_file(path=filename)

    with open(file_path_destination, "r") as destination_file:
        destination_file_content = destination_file.read()

    assert os.path.isfile(file_path_source)
    assert os.path.isfile(file_path_destination)
    assert destination_file_content == CONTENT


def test_create_file_with_sub_folders_on_destination_that_does_not_exist(
    tmp_source, tmp_destination
):
    filename = "filename.txt"
    sub_folders = "sub_folder1/sub_folder2"
    filename_path = os.path.join(sub_folders, filename)
    file_path_source = os.path.join(str(tmp_source), sub_folders, filename)
    file_path_destination = os.path.join(str(tmp_destination), sub_folders, filename)

    create_tmp_file(tmp_source, filename, CONTENT, sub_folders)

    assert os.path.isfile(file_path_source)
    assert not os.path.isfile(file_path_destination)

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    f_cli = FileSystemCommands(folder_settings=folder_settings, logger=logger)
    with pytest.raises(FileOrDirectoryNotFound):
        f_cli.create_file(path=filename_path)

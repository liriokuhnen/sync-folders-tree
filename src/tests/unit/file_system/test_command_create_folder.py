import os

import pytest

from src.file_system.commands import FileSystemCommands
from src.file_system.exceptions import (BlockCreateFolderOnSource,
                                        ErrorOnCreateFolder)
from src.settings import FolderSettingsDataClass
from src.tests.conftest import create_tmp_file


def test_create_folder(tmp_source, tmp_destination):
    folder = "sub_folder"
    folder_path = os.path.join(tmp_destination, folder)

    assert not os.path.isdir(folder_path)

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    f_cli = FileSystemCommands(folder_settings=folder_settings)
    f_cli.create_folder(path=folder)

    assert os.path.isdir(folder_path)


def test_create_folder_that_already_exist(tmp_source, tmp_destination):
    assert os.path.isdir(str(tmp_destination))

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    f_cli = FileSystemCommands(folder_settings=folder_settings)
    with pytest.raises(ErrorOnCreateFolder):
        f_cli.create_folder(path=str(tmp_destination))


def test_error_on_create_two_sub_folder_at_once(tmp_source, tmp_destination):
    folder = "sub_folder1/sub_folder2"
    folder_path = os.path.join(tmp_destination, folder)

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    f_cli = FileSystemCommands(folder_settings=folder_settings)
    with pytest.raises(ErrorOnCreateFolder):
        f_cli.create_folder(path=folder)

    assert not os.path.isdir(folder_path)


def test_error_on_create_folder_that_already_exist_as_file(tmp_source, tmp_destination):
    filename = "file_that_looks_a_folder"
    file_path_destination = os.path.join(str(tmp_destination), filename)

    create_tmp_file(tmp_destination, filename, "File Content")

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    f_cli = FileSystemCommands(folder_settings=folder_settings)
    with pytest.raises(ErrorOnCreateFolder):
        f_cli.create_folder(path=filename)

    assert os.path.isfile(file_path_destination)


def test_error_on_create_a_folder_on_source(tmp_source, tmp_destination):
    folder = "../source/sub_folder"
    folder_path = os.path.join(tmp_source, folder)

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    f_cli = FileSystemCommands(folder_settings=folder_settings)
    with pytest.raises(BlockCreateFolderOnSource):
        f_cli.create_folder(path=folder)

    assert not os.path.isdir(folder_path)

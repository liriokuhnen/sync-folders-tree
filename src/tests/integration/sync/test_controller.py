import os

import pytest

from src.settings import DiffActionsEnum, FolderSettingsDataClass
from src.sync.controller import SyncController
from src.tests.conftest import create_tmp_file, create_tmp_folder

LEVEL_1  = [
    {"name": "file1.txt", "content": "content file 1"},
    {"name": "file2.txt", "content": "content file 2"},
    {"name": "file3.txt", "content": "content file 3"},
]

LEVEL_2 = [
    {"name": "sub_file1.txt", "content": "content file 1"},
    {"name": "sub_file2.txt", "content": "content file 2"},
]


def test_sync_all_files_and_folders_on_destination(tmp_source, tmp_destination):
    for file_create in LEVEL_1:
        create_tmp_file(tmp_source, file_create["name"], file_create["content"])

    sub_folder_1 = "subfolder_1"
    tmp_sub_folder = create_tmp_folder(tmp_source, sub_folder_1)

    for file_create in LEVEL_2:
        create_tmp_file(tmp_sub_folder, file_create["name"], file_create["content"])
    
    assert not os.path.isfile(os.path.join(str(tmp_destination), "file1.txt"))
    assert not os.path.isfile(os.path.join(str(tmp_destination), "file2.txt"))
    assert not os.path.isfile(os.path.join(str(tmp_destination), "file3.txt"))
    assert not os.path.isdir(os.path.join(str(tmp_destination), sub_folder_1))
    assert not os.path.isfile(
        os.path.join(str(tmp_destination), sub_folder_1 + "/sub_file1.txt"))
    assert not os.path.isfile(
        os.path.join(str(tmp_destination), sub_folder_1 +"/sub_file2.txt"))

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )

    sync_controller = SyncController(folder_settings=folder_settings)
    sync_controller.execute()

    assert os.path.isfile(os.path.join(str(tmp_destination), "file1.txt"))
    assert os.path.isfile(os.path.join(str(tmp_destination), "file2.txt"))
    assert os.path.isfile(os.path.join(str(tmp_destination), "file3.txt"))
    assert os.path.isdir(os.path.join(str(tmp_destination), sub_folder_1))
    assert os.path.isfile(
        os.path.join(str(tmp_destination), sub_folder_1 + "/sub_file1.txt"))
    assert os.path.isfile(
        os.path.join(str(tmp_destination), sub_folder_1 +"/sub_file2.txt"))


def test_sync_delete_files_and_folder_that_only_exist_on_destination(
    tmp_source, tmp_destination
):
    for file_create in LEVEL_1:
        create_tmp_file(tmp_destination, file_create["name"], file_create["content"])

    sub_folder_1 = "subfolder_1"
    tmp_sub_folder = create_tmp_folder(tmp_destination, sub_folder_1)

    for file_create in LEVEL_2:
        create_tmp_file(tmp_sub_folder, file_create["name"], file_create["content"])

    assert os.path.isfile(os.path.join(str(tmp_destination), "file1.txt"))
    assert os.path.isfile(os.path.join(str(tmp_destination), "file2.txt"))
    assert os.path.isfile(os.path.join(str(tmp_destination), "file3.txt"))
    assert os.path.isdir(os.path.join(str(tmp_destination), sub_folder_1))
    assert os.path.isfile(
        os.path.join(str(tmp_destination), sub_folder_1 + "/sub_file1.txt"))
    assert os.path.isfile(
        os.path.join(str(tmp_destination), sub_folder_1 +"/sub_file2.txt"))

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )

    sync_controller = SyncController(folder_settings=folder_settings)
    sync_controller.execute()

    assert not os.path.isfile(os.path.join(str(tmp_destination), "file1.txt"))
    assert not os.path.isfile(os.path.join(str(tmp_destination), "file2.txt"))
    assert not os.path.isfile(os.path.join(str(tmp_destination), "file3.txt"))
    assert not os.path.isdir(os.path.join(str(tmp_destination), sub_folder_1))
    assert not os.path.isfile(
        os.path.join(str(tmp_destination), sub_folder_1 + "/sub_file1.txt"))
    assert not os.path.isfile(
        os.path.join(str(tmp_destination), sub_folder_1 +"/sub_file2.txt"))


def test_execute_sync_update_on_second_call(tmp_source, tmp_destination):
    file_name = "file_name.txt"
    sub_folder = "sub_folder"
    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )

    sync_controller = SyncController(folder_settings=folder_settings)
    sync_controller.execute()

    assert len(os.listdir(str(tmp_destination))) == 0

    create_tmp_file(tmp_source, file_name, "Content")
    tmp_sub_folder = create_tmp_folder(tmp_source, sub_folder)

    # second execute
    sync_controller.execute()

    assert len(os.listdir(str(tmp_destination))) == 2
    assert file_name in os.listdir(str(tmp_destination))
    assert sub_folder in os.listdir(str(tmp_destination))


def test_execute_sync_delete_on_second_call(tmp_source, tmp_destination):
    file_name = "file_name.txt"
    sub_folder = "sub_folder"

    create_tmp_file(tmp_source, file_name, "Content")
    create_tmp_file(tmp_destination, file_name, "Content")
    tmp_sub_folder = create_tmp_folder(tmp_source, sub_folder)
    tmp_sub_folder = create_tmp_folder(tmp_destination, sub_folder)

    assert len(os.listdir(str(tmp_source))) == 2
    assert len(os.listdir(str(tmp_destination))) == 2

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )

    sync_controller = SyncController(folder_settings=folder_settings)
    sync_controller.execute()

    # delete from source
    os.remove(os.path.join(str(tmp_source), file_name))
    os.rmdir(os.path.join(str(tmp_source), sub_folder))

    assert len(os.listdir(str(tmp_source))) == 0
    assert len(os.listdir(str(tmp_destination))) == 2

    # second execute
    sync_controller.execute()

    assert len(os.listdir(str(tmp_source))) == 0
    assert len(os.listdir(str(tmp_destination))) == 0

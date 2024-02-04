import os

import pytest

from src.diff_folders.walk_tree import DiffTree
from src.settings import DiffActionsEnum, FolderSettingsDataClass
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


def test_get_actions_create_when_file_and_folder_only_exist_on_source(
    tmp_source, tmp_destination
):
    for file_create in LEVEL_1:
        create_tmp_file(tmp_source, file_create["name"], file_create["content"])

    sub_folder_1 = "subfolder_1"
    tmp_sub_folder = create_tmp_folder(tmp_source, sub_folder_1)

    for file_create in LEVEL_2:
        create_tmp_file(tmp_sub_folder, file_create["name"], file_create["content"])

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )

    expected = {
        "file1.txt": DiffActionsEnum.CREATE_FILE,
        "file2.txt": DiffActionsEnum.CREATE_FILE,
        "file3.txt": DiffActionsEnum.CREATE_FILE,
        sub_folder_1: DiffActionsEnum.CREATE_FOLDER,
        sub_folder_1 + "/sub_file1.txt": DiffActionsEnum.CREATE_FILE,
        sub_folder_1 +"/sub_file2.txt": DiffActionsEnum.CREATE_FILE,
    }

    diff_tree = DiffTree(folder_settings=folder_settings)
    get_actions = diff_tree.get_actions()

    for count, action in enumerate(get_actions, 1):
        path = os.path.join(action.common_root, action.name)
        assert expected[path] == action.action

    assert count == len(expected.items())


def test_get_actions_delete_when_file_and_folder_exist_only_on_destination(
    tmp_source, tmp_destination
):
    for file_create in LEVEL_1:
        create_tmp_file(tmp_destination, file_create["name"], file_create["content"])

    sub_folder_1 = "subfolder_1"
    tmp_sub_folder = create_tmp_folder(tmp_destination, sub_folder_1)
    sub_folder_2 = "subfolder_2"
    tmp_sub_folder = create_tmp_folder(tmp_destination, sub_folder_2)

    for file_create in LEVEL_2:
        create_tmp_file(tmp_sub_folder, file_create["name"], file_create["content"])

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )

    expected = {
        "file1.txt": DiffActionsEnum.DELETE_FILE,
        "file2.txt": DiffActionsEnum.DELETE_FILE,
        "file3.txt": DiffActionsEnum.DELETE_FILE,
        sub_folder_1: DiffActionsEnum.DELETE_FOLDER,
        sub_folder_2: DiffActionsEnum.DELETE_FOLDER,
    }

    diff_tree = DiffTree(folder_settings=folder_settings)
    get_actions = diff_tree.get_actions()

    for count, action in enumerate(get_actions, 1):
        path = os.path.join(action.common_root, action.name)
        assert expected[path] == action.action

    assert count == len(expected.items())


def test_get_actions_update_when_file_exist_in_both_but_is_not_the_same(
    tmp_source, tmp_destination
):
    for file_create in LEVEL_1:
        create_tmp_file(tmp_source, file_create["name"], file_create["content"])
        create_tmp_file(tmp_destination, file_create["name"], "other value")

    sub_folder_1 = "subfolder_1"
    src_tmp_sub_folder = create_tmp_folder(tmp_source, sub_folder_1)
    dest_tmp_sub_folder = create_tmp_folder(tmp_destination, sub_folder_1)

    for file_create in LEVEL_2:
        create_tmp_file(src_tmp_sub_folder, file_create["name"], file_create["content"])
        create_tmp_file(
            dest_tmp_sub_folder, file_create["name"], "other value"
        )

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )

    expected = {
        "file1.txt": DiffActionsEnum.UPDATE_FILE,
        "file2.txt": DiffActionsEnum.UPDATE_FILE,
        "file3.txt": DiffActionsEnum.UPDATE_FILE,
        sub_folder_1 + "/sub_file1.txt": DiffActionsEnum.UPDATE_FILE,
        sub_folder_1 +"/sub_file2.txt": DiffActionsEnum.UPDATE_FILE,
    }

    diff_tree = DiffTree(folder_settings=folder_settings)
    get_actions = diff_tree.get_actions()

    for count, action in enumerate(get_actions, 1):
        path = os.path.join(action.common_root, action.name)
        assert expected[path] == action.action

    assert count == len(expected.items())


def test_get_any_actions_when_both_folders_is_synced(tmp_source, tmp_destination):
    for file_create in LEVEL_1:
        create_tmp_file(tmp_source, file_create["name"], file_create["content"])
        create_tmp_file(tmp_destination, file_create["name"], file_create["content"])

    sub_folder_1 = "subfolder_1"
    src_tmp_sub_folder = create_tmp_folder(tmp_source, sub_folder_1)
    dest_tmp_sub_folder = create_tmp_folder(tmp_destination, sub_folder_1)

    for file_create in LEVEL_2:
        create_tmp_file(src_tmp_sub_folder, file_create["name"], file_create["content"])
        create_tmp_file(
            dest_tmp_sub_folder, file_create["name"], file_create["content"]
        )

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )

    diff_tree = DiffTree(folder_settings=folder_settings)
    get_actions = diff_tree.get_actions()

    count = 0
    for action in get_actions:
        count+=1

    assert count == 0

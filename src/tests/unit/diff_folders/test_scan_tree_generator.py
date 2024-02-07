import os

import pytest

from diff_folders.walk_tree import DiffTree
from settings import FolderSettingsDataClass
from tests.conftest import create_tmp_file, create_tmp_folder

LEVEL_1  = [
    {"name": "file1.txt", "content": "content file 1"},
    {"name": "file2.txt", "content": "content file 2"},
    {"name": "file3.txt", "content": "content file 3"},
]

LEVEL_2 = [
    {"name": "sub_file1.txt", "content": "content file 1"},
    {"name": "sub_file2.txt", "content": "content file 2"},
]


def test_scan_tree_generator_with_files_only_on_source(tmp_source, tmp_destination):
    for file_create in LEVEL_1:
        create_tmp_file(tmp_source, file_create["name"], file_create["content"])

    sub_folder_1 = "subfolder_1"
    tmp_sub_folder = create_tmp_folder(tmp_source, sub_folder_1)

    for file_create in LEVEL_2:
        create_tmp_file(tmp_sub_folder, file_create["name"], file_create["content"])

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )

    diff_tree = DiffTree(folder_settings=folder_settings)
    scan_diff_generator = diff_tree._scan_tree_generator()

    first_level = next(scan_diff_generator)

    assert first_level.common_root == ""
    assert first_level.source.folders == {sub_folder_1}
    assert first_level.destination.folders == set()
    # check all files exist on source
    for file in LEVEL_1:
        assert file["name"] in first_level.source.files
    # check files does not exist on destination
    assert first_level.destination.folders == set()
    assert first_level.destination.files == set()

    second_level = next(scan_diff_generator)
    
    assert second_level.common_root == sub_folder_1
    assert second_level.source.folders == set()
    # check all files exist on source
    for file in LEVEL_2:
        assert file["name"] in second_level.source.files
    # check files does not exist on destination
    assert second_level.destination.folders == set()
    assert second_level.destination.files == set()

    with pytest.raises(StopIteration):
        next(scan_diff_generator)


def test_scan_tree_generator_with_files_on_source_and_destination(
    tmp_source, tmp_destination
):
    for file_create in LEVEL_1:
        create_tmp_file(tmp_source, file_create["name"], file_create["content"])
        create_tmp_file(tmp_destination, file_create["name"], file_create["content"])

    sub_folder_1 = "subfolder_1"
    tmp_src_sub_folder = create_tmp_folder(tmp_source, sub_folder_1)
    tmp_dest_sub_folder = create_tmp_folder(tmp_destination, sub_folder_1)

    for file_create in LEVEL_2:
        create_tmp_file(tmp_src_sub_folder, file_create["name"], file_create["content"])
        create_tmp_file(tmp_dest_sub_folder, file_create["name"], file_create["content"])

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )

    diff_tree = DiffTree(folder_settings=folder_settings)
    scan_diff_generator = diff_tree._scan_tree_generator()

    first_level = next(scan_diff_generator)

    assert first_level.common_root == ""
    assert first_level.source.folders == {sub_folder_1}
    assert first_level.destination.folders == {sub_folder_1}
    # check all files exist on source and destination
    for file in LEVEL_1:
        assert file["name"] in first_level.source.files
        assert file["name"] in first_level.destination.files

    second_level = next(scan_diff_generator)
    
    assert second_level.common_root == sub_folder_1
    assert second_level.source.folders == set()
    assert second_level.destination.folders == set()
    # check all files exist on source and destination
    for file in LEVEL_2:
        assert file["name"] in second_level.source.files
        assert file["name"] in second_level.destination.files

    with pytest.raises(StopIteration):
        next(scan_diff_generator)


def test_scan_tree_generator_with_files_only_on_destination(
    tmp_source, tmp_destination
):
    for file_create in LEVEL_1:
        create_tmp_file(tmp_destination, file_create["name"], file_create["content"])

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )

    diff_tree = DiffTree(folder_settings=folder_settings)
    scan_diff_generator = diff_tree._scan_tree_generator()

    first_level = next(scan_diff_generator)

    assert first_level.common_root == ""
    assert first_level.source.folders == set()
    assert first_level.destination.folders == set()
    # check all files exist on destination
    for file in LEVEL_1:
        assert file["name"] in first_level.destination.files
    # check files does not exist on source
    assert first_level.source.folders == set()
    assert first_level.source.files == set()

    with pytest.raises(StopIteration):
        next(scan_diff_generator)


def test_scan_tree_generator_without_any_file(tmp_source, tmp_destination):
    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )

    diff_tree = DiffTree(folder_settings=folder_settings)
    scan_diff_generator = diff_tree._scan_tree_generator()

    first_level = next(scan_diff_generator)

    assert first_level.common_root == ""
    assert first_level.source.folders == set()
    assert first_level.source.files == set()
    assert first_level.destination.files == set()
    assert first_level.destination.files == set()

    with pytest.raises(StopIteration):
        next(scan_diff_generator)

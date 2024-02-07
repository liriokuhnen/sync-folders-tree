import os
import random
import string

import pytest

from diff_folders.walk_tree import DiffTree
from settings import FolderSettingsDataClass
from tests.conftest import create_tmp_file


def get_random_string(length, letters):
    return ''.join(random.choice(letters) for i in range(length))


def test_compare_same_file(tmp_source, tmp_destination):
    filename = "file.txt"
    content = get_random_string(1024 * 256, string.printable)
    
    create_tmp_file(tmp_source, filename, content)
    create_tmp_file(tmp_destination, filename, content)

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    diff_tree = DiffTree(folder_settings=folder_settings)

    assert diff_tree._diff_file_sha256(common_root="", filename=filename)


def test_compare_different_files(tmp_source, tmp_destination):
    filename = "file.txt"
    content_1 = get_random_string(1024 * 256, string.ascii_letters + string.punctuation)
    content_2 = get_random_string(1024 * 256, string.ascii_uppercase + string.punctuation)
    
    create_tmp_file(tmp_source, filename, content_1)
    create_tmp_file(tmp_destination, filename, content_2)

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    diff_tree = DiffTree(folder_settings=folder_settings)

    assert not diff_tree._diff_file_sha256(common_root="", filename=filename)


def test_compare_almost_the_same_with_last_letter_different(
    tmp_source, tmp_destination
):
    filename = "file.txt"
    content_1 = get_random_string(1024 * 256, "abcdefg")
    content_2 = content_1[:-1] + "h"
    
    create_tmp_file(tmp_source, filename, content_1)
    create_tmp_file(tmp_destination, filename, content_2)

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    diff_tree = DiffTree(folder_settings=folder_settings)

    assert not diff_tree._diff_file_sha256(common_root="", filename=filename)


def test_compare_almost_the_same_with_first_letter_different(
    tmp_source, tmp_destination
):
    filename = "file.txt"
    content_1 = get_random_string(1024 * 256, "abcdefg")
    content_2 = "h" + content_1[1:]
    
    create_tmp_file(tmp_source, filename, content_1)
    create_tmp_file(tmp_destination, filename, content_2)

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    diff_tree = DiffTree(folder_settings=folder_settings)

    assert not diff_tree._diff_file_sha256(common_root="", filename=filename)


def test_compare_empty_files(tmp_source, tmp_destination):
    filename = "file.txt"
    
    create_tmp_file(tmp_source, filename, "")
    create_tmp_file(tmp_destination, filename, "")

    folder_settings = FolderSettingsDataClass(
        source=str(tmp_source), destination=str(tmp_destination)
    )
    diff_tree = DiffTree(folder_settings=folder_settings)

    assert diff_tree._diff_file_sha256(common_root="", filename=filename)

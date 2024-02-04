import shutil

import pytest


@pytest.fixture
def tmp_source(tmp_path):
    # Create temporary source folder
    tmp_source = tmp_path / "source"
    tmp_source.mkdir()

    yield tmp_source

    # Remove source folder after the test
    shutil.rmtree(str(tmp_source))


@pytest.fixture
def tmp_destination(tmp_path):
    # Create temporary destination folder
    tmp_destination = tmp_path / "destination"
    tmp_destination.mkdir()

    yield tmp_destination

    # Remove destination folder after the test
    shutil.rmtree(str(tmp_destination))


def create_tmp_file(tmp_folder, filename, content, sub_folders=None):
    if sub_folders:
        for sub_folder in sub_folders.split("/"):
            tmp_folder = tmp_folder / sub_folder
            tmp_folder.mkdir()

    file = tmp_folder / filename
    file.write_text(content)
    return file


def create_tmp_folder(tmp_folder, new_folder):
    tmp_folder = tmp_folder / new_folder
    tmp_folder.mkdir()
    return tmp_folder

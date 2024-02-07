"""
This module will walk through a source folder tree in order to get the
differences from destination, with the control level of how deep will be the diff
"""

import hashlib
import os
from dataclasses import dataclass
from typing import Generator, List, Optional

from settings import BUF_SIZE, DiffActionsEnum, FolderSettingsDataClass


@dataclass
class BaseStructure:
    """Base structure for holde tree folders information"""
    folders: List[str]
    files: List[str]


@dataclass
class SourceStructure(BaseStructure):
    """Structure of source"""


@dataclass
class DestinationStructure(BaseStructure):
    """Structure of destination"""


@dataclass
class DiffResponse:
    """Data response of diff between source and destination"""
    common_root: str
    source: SourceStructure
    destination: DestinationStructure


@dataclass
class GetActionResponse:
    """Data response with required action to keep destination synced"""
    common_root: str
    name: str
    action: DiffActionsEnum


class DiffTree:  # pylint: disable=too-few-public-methods
    """Scan folders tree to identify the differences and required sync actions"""

    def __init__(
        self, folder_settings: FolderSettingsDataClass, sha256: bool = False
    ) -> None:
        """
        Settings of source and destination and strategy of diff files
        (sha256 or file size + last modified date)
        """
        self._folder_settings = folder_settings
        self._compare_file = self._diff_file_sha256 if sha256 else self._diff_size_mtime

    def get_actions(self) -> Optional[Generator[GetActionResponse, None, None]]:
        """
        Method to get actions create, delete or update doing a diff between
        source and destination.

        comparing the filename combined with filesize plus last modified date, the
        objective is identify if update action is required without opening and reading
        all files
        """
        diff_scan = self._scan_tree_generator()

        for diff in diff_scan:
            files_create = diff.source.files - diff.destination.files
            for file_create in files_create:
                yield GetActionResponse(
                   common_root=diff.common_root,
                   name=file_create,
                   action=DiffActionsEnum.CREATE_FILE,
                )

            files_delete = diff.destination.files - diff.source.files
            for file_delete in files_delete:
                yield GetActionResponse(
                   common_root=diff.common_root,
                   name=file_delete,
                   action=DiffActionsEnum.DELETE_FILE,
                )

            files_check = diff.source.files - files_create
            for file_check in files_check:
                if self._compare_file(
                    common_root=diff.common_root, filename=file_check
                ):
                    yield GetActionResponse(
                       common_root=diff.common_root,
                       name=file_check,
                       action=DiffActionsEnum.UPDATE_FILE,
                    )

            folders_create = diff.source.folders - diff.destination.folders
            for folder_create in folders_create:
                yield GetActionResponse(
                   common_root=diff.common_root,
                   name=folder_create,
                   action=DiffActionsEnum.CREATE_FOLDER,
                )

            folders_delete = diff.destination.folders - diff.source.folders
            for folder_delete in folders_delete:
                yield GetActionResponse(
                   common_root=diff.common_root,
                   name=folder_delete,
                   action=DiffActionsEnum.DELETE_FOLDER,
                )


    def _scan_tree_generator(self) -> Generator[DiffResponse, None, None]:
        """Method that will get differences by file and folder name
        between source and destination, scanning all levels folders tree"""

        for src_root, src_folders, src_files in os.walk(self._folder_settings.source):
            common_root = self._get_common_root(src_root)
            destination_path = os.path.join(
                self._folder_settings.destination, common_root
            )

            destination_walk = os.walk(destination_path)

            try:
                _, dest_folders, dest_files = next(destination_walk)
            except StopIteration:
                dest_folders, dest_files = [], []

            source = SourceStructure(folders=set(src_folders), files=set(src_files))
            destination = DestinationStructure(
                folders=set(dest_folders), files=set(dest_files)
            )

            yield DiffResponse(
                common_root=common_root, source=source, destination=destination
            )

    def _diff_size_mtime(self, common_root: str, filename:str) -> bool:
        """
        This method will compare file from source and destination checking by filesize
        and last modified date in order to evaluate if the file need to be updated

        this check will avoid the need to open and read the file to confirm if the file
        should be synced, which means less computer resource, but this check not 100%
        precise once it will rely on OS file date updating which could be misupdated
        """
        source_file_path = os.path.join(
            self._folder_settings.source, common_root, filename
        )
        destination_file_path = os.path.join(
            self._folder_settings.destination, common_root, filename
        )

        src_st = os.stat(source_file_path)
        dest_st = os.stat(destination_file_path)

        return src_st.st_size != dest_st.st_size or src_st.st_mtime != dest_st.st_mtime


    def _diff_file_sha256(self, common_root: str, filename:str) -> bool:
        """
        This method will compare both files reading all content and generating
        his sha256 in order to check if the file have the same content
        """

        def file_hash(file):
            sha256 = hashlib.sha256()
            with open(file, 'rb') as f:
                while True:
                    data = f.read(BUF_SIZE)

                    if not data:
                        break

                    sha256.update(data)

            return sha256.hexdigest()

        source_file_path = os.path.join(
            self._folder_settings.source, common_root, filename
        )
        destination_file_path = os.path.join(
            self._folder_settings.destination, common_root, filename
        )

        return file_hash(source_file_path) == file_hash(destination_file_path)


    def _get_common_root(self, root):
        """
        Remove the absolute path from source to keep the common root for both
        source and destination
        """
        return root.replace(self._folder_settings.source, "").removeprefix("/")

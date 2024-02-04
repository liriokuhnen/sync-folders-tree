"""
This module will walk through a source folder tree in order to get the
differences from destination, with the control level of how deep will be the diff
"""

import os
from dataclasses import dataclass
from typing import Generator, List

from src.settings import FolderSettingsDataClass


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


class DiffTree:
    """Scan folders tree to identify the differences and required sync actions"""

    def __init__(
        self, folder_settings: FolderSettingsDataClass
    ) -> None:
        """Settings of source and destination"""
        self._folder_settings = folder_settings

    def _scan_tree_generator(self) -> Generator[DiffResponse, None, None]:
        """Method that will get differences by file and folder name
        between source and destination, scanning all levels folders tree"""

        for src_root, src_folders, src_files in os.walk(self._folder_settings.source):
            common_root = self._get_common_root(src_root)
            destination_path = os.path.join(self._folder_settings.destination, common_root)

            destination_walk = os.walk(destination_path)

            try:
                _, dest_folders, dest_files = next(destination_walk)
            except StopIteration:
                dest_folders, dest_files = [], []

            source = SourceStructure(folders=src_folders, files=src_files)
            destination = DestinationStructure(folders=dest_folders, files=dest_files)

            yield DiffResponse(
                common_root=common_root, source=source, destination=destination
            )

    def _get_common_root(self, root):
        """
        Remove the absolute path from source to keep the common root for both
        source and destination
        """
        return root.replace(self._folder_settings.source, "").removeprefix("/")

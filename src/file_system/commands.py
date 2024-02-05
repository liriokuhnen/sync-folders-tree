"""
File system module to manage the files and folders of source and destination
"""

import logging
import os
import shutil

from src.file_system.exceptions import (BlockCreateFolderOnSource,
                                        BlockDeleteOfDestinationFolder,
                                        BlockDeleteOnSource,
                                        DestinationPathDoesNotExist,
                                        ErrorOnCreateFolder, ErrorOnDelete,
                                        ErrorOnDeleteFolder,
                                        FileNotFoundOnDelete,
                                        FileOrDirectoryNotFound,
                                        FolderNotFoundOnDelete,
                                        SourceAndDestinationAreEquals,
                                        SourcePathDoesNotExist)
from src.settings import FolderSettingsDataClass


class FileSystemCommands:
    """
    Class to handle file system commands
    """

    def __init__(self, folder_settings: FolderSettingsDataClass) -> None:
        """
        Define source and destination root path

        :raises:
            SourcePathDoesNotExist: if source does not exist.
            DestinationPathDoesNotExist: if destination does not exist.
        """
        self._source = folder_settings.source
        self._destination = folder_settings.destination

        self._check_root_folders()


    def create_file(self, path: str) -> None:
        """
        Create a specific file from source to destination, source file and destination
        directory must exist

        :raises:
            FileOrDirectoryNotFound: if file or directory is not found.
        """
        source_path = os.path.normpath(os.path.join(self._source, path))
        destination_path = os.path.normpath(os.path.join(self._destination, path))

        try:
            shutil.copy2(source_path, destination_path)
        except FileNotFoundError as err:
            logging.warning("Error on copy file: %s - %s", err.filename, err.strerror)
            raise FileOrDirectoryNotFound from err


    def delete_file(self, path: str) -> None:
        """
        Delete a specific file on destination

        :raises:
            FileNotFoundOnDelete: if file not found on destination.
            BlockDeleteOnSource: block delete file on source.
            ErrorOnDelete: when os error happen on delete file
        """
        destination_path = os.path.normpath(
            os.path.join(self._destination, path)
        )

        if not os.path.isfile(destination_path):
            raise FileNotFoundOnDelete

        # Security check to block delete on source
        if destination_path.startswith(self._source):
            raise BlockDeleteOnSource

        try:
            os.remove(destination_path)
        except OSError as err:
            logging.warning("Error on delete: %s - %s.", err.filename, err.strerror)
            raise ErrorOnDelete from err


    def create_folder(self, path: str) -> None:
        """
        Create folder on destination

        :raises:
            ErrorOnCreateFolder: when a folder already exist or is not found.
            BlockCreateFolderOnSource: block create folder on source.
        """
        folder_path = os.path.normpath(os.path.join(self._destination, path))

        # Security check to block create folder on source
        if folder_path.startswith(self._source):
            raise BlockCreateFolderOnSource

        try:
            os.mkdir(folder_path)
        except (FileExistsError, FileNotFoundError) as err:
            logging.warning(
                "Error on create folder %s - %s.", err.filename, err.strerror
            )
            raise ErrorOnCreateFolder from err


    def delete_folder(self, path: str) -> None:
        """
        Delete folder on destination

        :raises:
            FolderNotFoundOnDelete: when folder to delete is not found
            BlockDeleteOfDestinationFolder: block to prevent delete root destination
            ErrorOnDeleteFolder: when a os error happen in the delete
        """
        folder_path = os.path.normpath(os.path.join(self._destination, path))

        # check if the folder_path is not the destination root
        if len(folder_path) <= len(self._destination) + 1:
            raise BlockDeleteOfDestinationFolder

        if not os.path.isdir(folder_path):
            raise FolderNotFoundOnDelete

        try:
            shutil.rmtree(folder_path)
        except OSError as err:
            logging.warning(
                "Error on delete folder: %s - %s.", err.filename, err.strerror
            )
            raise ErrorOnDeleteFolder from err


    def _check_root_folders(self):
        """
        Check settings of source and destination
        """
        if not os.path.isdir(self._source):
            raise SourcePathDoesNotExist

        if not os.path.isdir(self._destination):
            raise DestinationPathDoesNotExist

        if self._source == self._destination:
            raise SourceAndDestinationAreEquals

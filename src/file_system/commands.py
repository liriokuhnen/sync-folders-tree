"""
File system module to manage the files and directories of source and destination
"""

import logging
import os
import shutil

from src.file_system.exceptions import (BlockCreateFolderOnSource,
                                        BlockDeleteOnSource,
                                        DestinationPathDoesNotExist,
                                        ErrorOnDelete, FileNotFoundOnDelete,
                                        FileOrDirectoryNotFound,
                                        FolderAlreadyExist,
                                        SourcePathDoesNotExist)


class FileSystemCommands:
    """
    Class to handle file system commands
    """

    def __init__(self, source: str, destination: str) -> None:
        """
        Define source and destination root path

        :raises:
            SourcePathDoesNotExist: if source does not exist.
            DestinationPathDoesNotExist: if destination does not exist.
        """
        self._source = source
        self._destination = destination

        self._check_root_folders()


    def create_file(self, filename: str, path: str = "") -> None:
        """
        Create a specific file from source to destination, source file and destination
        directory must exist

        :raises:
            FileOrDirectoryNotFound: if file or directory is not found.
        """
        source_path = os.path.join(self._source, path, filename)
        destination_path = os.path.join(self._destination, path)

        try:
            shutil.copy2(source_path, destination_path)
        except FileNotFoundError as err:
            logging.warning("Error on copy file: %s - %s", err.filename, err.strerror)
            raise FileOrDirectoryNotFound from err


    def delete_file(self, filename: str, path: str = "") -> None:
        """
        Delete a specific file on destination

        :raises:
            FileNotFoundOnDelete: if file not found on destination.
        """
        destination_path = os.path.join(self._destination, path, filename)

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


    def create_folder(self, folder: str) -> None:
        """
        Create folder on destination

        :raises:
            FileExistsError: when a folder already exist
        """
        folder_path = os.path.join(self._destination, folder)

        # Security check to block create folder on source
        if folder_path.startswith(self._source):
            raise BlockCreateFolderOnSource

        try:
            os.mkdir(folder_path)
        except (FileExistsError, FileNotFoundError) as err:
            logging.warning(
                "Error on create folder %s - %s.", err.filename, err.strerror
            )
            raise FolderAlreadyExist from err


    def _check_root_folders(self):
        """
        Check if both source and destination folders exist
        """
        if not os.path.isdir(self._source):
            raise SourcePathDoesNotExist

        if not os.path.isdir(self._destination):
            raise DestinationPathDoesNotExist

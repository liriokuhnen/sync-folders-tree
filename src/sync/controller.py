"""
Module that will control sync actions interacting with DiffTree and FileSystemCommands
"""

import os
from logging import Logger

from diff_folders.walk_tree import DiffTree
from file_system.commands import FileSystemCommands
from settings import DiffActionsEnum, FolderSettingsDataClass
from utils.memory_usage import memory_usage
from utils.timeit import timeit


class SyncController:  #pylint: disable=too-few-public-methods
    """Class to execute sync operations between source and destination"""

    def __init__(
        self, folder_settings: FolderSettingsDataClass, logger: Logger
    ) -> None:
        """
        Initialize DiffTree and FileSystemCommands modules with source and destination
        settings
        """
        self._diff_client = DiffTree(folder_settings=folder_settings)
        self._commands_client = FileSystemCommands(
            folder_settings=folder_settings, logger=logger
        )
        self._logger = logger
        self._map_actions = {
            DiffActionsEnum.CREATE_FILE: self._commands_client.create_file,
            DiffActionsEnum.UPDATE_FILE: self._commands_client.create_file,
            DiffActionsEnum.DELETE_FILE: self._commands_client.delete_file,
            DiffActionsEnum.CREATE_FOLDER: self._commands_client.create_folder,
            DiffActionsEnum.DELETE_FOLDER: self._commands_client.delete_folder,
        }

    @memory_usage
    @timeit
    def execute(self):
        """Start diff scan in source to execute sync actions into destination"""

        for diff in self._diff_client.get_actions():
            callable_action = self._map_actions.get(diff.action)

            if callable_action:
                callable_action(path=os.path.join(diff.common_root, diff.name))
                self._logger.info(f"sync action {diff.action.value} complete")

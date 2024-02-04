"""Settings of the project"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


@dataclass
class FolderSettingsDataClass:
    """Data structure of folder settings"""
    source: Path
    destination: Path


class DiffActionsEnum(Enum):
    """Outcome actions from a diff between source and destination"""
    CREATE_FILE = "create_file"
    UPDATE_FILE = "update_file"
    DELETE_FILE = "delete_file"
    CREATE_FOLDER = "create_folder"
    DELETE_FOLDER = "delete_folder"

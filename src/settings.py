"""Settings of the project"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class FolderSettingsDataClass:
    """Data structure of folder settings"""
    source: Path
    destination: Path

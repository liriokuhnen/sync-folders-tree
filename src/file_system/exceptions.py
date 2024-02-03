"""Module with custom exceptions of file system commands"""

class FileSystemBaseException(Exception):
    """Base class exception of file operation""" 


class SourcePathDoesNotExist(FileSystemBaseException):
    """Raise when source path does not exist"""


class DestinationPathDoesNotExist(FileSystemBaseException):
    """Raise when destination path does not exist"""


class SourceAndDestinationAreEquals(FileSystemBaseException):
    """Raise when source and destination have the same values"""


class FileOrDirectoryNotFound(FileSystemBaseException):
    """
    Raise when source file or destination directory does not exist in a copy operation
    """


class FileNotFoundOnDelete(FileSystemBaseException):
    """Raise when a file is not found on delete"""


class ErrorOnDelete(FileSystemBaseException):
    """Raise when a error happen on delete file"""


class BlockDeleteOnSource(FileSystemBaseException):
    """Raise when a delete operation on soure is blocked"""


class ErrorOnCreateFolder(FileSystemBaseException):
    """Raise when try to create a folder that already exist or
    when some folder in the path does not exist"""


class BlockCreateFolderOnSource(FileSystemBaseException):
    """Raise when a creation folder is blocked on source"""


class FolderNotFoundOnDelete(FileSystemBaseException):
    """Raise when a folder is not found on delete"""


class BlockDeleteOfDestinationFolder(FileSystemBaseException):
    """Raise when a delete of root folder destination is blocked"""


class ErrorOnDeleteFolder(FileSystemBaseException):
    """Raise when a error happen on delete folder"""

"""
Start thread synchronization according with settings
"""

__author__ = "Lirio Kuhnen"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import threading
import time

from settings import FolderSettingsDataClass
from setup_logger import setup_logger
from sync.controller import SyncController


def main(args):
    """ Main entry point to start thread looping """
    settings = FolderSettingsDataClass(source=args.source, destination=args.destination)
    logger = setup_logger("sync_logger", args.log)

    sync_controller = SyncController(
        folder_settings=settings, logger=logger, sha256=args.sha256
    )

    while True:
        try:
            sync_controller.execute()
        except Exception as err:  #pylint: disable=broad-exception-caught
            print("Error on execution", err.__class__)

        print(f"interval sleep of {args.interval}")
        time.sleep(args.interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("source", help="Required source path", type=str)
    parser.add_argument("destination", help="Required destination path", type=str)
    parser.add_argument("interval", help="Required interval of sync in seconds", type=int)
    parser.add_argument("log", help="Required file log path", type=str)

    # Optional argument
    parser.add_argument("-s", "--sha256", action="store_true", default=False,
        help="diff files using sha256 hash strategy")

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {__version__})")

    sync_args = parser.parse_args()
    thread = threading.Thread(target=main, args=(sync_args, ))
    thread.start()

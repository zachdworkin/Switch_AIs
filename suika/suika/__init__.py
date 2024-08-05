# Description

from suika.core.watcher.screen import WindowCapture
import argparse
import logging
import datetime
import os
import path

logging.basicCoincif(
    level = logging.INFO,
    handlers = [],
    encoding = "utf-8",
    force = True
)
logger = logging.getLogger(__name__)

def setup_logging(output_root, quiet=False) -> None:
    """Setup a log directory structure for the application.

    Args:
        output_root (string): main directory to store log subdirectories
        quiet (bool, optional): Determines if handler should use stderr. Defaults to False.
    """
    
    log_path = os.path.join(output_root, "suika_logs", "logs")
    logfile_name = f"output{datetime.now().strftime('%Y%m%d%H%M%S')}.log"
    logfile_path = os.path.join(log_path, logfile_name)
    for handle in logger.handlers:
        logger.removeHandler(handle)

    # Add handler that goes to stderr
    if not quiet:
        logger.addHandler(logging.StreamHandler())

    os.makedirs(log_path, exist_ok=True)
    logger.addHandler(logging.FileHandler(logfile_path))


def get_args(args) -> argparse.Namespace:
    """
    Use argparse to get values of command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Run AI's based on emulator for suika game")
    parser.add_argument(
        "--app_name",
        type=str,
        help="Name of the application window to take screenshot",
        default="Ryujinx 1.1.1364"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Increase output verbosity"
    )

    return parser.parse_args(args)

# pylint: disable-next=missing-function-docstring
def cli_entry(args=None) -> int:
    parsed_args = get_args(args)
    WindowCapture().collect_screenshot(parsed_args.app_name)
    return 0
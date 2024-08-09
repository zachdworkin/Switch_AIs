"""Suika AI based on reinforcement learning
"""

import argparse
import logging
from datetime import datetime
import os
from PIL import Image

from suika.core.managers.reinforcement import ReinforcementLearning

logging.basicConfig(
    level=logging.INFO, handlers=[], encoding="utf-8", force=True
)
logger = logging.getLogger(__name__)


def setup_logger(output_root, quiet=False) -> None:
    """Setup a log directory structure for the application.

    Args:
        output_root (string): main directory to store log subdirectories
        quiet (bool, optional): Determines if handler should use stderr. Defaults to False.
    """

    log_path = os.path.join(output_root, "logs")
    logfile_name = f"output_{datetime.now().strftime('%Y%m%d%H%M%S')}.log"
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
        description="Run AI's based on emulator for suika game"
    )
    parser.add_argument(
        "--app_name",
        type=str,
        help="Name of the application window to take screenshot",
        default="Ryujinx 1.1.1",
    )
    parser.add_argument(
        "--output_root",
        type=str,
        help="Root directory to store logs and screenshots",
        default=os.environ["PWD"],
    )
    parser.add_argument(
        "--training_limit",
        type=int,
        help="Limit of training iterations to execute before stopping",
        default=1000,
    )
    parser.add_argument(
        "--quiet",
        type=bool,
        help="Use stderr for logging",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Increase output verbosity",
    )

    return parser.parse_args(args)


# pylint: disable-next=missing-function-docstring
def cli_entry(args=None) -> int:
    """main entry point for the application.

    Args:
        args (_type_, optional): Args to modify application. Defaults to None.

    Returns:
        int: error code
    """
    parsed_args = get_args(args)
    setup_logger(parsed_args.output_root, parsed_args.quiet)
    try:
        rfl = ReinforcementLearning(
            parsed_args.app_name,
            os.path.join(parsed_args.output_root, "logs"),
            parsed_args.training_limit,
        )
        rfl.train()
    except (
        FileNotFoundError,
        Image.UnidentifiedImageError,
        ValueError,
        TypeError,
    ) as err:
        logger.error("Training failed")
        logger.error(err)
        return -1

    return 0

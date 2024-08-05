# Description

from suika.core.watcher.screen import WindowCapture
import argparse

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
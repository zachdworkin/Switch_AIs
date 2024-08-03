# Description

from suika.core.watcher.screen import WindowCapture

# pylint: disable-next=missing-function-docstring
def cli_entry(args=None) -> int:
    WindowCapture().collect_screenshot("Ryujinx 1.1.1364")
    return 0
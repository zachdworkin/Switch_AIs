# Description

from suika.core.watcher.screen import WindowCapture

# pylint: disable-next=missing-function-docstring
def cli_entry(args=None) -> int:
    wc = WindowCapture()
    wc.take_screenshot()
    wc.save_screenshot("screenshot.png")
    wc.close_screenshot()
    return 0
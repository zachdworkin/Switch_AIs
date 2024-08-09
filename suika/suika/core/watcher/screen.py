# pylint: disable=missing-module-docstring
import logging
from PIL import ImageGrab
import pygetwindow as gw  # type: ignore

logger = logging.getLogger(__name__)


class WindowCapture:
    """
    Screenshot a window based on application name and specified offests for the application.
    """

    def __init__(self, app_name):
        """Offests based on application type"""
        self.offsets = {
            "none": {"left": 0, "top": 0, "right": 0, "bottom": 0},
            "ryujinx": {"left": 0, "top": 0, "right": 0, "bottom": 0},
        }
        self.app_name = self.__find_full_app_name(app_name)

    def __find_full_app_name(self, app_name):
        """
        Return application screen based on app_name.
        If no application screen is found, return None.

        Args:
            app_name (str): name of application window

        Returns:
            fd: screen fd
        """
        screens = gw.getAllTitles()
        for screen in screens:
            if app_name in screen:
                self.app_name = screen
                return screen

        return None

    def get_application_window(self):
        """Find the application window based on self.app_name.

        Returns:
            window: window object found based on app_name
        """
        if self.app_name is None:
            return None

        return gw.getWindowsWithTitle(self.app_name)[0]

    def save_screenshot(self, screenshot, path):
        """Save a screenshot based on path to it

        Args:
            screenshot (obj): screenshot to be saved
            path (str): location to save screenshot
        """
        if path is None or screenshot is None:
            return -1

        screenshot.save(path)
        return 0

    def take_screenshot(self, window, offset, path):
        """Take a screenshot of the window."""
        if offset not in self.offsets:
            offset = "none"

        screenshot = ImageGrab.grab(
            bbox=(
                window.left + self.offsets[offset]["left"],
                window.top + self.offsets[offset]["top"],
                window.right + self.offsets[offset]["right"],
                window.bottom + self.offsets[offset]["bottom"],
            )
        )

        self.save_screenshot(screenshot, path)

    def collect_screenshot(self, path):
        """collect a screenshot based on application name

        Args:
            app_name (str): name of application to screenshot
        """
        window = self.get_application_window()
        if window is None:
            msg = "Window not found %s", self.app_name
            logger.error(msg)
            raise FileNotFoundError(msg)

        self.take_screenshot(window, "ryujinx", path)

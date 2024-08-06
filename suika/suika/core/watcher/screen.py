# pylint: disable=missing-module-docstring
from PIL import ImageGrab
import pygetwindow as gw  # type: ignore


class WindowCapture:
    """
    Screenshot a window based on application name and specified offests for the application.
    """

    def __init__(self, output_root):
        """Offests based on application type"""
        self.output_root = output_root
        self.offsets = {
            "none": {"left": 0, "top": 0, "right": 0, "bottom": 0},
            "ryujinx": {"left": 100, "top": 125, "right": 200, "bottom": 0},
        }
        self.screenshot = None

    def find_app_name(self, app_name):
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
                return screen

        return None

    def get_application_window(self, app_name):
        """Find the application window based on app_name.

        Args:
            app_name (str): name of application window

        Returns:
            window: window object found based on app_name
        """
        if app_name is None:
            return None

        return gw.getWindowsWithTitle(app_name)[0]

    def take_screenshot(self, window, offset):
        """Take a screenshot of the window."""
        if offset not in self.offsets:
            offset = "none"

        self.screenshot = ImageGrab.grab(
            bbox=(
                window.left + self.offsets[offset]["left"],
                window.top + self.offsets[offset]["top"],
                window.right + self.offsets[offset]["right"],
                window.bottom + self.offsets[offset]["bottom"],
            )
        )

    def save_screenshot(self, path):
        """Save a screenshot based on path to it

        Args:
            screenshot (obj): screenshot to be saved
            path (str): location to save screenshot
        """
        if path is None or self.screenshot is None:
            return -1

        self.screenshot.save(path)
        return 0

    def close_screenshot(self):
        """close a screenshot fd

        Args:
            screenshot (obj): screenshot fd object
        """
        if self.screenshot is not None:
            self.screenshot.close()

    def collect_screenshot(self, app_name):
        """collect a screenshot based on application name

        Args:
            app_name (str): name of application to screenshot
        """
        window = self.get_application_window(self.find_app_name(app_name))
        if window is None:
            print("Window not found")
            return

        self.take_screenshot(window, app_name)
        self.save_screenshot(f"{self.output_root}/screenshot.png")
        self.close_screenshot()

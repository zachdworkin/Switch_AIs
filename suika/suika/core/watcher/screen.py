from PIL import ImageGrab
import pygetwindow as gw
import os

class WindowCapture:

    def __init__(self):
        self.ryujinx_offsets = {
            "left": 100,
            "top": 125,
            "right": 200,
            "bottom": 0
        }
        pass

    def find_app_name(self, app_name):
        screens = gw.getAllTitles()
        for screen in screens:
            if app_name in screen:
                return screen

        return None

    def get_application_window(self, app_name):
        if app_name is None:
            return None
        return gw.getWindowsWithTitle(app_name)[0]

    def take_screenshot(self, window):
        return ImageGrab.grab(bbox=(
                    window.left + self.ryujinx_offsets["left"],
                    window.top + self.ryujinx_offsets["top"],
                    window.right + self.ryujinx_offsets["right"],
                    window.bottom + self.ryujinx_offsets["bottom"]
                )
        )

    def save_screenshot(self, screenshot, path):
        screenshot.save(path)

    def close_screenshot(self, screenshot):
        screenshot.close()

    def collect_screenshot(self, app_name):
        window = self.get_application_window(self.find_app_name(app_name))
        if window is None:
            print("Window not found")
            return

        screenshot = self.take_screenshot(window)
        self.save_screenshot(screenshot, f"{os.environ['PWD']}/screenshot.png")
        self.close_screenshot(screenshot)


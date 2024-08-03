from PIL import ImageGrab

class WindowCapture:

    def __init__(self):
        self.screenshot = None
        pass

    def take_screenshot(self):
        self.screenshot = ImageGrab.grab()

    def save_screenshot(self, path):
        self.screenshot.save("screenshot.png")

    def close_screenshot(self):
        self.screenshot.close()

    # region
    # Capture a specific region (left, top, right, bottom)
    # screenshot = ImageGrab.grab(bbox=(100, 100, 500, 500))

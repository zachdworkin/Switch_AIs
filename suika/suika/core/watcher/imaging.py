# pylint: disable=missing-module-docstring
import os
from pathlib import Path
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


class Imaging:
    """Imaging manager for capturing and processing images."""

    def __init__(self, screenshot_path: str):
        self.screenshot_path: str = screenshot_path
        self.black_and_white: Image.Image = Image.Image()
        self.screenshot: np.ndarray = np.ndarray(0)
        self.bw_data: np.ndarray = np.ndarray(0)

    def black_and_whitify(self):
        """Convert the image to black and white."""
        try:
            img = Image.open(self.screenshot_path)
            img.convert("l")
        except FileNotFoundError:
            return None

        return img

    def save_black_and_white(self, path):
        """Save the black and white image."""
        # TODO determine what path should be
        try:
            self.black_and_white.save(path)
        except FileNotFoundError:
            self.close()

    def close(self):
        """Close the image."""
        self.black_and_white.close()

    def analyze(self):
        """Analyze the image."""
        try:
            self.black_and_white = self.black_and_whitify()
            self.screenshot = plt.imread(self.screenshot_path)
            self.bw_data = np.asarray(self.black_and_white)
            self.save_black_and_white(
                os.path.join(
                    os.path.dirname(self.screenshot_path),
                    Path(self.screenshot_path).stem + "_bw.png",
                )
            )
        except FileNotFoundError:
            self.black_and_white.close()
        finally:
            self.black_and_white.close()

        return 0

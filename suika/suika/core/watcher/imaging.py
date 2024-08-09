# pylint: disable=missing-module-docstring
import os
import shutil
import logging
from enum import Enum
from PIL import Image

from suika.core.watcher.screen import WindowCapture

logger = logging.getLogger(__name__)


class ImagingType(Enum):
    """Enum for Imaging types.

    Attributes
    ----------
    COLOR : const int
        Color image type
    BW : const int
        Black and white image type
    UNKN : const int
        Unknown Image type
    """

    COLOR = "color"
    BW = "bw"
    UNKN = "UNKN"

    def __str__(self):
        return self.value


class Imaging:
    """Imaging manager for capturing and processing images."""

    def __init__(self, app_name, output_root):
        self.wc = WindowCapture(app_name)
        self.output_root = output_root
        self.history: dict = {
            str(ImagingType.COLOR): [],
            str(ImagingType.BW): [],
            str(ImagingType.UNKN): [],
        }
        self.__create_paths()
        self.path_prefixes = {
            str(ImagingType.COLOR): os.path.join(
                self.output_root,
                str(ImagingType.COLOR),
            ),
            str(ImagingType.BW): os.path.join(
                self.output_root,
                str(ImagingType.BW),
            ),
            str(ImagingType.UNKN): os.path.join(
                self.output_root,
                str(ImagingType.UNKN),
            ),
        }

    def __create_paths(self):
        """Create upload paths for the images."""
        for img_type in ImagingType:
            path = os.path.join(self.output_root, str(img_type))
            if os.path.exists(path):
                shutil.rmtree(path)

            try:
                os.makedirs(
                    path,
                    exist_ok=False,
                )
            except OSError as err:
                logger.error("Could not create upload paths.")
                raise err from err

    def black_and_whitify(self, screenshot, path):
        """Convert the image to black and white."""
        bw_img = None
        try:
            with Image.open(screenshot) as color_img:
                copy = color_img.copy()
                bw_img = copy.convert("L")
        except (
            FileNotFoundError,
            Image.UnidentifiedImageError,
            ValueError,
            TypeError,
        ) as err:
            logger.error("Could not convert image to black and white.")
            raise err from err

        self.wc.save_screenshot(bw_img, path)

    def is_game_over(self):
        """Check if the game is over."""
        return False

    def analyze_next_screenshot(self, idx):
        """Analyze the image."""
        next_color = os.path.join(
            self.path_prefixes[str(ImagingType.COLOR)],
            f"{idx}.png",
        )
        next_bw = os.path.join(
            self.path_prefixes[str(ImagingType.BW)],
            f"{idx}.png",
        )
        try:
            self.wc.collect_screenshot(next_color)
        except FileNotFoundError as err:
            logger.error("Could not collect screenshot.")
            logger.error(err)
            raise err from err

        self.history[str(ImagingType.COLOR)].append(next_color)
        try:
            self.black_and_whitify(next_color, next_bw)
        except (
            FileNotFoundError,
            Image.UnidentifiedImageError,
            ValueError,
            TypeError,
        ) as err:
            logger.error("Could not convert image to black and white.")
            raise err from err

        self.history[str(ImagingType.BW)].append(next_bw)
        return 0

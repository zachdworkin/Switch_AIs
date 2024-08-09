# pylint: disable=missing-module-docstring
import logging
from PIL import Image

from suika.core.watcher.imaging import Imaging

logger = logging.getLogger(__name__)


class ReinforcementLearning:
    """Reinforcement learning manager for training the model."""

    def __init__(self, app_name, output_root, training_limit):
        self.app_name = app_name
        self.output_root = output_root
        self.training_limit = training_limit
        self.imager = Imaging(self.app_name, self.output_root)
        self.idx = 0

    def train(self):
        """
        Main loop for training the model.
        Train the model using reinforcement learning.
        """
        while not self.imager.is_game_over() and self.idx < self.training_limit:
            try:
                self.imager.analyze_next_screenshot(self.idx)
            except (
                FileNotFoundError,
                Image.UnidentifiedImageError,
                ValueError,
                TypeError,
            ) as err:
                logger.error("Train failed")
                raise err from err

            self.idx += 1
            # TODO determine next input
            # TODO send input to emulator

        return 0

    def test(self):
        """empty method to satisfy pylint"""
        # TODO remove later

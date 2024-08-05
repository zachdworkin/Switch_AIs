# Empty file description
from suika.core.watcher.screen import WindowCapture

class ReinforcementLearning:
    def __init__(self, app_name):
        self.app_name = app_name
        self.wc = WindowCapture(app_name)

    def train(self):
        """
        Main loop for training the model.
        Train the model using reinforcement learning.
        """
        while self.wc.find_app_name(self.app_name) is not None:
            self.wc.collect_screenshot(self.app_name)
            # TODO determine next input
            # TODO send input to emulator
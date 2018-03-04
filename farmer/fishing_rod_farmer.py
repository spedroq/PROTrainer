import time
from farmer.farmer import Farmer


class FishingRodFarmer(Farmer):
    """
    Class that defines WaterFarmer derived from Farmer.
    Used to farm XP in the water using the fishing rod.
    """

    TURN = 0
    WRAP_AROUND = 3

    def farm(self):
        """
        Implement the abstract function farm() with the specific implementation
        to farm with a fishing rod in the water.
        """
        self.press_1()
        screenshot_filepath = self.radon.save_screenshot()
        screenshot_text = self.radon.read_text_from_image(screenshot_filepath)
        if 'no PP left' in screenshot_text:
            print('NO PP')


        time.sleep(1)
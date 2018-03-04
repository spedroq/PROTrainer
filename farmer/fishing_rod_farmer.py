import time
from farmer.farmer import Farmer



class FishingRodFarmer(Farmer):
    """
    Class that defines WaterFarmer derived from Farmer.
    Used to farm XP in the water using the fishing rod.
    """
    def farm(self):
        """
        Implement the abstract function farm() with the specific implementation
        to farm with a fishing rod in the water.
        """
        self.press_1()
        print(self.radon.save_screenshot())
        time.sleep(1)

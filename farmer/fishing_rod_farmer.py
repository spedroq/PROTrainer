from farmer.farmer import Farmer
from move_set.move_set import PROTrainerMoveSequence


class FishingRodFarmer(Farmer):
    """
    Class that defines WaterFarmer derived from Farmer.
    Used to farm XP in the water using the fishing rod.
    """

    TURN = 0
    WRAP_AROUND = 3

    # Define moves
    default_move_set = PROTrainerMoveSequence(["1|1"])
    poke_center_move_set = PROTrainerMoveSequence(["4|25", "w|25", "1, ,s|25", "s|25"])

    # Init farm move sequence
    farm_move_sequence = default_move_set

    def farm(self):
        """
        Implement the abstract function farm() with the specific implementation
        to farm with a fishing rod in the water.
        """
        # Press 1 forever
        self.farm_move_sequence = self.default_move_set

    """
    def handle_radon_results(self, radon_results: str):
        self.farm_move_sequence = self.default_move_set
        if "no PP left" in radon_results:
            self.farm_move_sequence = self.poke_center_move_set
    """



from farmer.farmer import Farmer
from move_set.move_set import PROTrainerMoveSequence


class SurfFarmer(Farmer):
    """
    Class that defines SurfFarmer derived from Farmer.
    Used to farm XP surfing in the water.
    """

    # Define moves
    default_move_set = PROTrainerMoveSequence(["s,1, ,mouse_left%1071%580|12", "w,1|4"])
    poke_center_move_set = PROTrainerMoveSequence(["4,w|30", "4,w, |15", "1, ,s|15",
                                                   "1, ,s,mouse_left%1071%580|15"])

    # Init farm move sequence
    farm_move_sequence = default_move_set

    def farm(self):
        """
        Implement the abstract function farm() with the specific implementation
        to farm surfing in the water.
        """

        if self.COUNT > self.TIMEOUT:
            # Speak to Nurse Joy
            print(self.poke_center_move_set)
            self.farm_move_sequence = self.poke_center_move_set
            self.COUNT = 0
            print(self.default_move_set)
        else:
            # Press 1 forever
            self.farm_move_sequence = self.default_move_set




from farmer.farmer import Farmer
from move_set.move_set import PROTrainerMoveSequence


class GhostTowerFarmer(Farmer):
    """
    Class that defines GhostTowerFarmer derived from Farmer.
    Used to farm XP in the in the ghost tower.
    """

    # Define moves
    default_move_set = PROTrainerMoveSequence(["s,1|10", "w,1|10"])
    poke_center_move_set = PROTrainerMoveSequence(["4,w|30", "4,d, |15", "1, ,a|15", "a|10"])

    # Init farm move sequence
    farm_move_sequence = default_move_set

    def farm(self):
        """
        Implement the abstract function farm() with the specific implementation
        to farm in the ghost tower.
        """
        if 'no PP' in self.radon_text:
            # Speak to Nurse Joy Sequence
            self.farm_move_sequence = self.poke_center_move_set
        else:
            # Farm Sequence
            self.farm_move_sequence = self.default_move_set




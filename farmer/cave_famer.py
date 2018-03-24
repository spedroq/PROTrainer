from farmer.farmer import Farmer
from move_set.move_set import PROTrainerMoveSequence


class CaveFarmer(Farmer):
    """
    Class that defines CaveFarmer derived from Farmer.
    Used to farm XP in the in the cave.
    """

    # Define moves
    default_move_set = PROTrainerMoveSequence(["s,1|10", "w,1|10"])
    poke_center_move_set = PROTrainerMoveSequence(["4,s|30", "4,s, |15", "1, ,w|15"])

    # Init farm move sequence
    farm_move_sequence = default_move_set

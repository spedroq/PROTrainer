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
    default_move_set = PROTrainerMoveSequence([" , , , ,1|1"],1)
    #default_move_set = PROTrainerMoveSequence(["a,1|6", "d,1|6"])
    poke_center_move_set = PROTrainerMoveSequence(["4|25", "w,4|25", "1, ,s|25", "s|25"])

    # Init farm move sequence
    farm_move_sequence = default_move_set


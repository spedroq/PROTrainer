from farmer.farmer import Farmer
from move_set.move_set import PROTrainerMoveSequence, PROTrainerMove


class FishingRodFarmer(Farmer):
    """
    Class that defines WaterFarmer derived from Farmer.
    Used to farm XP in the water using the fishing rod.
    """

    TURN = 0
    WRAP_AROUND = 3

    # Define moves
    default_move_set = PROTrainerMoveSequence([PROTrainerMove(["a", "1"], 6),
                                               PROTrainerMove(["d", "1"], 6)])
    poke_center_move_set = PROTrainerMoveSequence([PROTrainerMove(["4"], 25),
                                                   PROTrainerMove(["w"], 25),
                                                   PROTrainerMove(["1", " ", "s"], 25),
                                                   PROTrainerMove(["s"], 25)])

    # Init farm move sequence
    farm_move_sequence = default_move_set


from farmer.farmer import Farmer
from move_set.move_set import PROTrainerMoveSequence, PROTrainerMove


class GhostTowerFarmer(Farmer):
    """
    Class that defines GhostTowerFarmer derived from Farmer.
    Used to farm XP in the in the ghost tower.
    """

    # Define moves
    default_move_set = PROTrainerMoveSequence([PROTrainerMove(["s", "1"], 10), PROTrainerMove(["w", "1"], 10)])
    poke_center_move_set = PROTrainerMoveSequence([PROTrainerMove(["4", "w"], 30),
                                                   PROTrainerMove(["4", "d"], 15),
                                                   PROTrainerMove(["1", " ", "a"], 15),
                                                   PROTrainerMove(["a"], 10)])

    # Init farm move sequence
    farm_move_sequence = default_move_set


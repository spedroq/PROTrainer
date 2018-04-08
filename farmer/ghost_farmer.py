from farmer.farmer import Farmer
from move_set.move_set import PROTrainerMoveSequence, PROTrainerMove


class GhostTowerFarmer(Farmer):
    """
    Class that defines GhostTowerFarmer derived from Farmer.
    Used to farm XP in the in the ghost tower.
    """

    # Define moves
    default_move_set = PROTrainerMoveSequence([PROTrainerMove(["w"], 15, timeout=0.05, random_deviation=0.1),
                                               PROTrainerMove(["s"], 15, timeout=0.05, random_deviation=0.1),
                                               PROTrainerMove(["w"], 15, timeout=0.05, random_deviation=0.1),
                                               PROTrainerMove(["s"], 15, timeout=0.05, random_deviation=0.1),
                                               PROTrainerMove(["1"], 1, timeout=1, random_deviation=1)])
    poke_center_move_set = PROTrainerMoveSequence([PROTrainerMove(["4", "w"], 45, timeout=0.05, random_deviation=0.1),
                                                   PROTrainerMove(["4", "d"], 25, timeout=0.05, random_deviation=0.1),
                                                   PROTrainerMove(["1", " ", "a"], 25, timeout=0.05, random_deviation=0.1),
                                                   PROTrainerMove(["a"], 25, timeout=0.05, random_deviation=0.1)])

    # Init farm move sequence
    farm_move_sequence = default_move_set
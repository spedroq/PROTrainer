from farmer.farmer import Farmer
from move_set.move_set import PROTrainerMoveSequence, PROTrainerMove


class CaveFarmer(Farmer):
    """
    Class that defines CaveFarmer derived from Farmer.
    Used to farm XP in the in the cave.
    """

    # Define moves
    default_move_set = PROTrainerMoveSequence([PROTrainerMove(["w"], 15, timeout=0.05, random_deviation=0.1),
                                               PROTrainerMove(["s"], 15, timeout=0.05, random_deviation=0.1),
                                               PROTrainerMove(["w"], 15, timeout=0.05, random_deviation=0.1),
                                               PROTrainerMove(["s"], 15, timeout=0.05, random_deviation=0.1),
                                               PROTrainerMove(["1"], 1, timeout=0.6, random_deviation=0.5)])
    poke_center_move_set = PROTrainerMoveSequence([PROTrainerMove(["4", "s"], 45, timeout=0.05, random_deviation=0.1),
                                                   PROTrainerMove(["1", " ", "w"], 25, timeout=0.05, random_deviation=0.1),
                                                   PROTrainerMove(["w"], 25, timeout=0.05, random_deviation=0.1)])

    # Init farm move sequence
    farm_move_sequence = default_move_set

from farmer.farmer import Farmer
from move_set.move_set import PROTrainerMoveSequence, PROTrainerMove


class CaveFarmer(Farmer):
    """
    Class that defines CaveFarmer derived from Farmer.
    Used to farm XP in the in the cave.
    """

    # Define moves
    default_move_set = PROTrainerMoveSequence([PROTrainerMove(["s", "1"], 10),
                                               PROTrainerMove(["w", "1"], 10)])
    poke_center_move_set = PROTrainerMoveSequence([PROTrainerMove(["4", "s"], 30),
                                                   PROTrainerMove(["1", " ", "w"], 15)])

    # Init farm move sequence
    farm_move_sequence = default_move_set

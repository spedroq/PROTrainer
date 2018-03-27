from farmer.farmer import Farmer
from move_set.move_set import PROTrainerMoveSequence, PROTrainerMove


class CeruleanBushFarmer(Farmer):
    """
    Class that defines CeruleanBushFarmer derived from Farmer.
    Used to farm XP in Cerulean bushes.
    """

    TURN = 0
    WRAP_AROUND = 3

    # Define moves
    default_move_set = PROTrainerMoveSequence([PROTrainerMove(["w", "1"], 10),
                                               PROTrainerMove(["s", "1"], 10)])
    poke_center_move_set = PROTrainerMoveSequence([
        # Go to PokeCenter
        PROTrainerMove(["4", "s"], 25, 1.5),
        PROTrainerMove(["4", "d"], 25, 1.5),
        PROTrainerMove(["w"], 5, 1.5),
        PROTrainerMove(["d"], 10, 1.5),
        PROTrainerMove(["w"], 10, 1.5),
        PROTrainerMove(["d"], 14, 1.5),
        PROTrainerMove(["s"], 13, 1.5),
        PROTrainerMove(["d"], 17, 1.5),
        # Talk to Nurse Joy
        PROTrainerMove(["w", " "], 20, 0.75),
        PROTrainerMove(["1", "s", " "], 3, 1.5),
        # Walk out of PokeCenter
        PROTrainerMove(["s"], 7, 1.5),
        PROTrainerMove(["a"], 20, 0.75),
        PROTrainerMove(["w"], 20, 0.75),
        PROTrainerMove(["a"], 20, 0.75),
        PROTrainerMove(["s"], 20, 0.75),
        # Back to the bush area
        PROTrainerMove(["1", "a"], 20, 1.5)
    ])

    # Init farm move sequence
    farm_move_sequence = default_move_set


from farmer.farmer import Farmer
from move_set.move_set import PROTrainerMoveSequence, PROTrainerMove


class VictoryRoadFarmer(Farmer):
    """
    Class that defines VictoryRoadFarmer derived from Farmer.
    Used to farm XP in the in the high level pokemon cave.
    """

    # Define moves
    default_move_set = PROTrainerMoveSequence([PROTrainerMove(["a", "1"], 10),
                                               PROTrainerMove(["d", "1"], 10)])
    poke_center_move_set = PROTrainerMoveSequence([
        # Get out of the cave
        PROTrainerMove(["d", "4"], 20, 0.75),
        PROTrainerMove(["w", "4"], 20, 0.75),
        # Walk out
        PROTrainerMove(["a", "4"], 1, 0.75),
        PROTrainerMove(["w", "4"], 1, 0.75),
        PROTrainerMove(["a", "4"], 1, 0.75),
        PROTrainerMove(["w", "4"], 1, 0.75),
        PROTrainerMove(["a", "4"], 1, 0.75),
        PROTrainerMove(["w", "4"], 1, 0.75),
        # Jank out of the cave
        PROTrainerMove(["d", "4"], 1, 0.75),
        PROTrainerMove(["w", "4"], 1, 0.75),
        PROTrainerMove(["d", "4"], 1, 0.75),
        PROTrainerMove(["w"], 1, 0.75),
        PROTrainerMove(["d"], 6, 0.75),
        # To Pokecenter
        PROTrainerMove(["w"], 20, 0.5),
        PROTrainerMove(["d"], 9, 0.5),
        PROTrainerMove(["w"], 2, 0.5),
        # In Pokecenter
        PROTrainerMove(["w"], 4, 0.75),
        PROTrainerMove(["a"], 6, 0.75),
        # Nurse Joy
        PROTrainerMove(["w", " "], 10, 0.5),
        PROTrainerMove(["1", " ", "s"], 10, 0.75),
        # Get out of the Pokecenter
        PROTrainerMove(["d"], 10, 0.5),
        PROTrainerMove(["s"], 10, 0.5),
        PROTrainerMove(["a"], 12, 0.5),
        # Into the cave
        PROTrainerMove(["s", "1"], 20, 0.75),
        PROTrainerMove(["s", "1"], 20, 0.75)
    ])

    # Init farm move sequence
    farm_move_sequence = default_move_set


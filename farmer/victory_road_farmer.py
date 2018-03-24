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
        PROTrainerMove(["d", "4"], 20),
        PROTrainerMove(["w", "4"], 20),
        # Walk out
        PROTrainerMove(["a", "4"], 1),
        PROTrainerMove(["w", "4"], 1),
        PROTrainerMove(["a", "4"], 1),
        PROTrainerMove(["w", "4"], 1),
        PROTrainerMove(["a", "4"], 1),
        PROTrainerMove(["w", "4"], 1),
        # Jank out of the cave
        PROTrainerMove(["d", "4"], 1),
        PROTrainerMove(["w", "4"], 1),
        PROTrainerMove(["d", "4"], 1),
        PROTrainerMove(["w"], 1),
        PROTrainerMove(["d"], 6),
        # To Pokecenter
        PROTrainerMove(["w"], 20),
        PROTrainerMove(["d"], 9),
        PROTrainerMove(["w"], 2),
        # In Pokecenter
        PROTrainerMove(["w"], 4),
        PROTrainerMove(["a"], 6),
        # Nurse Joy
        PROTrainerMove(["w", " "], 10),
        PROTrainerMove(["1", " ", "s"], 10),
        # Get out of the Pokecenter
        PROTrainerMove(["d"], 10),
        PROTrainerMove(["s"], 10),
        PROTrainerMove(["a"], 12),
        # Into the cave
        PROTrainerMove(["s", "1"], 20),
        PROTrainerMove(["s", "1"], 20)
    ])

    # Init farm move sequence
    farm_move_sequence = default_move_set


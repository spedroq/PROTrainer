from farmer.farmer import Farmer
from move_set.move_set import PROTrainerMoveSequence, PROTrainerMove


class VictoryRoadFarmer(Farmer):
    """
    Class that defines VictoryRoadFarmer derived from Farmer.
    Used to farm XP in the in the high level pokemon cave.
    """

    # Define moves
    default_move_set = PROTrainerMoveSequence([PROTrainerMove(["w"], 15, timeout=0.05, random_deviation=0.1),
                                               PROTrainerMove(["s"], 15, timeout=0.05, random_deviation=0.1),
                                               PROTrainerMove(["w"], 15, timeout=0.05, random_deviation=0.1),
                                               PROTrainerMove(["s"], 15, timeout=0.05, random_deviation=0.1),
                                               PROTrainerMove(["1"], 1, timeout=4, random_deviation=2)])
    """
    poke_center_move_set = PROTrainerMoveSequence([
        # Get out of the cave
        PROTrainerMove(["d", "4"], 20, 1),
        PROTrainerMove(["w", "4"], 20, 1),
        # Walk out
        PROTrainerMove(["a", "4"], 1, 1),
        PROTrainerMove(["w", "4"], 1, 1),
        PROTrainerMove(["a", "4"], 1, 1),
        PROTrainerMove(["w", "4"], 1, 1),
        PROTrainerMove(["a", "4"], 1, 1),
        PROTrainerMove(["w", "4"], 1, 1),
        # Jank out of the cave
        PROTrainerMove(["d", "4"], 1, 1),
        PROTrainerMove(["w", "4"], 1, 1),
        PROTrainerMove(["d", "4"], 1, 1),
        PROTrainerMove(["w"], 1, 1),
        PROTrainerMove(["d"], 6, 1),
        # To Pokecenter
        PROTrainerMove(["w"], 20, 0.75),
        PROTrainerMove(["d"], 9, 1.5),
        PROTrainerMove(["w"], 2, 1.5),
        # In Pokecenter
        PROTrainerMove(["w"], 4, 1.5),
        PROTrainerMove(["a"], 6, 1.5),
        # Nurse Joy
        PROTrainerMove(["w", " "], 10, 0.75),
        PROTrainerMove(["1", " ", "s"], 10, 1),
        # Get out of the Pokecenter
        PROTrainerMove(["d"], 10, 0.75),
        PROTrainerMove(["s"], 10, 0.75),
        PROTrainerMove(["a"], 12, 0.75),
        # Into the cave
        PROTrainerMove(["s", "1"], 20, 1),
        PROTrainerMove(["s", "1"], 20, 1)
    ])
    """
    poke_center_move_set = PROTrainerMoveSequence([PROTrainerMove(["w"], 15, timeout=0.05, random_deviation=0.1),
                                                   PROTrainerMove(["s"], 15, timeout=0.05, random_deviation=0.1),
                                                   PROTrainerMove(["w"], 15, timeout=0.05, random_deviation=0.1),
                                                   PROTrainerMove(["s"], 15, timeout=0.05, random_deviation=0.1),
                                                   PROTrainerMove(["1"], 1, timeout=4, random_deviation=2)])

    # Init farm move sequence
    farm_move_sequence = default_move_set



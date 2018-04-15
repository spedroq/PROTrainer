from farmer.farmer import Farmer
from move_set.move_set import PROTrainerMoveSequence, PROTrainerMove


class PikachuFarmer(Farmer):
    """
    Class that defines CeladonFarmer derived from Farmer.
    Used to farm XP on the right of the city.
    """

    TURN = 0
    WRAP_AROUND = 3

    # Define moves
    default_move_set = PROTrainerMoveSequence([PROTrainerMove(["d"], 5, timeout=0.05, random_deviation=0.1),
                                               PROTrainerMove(["a"], 5, timeout=0.05, random_deviation=0.1),
                                               PROTrainerMove(["d"], 5, timeout=0.05, random_deviation=0.1),
                                               PROTrainerMove(["a"], 5, timeout=0.05, random_deviation=0.1),
                                               PROTrainerMove(["1"], 1, timeout=0.6, random_deviation=0.5)])

    poke_center_move_set = PROTrainerMoveSequence([
        # Go to the tunnel
        PROTrainerMove(["4", "a"], 25, timeout=0.25),
        PROTrainerMove(["4", "w"], 25, timeout=0.25),
        PROTrainerMove(["4", "d"], 1, timeout=0.5),
        PROTrainerMove(["w"], 2, timeout=0.5),
        PROTrainerMove(["nothing"], 1, timeout=2, random_deviation=2),
        # Through the tunnel
        PROTrainerMove(["w"], 9, timeout=0.5),
        PROTrainerMove(["nothing"], 1, timeout=2, random_deviation=2),
        # Up to the next transition screen
        PROTrainerMove(["w"], 13, timeout=0.5),
        PROTrainerMove(["d"], 12, timeout=0.5),
        PROTrainerMove(["w"], 9, timeout=0.5),
        PROTrainerMove(["d"], 5, timeout=0.5),
        PROTrainerMove(["w"], 19, timeout=0.5),
        PROTrainerMove(["nothing"], 1, timeout=2, random_deviation=2),
        # Through the town and into the pokecenter
        PROTrainerMove(["w"], 11, timeout=0.5),
        PROTrainerMove(["d"], 8, timeout=0.5),
        PROTrainerMove(["w"], 8, timeout=0.5),
        PROTrainerMove(["nothing"], 1, timeout=2, random_deviation=2),
        # In the pokecenter
        PROTrainerMove(["w"], 7, timeout=0.5),
        # Talk to nurse Joy
        PROTrainerMove(["w", " "], 10, timeout=0.5),
        PROTrainerMove(["1", " ", "s"], 5, timeout=0.5),
        PROTrainerMove(["s"], 5, timeout=0.5),
        # To the route
        PROTrainerMove(["s"], 8, timeout=0.5),
        PROTrainerMove(["a"], 9, timeout=0.5),
        PROTrainerMove(["s"], 11, timeout=0.5),
        PROTrainerMove(["nothing"], 1, timeout=2, random_deviation=2),
        # Through the route to the tunnel
        PROTrainerMove(["s"], 18, timeout=0.5),
        PROTrainerMove(["a"], 4, timeout=0.5),
        PROTrainerMove(["s"], 9, timeout=0.5),
        PROTrainerMove(["a"], 12, timeout=0.5),
        PROTrainerMove(["s"], 15, timeout=0.5),
        PROTrainerMove(["nothing"], 1, timeout=2, random_deviation=2),
        # Through the tunnel
        PROTrainerMove(["s"], 9, timeout=0.5),
        PROTrainerMove(["nothing"], 1, timeout=2, random_deviation=2),
        # Back to farming spot
    ])

    # Init farm move sequence
    #farm_move_sequence = default_move_set

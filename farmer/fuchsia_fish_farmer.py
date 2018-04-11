from farmer.farmer import Farmer
from move_set.move_set import PROTrainerMoveSequence, PROTrainerMove


class FuchsiaFishFarmer(Farmer):
    """
    Class that defines CeladonFarmer derived from Farmer.
    Used to farm XP on the right of the city.
    """

    TURN = 0
    WRAP_AROUND = 3

    # Define moves
    default_move_set = PROTrainerMoveSequence([

        # Farm
        PROTrainerMove(["1"], 10, timeout=.75, random_deviation=0.5)

    ])

    poke_center_move_set = PROTrainerMoveSequence([

        # No PP, bail
        PROTrainerMove(["4"], 30, timeout=0.1),
        # Up to pokecenter
        PROTrainerMove(["w"], 110, timeout=0.10),
        # Right to the pokemon center down one to match it
        PROTrainerMove(["d"], 4, timeout=0.4),
        PROTrainerMove(["s"], 1, timeout=0.4),
        PROTrainerMove(["d"], 4, timeout=0.4),
        # Move to nurse joy and interact
        PROTrainerMove(["w"], 35, timeout=0.10),

        PROTrainerMove(["1", " ", "s"], 15, timeout=0.10),
        PROTrainerMove(["s"], 3, timeout=0.10),
        PROTrainerMove(["nothing"], 1, timeout=1),
        # Bail from the pokemon center
        PROTrainerMove(["s"], 3, timeout=0.25),
        PROTrainerMove(["a"], 7, timeout=0.4),
        PROTrainerMove(["s"], 6, timeout=0.25),
        PROTrainerMove(["nothing"], 1, timeout=1),
        # Back to the left
        PROTrainerMove(["a"], 6, timeout=0.25),
        # Down to the water
        PROTrainerMove(["s"], 20, timeout=0.10),
        PROTrainerMove(["d"], 1, timeout=0.25),
        PROTrainerMove(["s"], 100, timeout=0.10),

    ])

    # Init farm move sequence
    #farm_move_sequence = default_move_set

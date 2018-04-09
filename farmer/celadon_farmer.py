from farmer.farmer import Farmer
from move_set.move_set import PROTrainerMoveSequence, PROTrainerMove


class CeladonFarmer(Farmer):
    """
    Class that defines CeladonFarmer derived from Farmer.
    Used to farm XP on the right of the city.
    """

    TURN = 0
    WRAP_AROUND = 3

    # Define moves
    default_move_set =  PROTrainerMoveSequence([
        
        #
        #   Farm
        PROTrainerMove(["d"], 15, timeout=0.05, random_deviation=0.1),
        PROTrainerMove(["a"], 15, timeout=0.05, random_deviation=0.1),
        PROTrainerMove(["1"], 10, timeout=.75, random_deviation=0.5)

    ])


    poke_center_move_set = PROTrainerMoveSequence([
        #
        #   No PP, bail, reach the left of the grass
        PROTrainerMove(["4", "a"], 50, timeout=0.1),
        #
        #   Down from the grass
        PROTrainerMove(["s"], 1, timeout=0.10),
        PROTrainerMove(["a", "s"], 2, timeout=0.15),
        #
        #   Left to near the pokemon center
        PROTrainerMove(["a"], 30, timeout=0.25),
        #
        #   Navigate into the pokemon center
        PROTrainerMove(["w"], 1, timeout=0.25),
        PROTrainerMove(["w"], 1, timeout=0.25),
        PROTrainerMove(["w"], 1, timeout=0.25),
        PROTrainerMove(["w"], 1, timeout=0.25),
        PROTrainerMove(["w"], 1, timeout=0.25),
        PROTrainerMove(["a"], 1, timeout=0.25),
        PROTrainerMove(["a"], 1, timeout=0.25),
        PROTrainerMove(["w"], 1, timeout=0.25),
        #
        #   Move to nurse joy and interact
        PROTrainerMove(["w"], 35, timeout=0.10),
        PROTrainerMove(["1", " ", "s"], 25, timeout=0.10),
        #
        #   Bail from the pokemon center
        PROTrainerMove(["s"], 8, timeout=0.10),
        #
        #   Back to the right 
        PROTrainerMove(["d"], 25, timeout=0.25),
        #
        #   Up to the wall
        PROTrainerMove(["w"], 1, timeout=0.25),
        PROTrainerMove(["w"], 1, timeout=0.25),
        PROTrainerMove(["w"], 1, timeout=0.25),
        PROTrainerMove(["w"], 1, timeout=0.25),
        PROTrainerMove(["w"], 1, timeout=0.25),
        PROTrainerMove(["w"], 1, timeout=0.25),
        PROTrainerMove(["w"], 1, timeout=0.25),
        PROTrainerMove(["w"], 1, timeout=0.25),
        #
        #   Into the grass
        PROTrainerMove(["d"], 12, timeout=0.25),
        PROTrainerMove(["w"], 1, timeout=0.5),
    ])

    # Init farm move sequence
    #farm_move_sequence = default_move_set


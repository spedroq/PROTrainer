from farmer.farmer import Farmer
from move_set.move_set import PROTrainerMoveSequence, PROTrainerMove


class FishingRodFarmer(Farmer):
    """
    Class that defines WaterFarmer derived from Farmer.
    Used to farm XP in the water using the fishing rod.
    """

    # Define moves
    default_move_set = PROTrainerMoveSequence([PROTrainerMove(["1"], 1, timeout=3, random_deviation=1)])
    poke_center_move_set = PROTrainerMoveSequence([PROTrainerMove(["4", "w"], 66, timeout=0.10),
                                                   PROTrainerMove(["1", " ", "s"], 20, timeout=0.10),
                                                   PROTrainerMove(["s"], 120, timeout=0.10)])

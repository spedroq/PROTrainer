from farmer.farmer import Farmer
from move_set.move_set import PROTrainerMoveSequence


class GhostTowerFarmer(Farmer):
    """
    Class that defines GhostTowerFarmer derived from Farmer.
    Used to farm XP in the in the ghost tower.
    """

    # Define moves
    default_move_set = PROTrainerMoveSequence(["s,1|10", "w,1|10"])
    poke_center_move_set = PROTrainerMoveSequence(["4,w|30", "4,d, |15", "1, ,a|15", "a|10"])

    # Init farm move sequence
    farm_move_sequence = default_move_set

    def farm(self):
        """
        Implement the abstract function farm() with the specific implementation
        to farm in the ghost tower.
        """
        if self.radon_status.get("code") == 20:
            # Speak to Nurse Joy Sequence as no PP
            self.farm_move_sequence = self.poke_center_move_set
        elif self.radon_status.get("code") == 10:
            # Login to the game, read all the tiles and click there
            mouse_click_sequences = []
            for tile in self.radon_status.get("tiles"):
                mouse_click_sequences.append("mouse_left%{}%{}|1".format(
                    tile["info"]["x"], tile["info"]["y"]
                ))
                click_on_login_move_sequence = PROTrainerMoveSequence(mouse_click_sequences)
                self.farm_move_sequence = click_on_login_move_sequence
        else:
            # Farm Sequence
            self.farm_move_sequence = self.default_move_set
        #print(self.farm_move_sequence)





from farmer.farmer import Farmer
from move_set.move_set import PROTrainerMoveSequence


class VictoryRoadFarmer(Farmer):
    """
    Class that defines VictoryRoadFarmer derived from Farmer.
    Used to farm XP in the in the high level pokemon cave.
    """

    # Define moves
    default_move_set = PROTrainerMoveSequence(["a,1|10", "d,1|10"])
    poke_center_move_set = PROTrainerMoveSequence([
        # Get out of the cave
        "d,4|20", "w,4|20", "a,4|1", "w,4|1", "a,4|1", "w,4|1", "a,4|1", "w,4|1",
        "d,4|1", "w,4|1", "d,4|1", "w|1", "d|6",
        # To Pokecenter
        "w|20", "d|9", "w|2",
        # In Pokecenter
        "w|4", "a|6", "w, |10", "1, ,s|10",
        # Get out of the Pokecenter
        "d|10", "s|10", "a|12",
        # Into the cave
        "s,1|20", "s,1|20"], 1)

    # Init farm move sequence
    farm_move_sequence = default_move_set

    def farm(self):
        """
        Implement the abstract function farm() with the specific implementation
        to farm in the victory road.
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

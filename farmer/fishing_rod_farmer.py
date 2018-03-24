from farmer.farmer import Farmer
from move_set.move_set import PROTrainerMoveSequence


class FishingRodFarmer(Farmer):
    """
    Class that defines WaterFarmer derived from Farmer.
    Used to farm XP in the water using the fishing rod.
    """

    TURN = 0
    WRAP_AROUND = 3

    # Define moves
    #default_move_set = PROTrainerMoveSequence(["1|1"])
    default_move_set = PROTrainerMoveSequence(["a,1|6", "d,1|6"])
    poke_center_move_set = PROTrainerMoveSequence(["4|25", "w|25", "1, ,s|25", "s|25"])

    # Init farm move sequence
    farm_move_sequence = default_move_set

    def farm(self):
        """
        Implement the abstract function farm() with the specific implementation
        to farm with a fishing rod in the water.
        """
        #
        # Check what codes that Radon passed, if it's a high-priority code
        # check it first, then look to see if we need to change our moveset
        # to click on the screen
        if self.radon_status.get("code") == 20:
            # Speak to Nurse Joy Sequence as no PP
            self.farm_move_sequence = self.poke_center_move_set
        # If Radon passed this tile element in the dictionary, we need to click
        # on the tiles it passed us
        elif self.radon_status.get("tiles"):
            # Map these tiles onto a move sequence
            mouse_click_sequences = []
            #print("\tclicking on {} tiles".format(len(self.radon_status.get("tiles"))))
            for tile in self.radon_status.get("tiles"):
                # Get the mid points of these tiles and then click there
                # Add this click to the current move sequence at the center of
                # the tile
                mouse_click_sequences.append("mouse_left%{}%{}|1".format(
                    tile["info"]["x"], tile["info"]["y"]
                ))
                click_on_tiles_move_sequence = PROTrainerMoveSequence(mouse_click_sequences)
                # Change the current move sequece to this one
                self.farm_move_sequence = click_on_tiles_move_sequence
        else:
            # Farm Sequence
            self.farm_move_sequence = self.default_move_set


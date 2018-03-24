from farmer.farmer import Farmer
from move_set.move_set import PROTrainerMoveSequence


class SurfFarmer(Farmer):
    """
    Class that defines SurfFarmer derived from Farmer.
    Used to farm XP surfing in the water.
    """

    # Define moves
    default_move_set = PROTrainerMoveSequence(["s,1, ,mouse_left%1071%580|12", "w,1|4"])
    poke_center_move_set = PROTrainerMoveSequence(["4,w|30", "4,w, |15", "1, ,s|15",
                                                   "1, ,s,mouse_left%1071%580|15"])

    # Init farm move sequence
    farm_move_sequence = default_move_set

    def farm(self):
        """
        Implement the abstract function farm() with the specific implementation
        to farm surfing in the water.
        """
        if self.radon_status.get("code") == 20:
            # Speak to Nurse Joy Sequence as no PP
            self.farm_move_sequence = self.poke_center_move_set
        # If Radon passed this tile element in the dictionary, we need to click
        # on the tiles it passed us
        elif self.radon_status.get("tiles"):
            # Map these tiles onto a move sequence
            mouse_click_sequences = []
            print("\tclicking on {} tiles".format(
                len(self.radon_status.get("tiles"))))
            for tile in self.radon_status.get("tiles"):
                # Get the mid points of these tiles and then click there
                # Add this click to the current move sequence at the center of
                # the tile
                if len(mouse_click_sequences) < 9:
                    mouse_click_sequences.append("mouse_left%{}%{}|1".format(
                        tile["info"]["x_center"], tile["info"]["y_center"]
                    ))
                    click_on_tiles_move_sequence = PROTrainerMoveSequence(mouse_click_sequences)
                    # Change the current move sequece to this one
                    self.farm_move_sequence = click_on_tiles_move_sequence
        else:
            # Farm Sequence
            self.farm_move_sequence = self.default_move_set



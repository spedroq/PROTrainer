import threading
from abc import abstractmethod
import time
import win32com.client as com_client
from move_set.move_set import SimulatedKeyboard, PROTrainerMoveSequence


class Farmer(threading.Thread):
    """
    Class that defines the abstract class for Farmer classes.
    Defines:
        :attribute: wsh: Windows Shell to interface with Key presses.
        :attribute: pause: Boolean flag to represent pause state.
        :method: start_farming: Method to start farming.
        :method: farm: Abstract method to farm. Implemented by each
         implementation.
    """
    # Init Windows Shell with WScript Shell
    wsh = com_client.Dispatch("WScript.Shell")
    # Init the flag to pause the farming
    pause = True
    # Init the flag to quit the farming
    quit = False
    # Init the radon text to blank
    radon_status = {
        "code": -1,
        "status": "-1: initalising..."
    }
    # Init the Simulated Keyboard
    keyboard = None
    # Init farm move sequence
    farm_move_sequence = PROTrainerMoveSequence()

    # Attributes need to be set by classes derived by Farmer
    poke_center_move_set = None
    default_move_set = None

    # Last pokemon seen
    last_poke_name = ""

    def run(self) -> None:
        # Create a PROWatch
        self.prowatch = self._args[0]
        """
        Method to init the Farmer class.
        """
        # Init keyboard
        self.keyboard = SimulatedKeyboard(farmer=self)
        # Start Farming
        self.start_farming()

    """ Farm """

    def start_farming(self) -> None:

        # Keep farming while quit is False
        while not self.quit:
            time.sleep(0.25)

            # Farm if pause is False
            if not self.pause:
                # Farm away
                self.farm()
                self.keyboard.use_move_sequence(self.farm_move_sequence)
                
                # self.handle_radon_results(self.radon.read_text_from_screenshot_taken_right_row())

    def farm(self):
        """
        Implement the abstract function farm() with the specific implementation
        to farm with a fishing rod in the water.
        """
        # Farm Sequence
        self.farm_move_sequence = self.default_move_set
        self.prowatch.append_write_to_log(
            1,
            "protrainer started using the farm move sequence",
            self.farm_move_sequence,
            "None"
        )

    """ Pause """

    def toggle_pause(self) -> None:
        # Toggle pause between True or False
        self.pause = not self.pause

    def set_quit(self) -> None:
        # Set quit to True to stop the farming
        self.quit = True

    """ Radon Interaction """

    def deliver_radon_status(self, status: dict):
        self.radon_status = status
        #print(self.radon_status["status"])

    """ Validate Move Status """

    def validate(self) -> bool:
        """
        Validate if there is any radon output and if the farming is paused.
        :return: bool value of weather the move should be played or not.
        """
        #
        # Check what codes that Radon passed, if it's a high-priority code
        # check it first, then look to see if we need to change our moveset
        # to click on the screen
        if self.radon_status.get("code") == 20:
            # Speak to Nurse Joy Sequence, there is no PP
            # Perform a move sequence
            self.keyboard.use_move_sequence(self.poke_center_move_set, validate=False)
            self.prowatch.append_write_to_log(
                1,
                "protrainer started using pokecenter move sequence",
                self.poke_center_move_set,
                "None"
            )
        
        # We need to catch this pokemon by throwing a pokeball
        if False:
            print("VALID POKE, SHOULD CATCH")
            #
            #   Make sure we start pressing Items not Attack
            throw_pokeball_move_sequence = PROTrainerMoveSequence(["3|15"],0.5)
            self.keyboard.use_move_sequence(throw_pokeball_move_sequence, validate=False)
            #
            #   Handle clicking on the pokeball
            mouse_click_sequences = []
            if self.radon_status.get("tiles"):
                for tile in self.radon_status.get("tiles"):
                    mouse_click_sequences.append("mouse_left%{}%{}|1".format(
                        tile["info"]["x_center"], tile["info"]["y_center"]
                    ))
                click_on_tiles_move_sequence = PROTrainerMoveSequence(mouse_click_sequences)
                self.keyboard.use_move_sequence(click_on_tiles_move_sequence, validate=False)
            self.last_poke_name = ""
            self.prowatch.append_write_to_log(
                1,
                "protrainer started using a catch pokemon move sequence",
                click_on_tiles_move_sequence,
                "None"
            )

        # If Radon passed this tile element in the dictionary, we need to click
        # on the tiles it passed us
        if self.radon_status.get("tiles"):
            radon_tiles = self.radon_status.get("tiles")
            # Map these tiles onto a move sequence
            if len(radon_tiles) > 9:
                radon_tiles = radon_tiles[:9]
            mouse_click_sequences = []
            for tile in radon_tiles:
                # Get the mid points of these tiles and then click there
                # Add this click to the current move sequence at the center of
                # the tile
                mouse_click_sequences.append("mouse_left%{}%{}|1".format(
                    tile["info"]["x_center"], tile["info"]["y_center"]
                ))
            click_on_tiles_move_sequence = PROTrainerMoveSequence(mouse_click_sequences)
            # Perform a move sequence
            # TODO:  CAUTION: THIS MAY BREAK CLICKING (was indented into the list)
            self.keyboard.use_move_sequence(click_on_tiles_move_sequence, validate=False)
            self.prowatch.append_write_to_log(
                1,
                "protrainer started using using click on tiles move sequence",
                click_on_tiles_move_sequence,
                "None"
            )

        # Return the current pause status
        return self.pause

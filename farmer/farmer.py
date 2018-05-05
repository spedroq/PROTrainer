import threading
from abc import abstractmethod
import time
import win32com.client as com_client
from move_set.move_set import SimulatedKeyboard, PROTrainerMoveSequence, PROTrainerMove
from prowatch.PROWatchReplay import *


""" AFK Randomisers """


def get_short_afk_sleep() -> float:
    """
    Static method to generate a random short AFK sleep time.
    :return: a random AFK sleep time
    """
    # TODO: Log AFK status
    # print('Short AFK')
    # Between 5 secs and 10 secs
    return random.uniform(5, 10)


def get_long_afk_sleep() -> float:
    """
    Static method to generate a random long AFK sleep time.
    :return: a random AFK sleep time
    """
    # TODO: Log AFK status
    # print('Long AFK')
    # Between 20 secs and 1800 secs - 30 mins
    return random.uniform(20, 1800)


def get_random_afk_timeout() -> int:
    """
    Method to reset the AFK timeout.
    """
    # Between 10 secs and 450 secs - 7.5 mins
    return random.randint(10, 450)


""" END AFK Randomisers"""


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
    pause = False
    # Init the flag to quit the farming
    quit = False
    reset_mode = False
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
    # Pokemon we want to catch
    pokes_to_catch = [
        "kadabra",
        "abra",
        "ditto",
        "growlithe",
        "jigglypuff",
        "vulpix",
        "gastly",
        "gengar",
        "cubone",
        "staryu",
        "pikachu",
        "meowth"
    ]

    # AFK timeout
    afk_timeout = get_random_afk_timeout()
    #
    #   Emergency Reset Counter
    emergency_reset_radon_unknown_statuses_limit = 500
    unknown_radon_statuses_counter = 0
    sequential_radon_status_limit = 500
    sequential_radon_status_count = 0
    last_radon_status = {}

    is_emergency = False

    # OTHER THREAD MODULES
    control_thread = None
    prowatch_thread = None

    def run(self) -> None:
        print("New Farmer thread started!!!!")
        # Create a PROWatch
        self.control_thread = self._args[0]
        self.prowatch_thread = self.control_thread.prowatch_thread
        self.pause = self.control_thread.farmer_pause
        """
        Method to init the Farmer class.
        """
        # Init keyboard
        self.keyboard = SimulatedKeyboard(farmer=self, control=self.control_thread)
        # Start Farming
        self.start_farming()

    """ Farm """

    def start_farming(self) -> None:
        """
        Method to start farming.
        """
        # Keep farming while quit is False
        # TODO: Fix quit functionality
        while not self.quit:
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
        self.prowatch_thread.append_write_to_log(
            1,
            "protrainer started using the farm move sequence",
            self.farm_move_sequence,
            "None"
        )

    """ Pause """

    def toggle_pause(self) -> None:
        """
        Method to toggle pause between True and False.
        """
        # Toggle pause between True or False
        self.pause = not self.pause
        print(self.pause)

    def set_quit(self) -> None:
        """
        Method to quit the PROTrainer.
        """
        # Set quit to True to stop the farming
        self.quit = True

    """ Radon Interaction """

    def deliver_radon_status(self, status: dict) -> None:
        #
        #   Deliver the Radon Status
        self.radon_status = status
        #
        #   Marker for is an emergency
        #is_emergency = self.is_emergency
        #
        #   E M E R G E N C Y  C H E C K
        #if self.unknown_radon_statuses_counter > self.emergency_reset_radon_unknown_statuses_limit:
        #    self.is_emergency = True
        #if self.sequential_radon_status_count > self.sequential_radon_status_limit:
        #    self.is_emergency = True

        #if self.is_emergency:
        #    self.prowatch_thread.append_write_to_log(
        #        97,
        #        "emergency, protrainer has been reading the same radon status for too long",
        #        "None",
        #        "None"
        #    )
        #    print("E M E R G E N C Y  -  P A U S I N G")
        #    #
        #    #   P A U S E
        #    #self.paused = True
        #    self.is_emergency = True

        #
        #   When the status is delivered, count up any sequential 0s
        if status["code"] == 0:
            #
            #   If it's a 0, add up the 0 counter
            self.unknown_radon_statuses_counter = 1
        #
        #   If it's not equal to 0, reset the counter as it's a sequential count for unknowns
        if status["code"] != 0:
            self.unknown_radon_statuses_counter = 0
        #
        #   If this status is different to the last one reset the sequential count
        if status != self.last_radon_status:
            self.sequential_radon_status_count = 0
        #
        #   If this status is the same as the last one, add one to the counter
        if status == self.last_radon_status:
            self.sequential_radon_status_count = 1
        #
        #   Set our last status
        self.last_radon_status = self.radon_status
        #
        #   Print the status 
        print(self.radon_status["status"])

    """ Validate Move Status """

    def validate(self) -> None:
        """
        Validate if there is any radon output.
        :return: bool value of weather the move should be played or not.
        """
        #
        # Check what codes that Radon passed, if it's a high-priority code
        # check it first, then look to see if we need to change our moveset
        # to click on the screen
        #if self.radon_status.get("code") == 20 or self.is_emergency:
        if self.radon_status.get("code") == 20:
            # Speak to Nurse Joy Sequence, there is no PP
            # Perform a move sequence
            self.keyboard.use_move_sequence(self.poke_center_move_set, validate=False)
            self.prowatch_thread.append_write_to_log(
                1,
                "protrainer started using pokecenter move sequence",
                self.poke_center_move_set,
                "None"
            )
            #self.is_emergency = False

        """ CATCH POKEMON """
        # We need to catch this pokemon by throwing a pokeball
        if self.last_poke_name.lower() in self.pokes_to_catch:
            print("V A L I D  P O K E  -  S H O U L D  C A T C H")
            #
            #   Make sure we start pressing Items not Attack
            throw_pokeball_move_sequence = PROTrainerMoveSequence("throw_pokeball_move_sequence", [
                PROTrainerMove(["3"], 15, 0.5)
            ])
            self.keyboard.use_move_sequence(throw_pokeball_move_sequence, validate=False)
            #
            #   Handle clicking on the pokeball
            mouse_click_sequences = []
            if self.radon_status.get("tiles"):
                radon_tiles = self.radon_status.get("tiles")
                protrainer_moves = []
                for tile in radon_tiles:
                    # Get the mid points of these tiles and then click there
                    # Add this click to the current move sequence at the center of
                    # the tile
                    # mouse_click_sequences.append("mouse_left%{}%{}1".format(
                    #     tile["info"]["x_center"], tile["info"]["y_center"]
                    # ))
                    type_and_coordinates = "mouse_left%{}%{}".format(
                        tile["info"]["x_center"], tile["info"]["y_center"]
                    )
                    protrainer_moves.append(
                        PROTrainerMove([type_and_coordinates], 1, 0.5)
                    )

                click_on_tiles_move_sequence = PROTrainerMoveSequence("click_on_tiles_move_sequence",
                                                                      protrainer_moves)
                print(click_on_tiles_move_sequence)
                self.keyboard.use_move_sequence(click_on_tiles_move_sequence, validate=False)
                self.prowatch_thread.append_write_to_log(
                    1,
                    "protrainer started using a catch pokemon move sequence",
                    click_on_tiles_move_sequence,
                    "None"
                )
            self.last_poke_name = ""

        # If Radon passed this tile element in the dictionary, we need to click
        # on the tiles it passed us
        if self.radon_status.get("tiles"):
            radon_tiles = self.radon_status.get("tiles")
            print("\tR A D O N  D E L I V E R E D  {}  T I L E S".format(
                len(radon_tiles)
            ))
            if self.radon_status.get("code") == 12:
                print("I G N O R E D  I N C O M I N G  R A N D O  M E S S A G E  S T A T U S")
            else:
                # Map these tiles onto a move sequence
                if len(radon_tiles) > 9:
                    radon_tiles = radon_tiles[:9]
                mouse_click_sequences = []
                protrainer_moves = []
                for tile in radon_tiles:
                    # Get the mid points of these tiles and then click there
                    # Add this click to the current move sequence at the center of
                    # the tile
                    # mouse_click_sequences.append("mouse_left%{}%{}1".format(
                    #     tile["info"]["x_center"], tile["info"]["y_center"]
                    # ))
                    type_and_coordinates = "mouse_left%{}%{}".format(
                        tile["info"]["x_center"], tile["info"]["y_center"]
                    )
                    protrainer_moves.append(
                        PROTrainerMove([type_and_coordinates], 1, 0.5)
                    )

                click_on_tiles_move_sequence = PROTrainerMoveSequence("click_on_tiles_move_sequence",
                                                                      protrainer_moves)
                #print(click_on_tiles_move_sequence)
                # Perform a move sequence
                # TODO:  CAUTION: THIS MAY BREAK CLICKING (was indented into the list)
                self.keyboard.use_move_sequence(click_on_tiles_move_sequence, validate=False)
                self.prowatch_thread.append_write_to_log(
                    1,
                    "protrainer started using using click on tiles move sequence",
                    click_on_tiles_move_sequence,
                    "None"
                )

    """ AFK """

    def reduce_afk_timeout(self, reduce_by: float) -> None:
        """
        Method to reduce the AFK timeout.
        """
        self.afk_timeout -= reduce_by

    @staticmethod
    def get_afk_sleep() -> float:
        """
        Method that randomizes between long or short AFK time.
        :return: a short or long AFK sleep.
        """
        """
        # 1 in every 20 AFKs it will be a long afk
        one_in_every = 20
        rand = random.randint(0, one_in_every) + 1
        if rand < one_in_every:
            sleep_timer = get_short_afk_sleep()
        else:
            sleep_timer = get_long_afk_sleep()
        return sleep_timer
        """
        # For now only afk for a short time
        # in case we reset to an unknown location such as a pokecenter
        # when battling in the ghost town or cave
        return get_short_afk_sleep()

    def reset_afk_timeout(self):
        """
        Static method to reset AFK timeout.
        """
        self.afk_timeout = get_random_afk_timeout()

    def reset(self):
        self.reset_mode = True



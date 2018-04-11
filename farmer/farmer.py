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
    # Pokemon we want to catch
    pokes_to_catch = [
        "kadabra",
        "abra",
        "squirtle",
        "ditto",
        "growlithe",
        "jigglypuff",
        "vulpix",
        "gastly",
        "gengar",
        "cubone",
        "staryu"
    ]

    # AFK timeout
    afk_timeout = get_random_afk_timeout()
    #
    #   Emergency Reset Counter
    emergency_reset_radon_unknown_statuses_limit = 999
    unknown_radon_statuses_counter = 0

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
        self.prowatch.append_write_to_log(
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

    def set_quit(self) -> None:
        """
        Method to quit the PROTrainer.
        """
        # Set quit to True to stop the farming
        self.quit = True

    """ Radon Interaction """

    def deliver_radon_status(self, status: dict) -> None:
        self.radon_status = status
        #
        #   When the status is delivered, count up any sequential 0s
        if status["code"] == 0:
            self.unknown_radon_statuses_counter += 1
            if self.unknown_radon_statuses_counter > (self.emergency_reset_radon_unknown_statuses_limit * 0.80):
                self.prowatch.append_write_to_log(
                    98,
                    "warning, protrainer has been experiencing sequential unknown radon statuses, limit 80% reached",
                    "None"
                    "None"
                )
                print("warning, protrainer has been experiencing sequential unknown radon statuses, limit 80% reached")
        #
        #   If it's not equal to 0, reset the counter as it's a sequential counter
        if status["code"] != 0:
            self.unknown_radon_statuses_counter = 0
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
        if self.radon_status.get("code") == 20 or self.unknown_radon_statuses_counter > self.emergency_reset_radon_unknown_statuses_limit:
            if self.unknown_radon_statuses_counter > self.emergency_reset_radon_unknown_statuses_limit:
                print("E R R O R:  W E  A R E  L O S T  -  A B O R T  B Y  P A U S I N G")
                self.prowatch.append_write_to_log(
                    99,
                    "protrainer is lost, paused inputs",
                    self.poke_center_move_set,
                    "None"
                )
                self.unknown_radon_statuses_counter = 0
                #
                #   Pause all input
                self.pause = True

            # Speak to Nurse Joy Sequence, there is no PP
            # Perform a move sequence
            self.keyboard.use_move_sequence(self.poke_center_move_set, validate=False)
            self.prowatch.append_write_to_log(
                1,
                "protrainer started using pokecenter move sequence",
                self.poke_center_move_set,
                "None"
            )

        """ CATCH POKEMON """
        # We need to catch this pokemon by throwing a pokeball
        if self.last_poke_name.lower() in self.pokes_to_catch:
            print("V A L I D  P O K E  -  S H O U L D  C A T C H")
            #
            #   Make sure we start pressing Items not Attack
            throw_pokeball_move_sequence = PROTrainerMoveSequence([PROTrainerMove(["3"], 15, 0.5)])
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

                click_on_tiles_move_sequence = PROTrainerMoveSequence(protrainer_moves)
                print(click_on_tiles_move_sequence)
                self.keyboard.use_move_sequence(click_on_tiles_move_sequence, validate=False)
                self.prowatch.append_write_to_log(
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

            click_on_tiles_move_sequence = PROTrainerMoveSequence(protrainer_moves)
            #print(click_on_tiles_move_sequence)
            # Perform a move sequence
            # TODO:  CAUTION: THIS MAY BREAK CLICKING (was indented into the list)
            self.keyboard.use_move_sequence(click_on_tiles_move_sequence, validate=False)
            self.prowatch.append_write_to_log(
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



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
        :method: press_1: Presses key 1.
        :method: press_w: Presses key w.
        :method: press_s: Presses key s.
        :method: press_d: Presses key d.
        :method: press_a: Presses key a.
        :method: farm: Abstract method to farm. Implemented by each
         implementation.
    """
    # Init timeout and count for healing
    TIMEOUT = 1800
    COUNT = 1
    # Init Windows Shell with WScript Shell
    wsh = com_client.Dispatch("WScript.Shell")
    # Init the flag to pause the farming
    pause = True
    # Init the flag to quit the farming
    quit = False
    # Init the Simulated Keyboard
    keyboard = SimulatedKeyboard()
    # Init farm move sequence
    farm_move_sequence = PROTrainerMoveSequence()
    # Create Radon for managing screenshots / OCR
    # radon = Radon(pt)

    def run(self) -> None:
        """
        Method to init the Farmer class.
        """
        self.start_farming()

    """ Farm """

    def start_farming(self) -> None:

        # Keep farming while quit is False
        while not self.quit:
            time.sleep(0.1)

            # Farm if pause is False
            if not self.pause:
                # Farm away
                self.farm()
                self.COUNT = self.COUNT + self.keyboard.use_move_sequence(self.farm_move_sequence)
                # self.handle_radon_results(self.radon.read_text_from_screenshot_taken_right_row())

    @abstractmethod
    def farm(self):
        pass

    """
    @abstractmethod
    def handle_radon_results(self, radon_results: str):
        pass
    """

    """ Pause """

    def toggle_pause(self) -> None:
        # Toggle pause between True or False
        self.pause = not self.pause

    def set_quit(self) -> None:
        # Set quit to True to stop the farming
        self.quit = True

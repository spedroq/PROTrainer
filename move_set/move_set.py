import time
import pythoncom
import win32api
import win32com.client as com_client
import win32con


class PROTrainerMove:
    """
    Class PROTrainer Move defines the data for a single move.
    """
    def __init__(self, input_characters: list=list(), iterations: int=1, timeout: float=0.25):
        self.input_characters = input_characters
        self.iterations = iterations
        self.timeout = timeout

    def __repr__(self):
        output_string = "PROTrainerMove: "
        for char in self.input_characters:
            output_string += char + "_"
        output_string += " | x" + str(self.iterations)
        output_string += " | " + str(self.timeout) + "s"
        return output_string


class PROTrainerMoveSequence:
    """
    Class PROTrainerMoveSequence defines data structure for a sequence of moves.
    """
    def __init__(self, move_sequence: list=list()):
        self.move_sequence = move_sequence

    def __repr__(self):
        output_string = "PROTrainerMoveSequence: {}".format(self.move_sequence)
        output_string = output_string.replace(",", "_")
        return output_string


class SimulatedKeyboard:
    """
    Class SimulatedKeyboard defines the simulated keyboard output to PRO.
    """
    def __init__(self, farmer: 'Farmer'):
        pythoncom.CoInitialize()
        # Init Windows Shell with WScript Shell
        self.wsh = com_client.Dispatch("WScript.Shell")
        self.farmer = farmer

    def use_move_sequence(self, protms: PROTrainerMoveSequence, validate: bool=True) -> None:
        """
        Method to run through a move sequence.
        Ex.:
            - ["mouse_left%500%300"] -> ["mouse_left"] x 15 clicks at position [500, 300]
        :param protms: PRO Trainer Move Sequence object to execute.
        :param validate: flag of whether this should call the validate() method or not.
                         NOTE: This is crucial since we need call validate() from within this method,
                               and validate() can call this method with a new move sequence to use.
                               Otherwise we get stuck in an infinite loop.
                         DEFAULT: True, as in do use validate().
        """
        # Iterate through moves in the move sequence
        for move in protms.move_sequence:
            # Get the input characters of the move
            # ["w", "s", " "]
            keys = move.input_characters
            # Get the number of iterations of move repetition
            loop_count = move.iterations

            # Iterate through number of repetitions
            for i in range(0, loop_count):
                # Iterate through number of keys
                key_index = 0
                while key_index < len(keys):
                    if not self.farmer.pause:
                        # Check if we should validate the move or not
                        # So that validation method can run moves
                        if validate:
                            self.farmer.validate()
                        # Get the key
                        key = keys[key_index]
                        # Process key
                        self.perform_move(key, move)
                        # Listen for radon output with PROWatch log
                        self.farmer.prowatch.append_write_to_log(
                            2,
                            "protrainer simulated some input",
                            key,
                            move
                        )
                        # Increment index
                        key_index += 1

    def perform_move(self, key: str, move: PROTrainerMove):
        if "mouse" in key:
            # Split the coordinates and mouse click
            mouse_config = key.split("%")
            key = mouse_config[0]
            x_coordinate = mouse_config[1]
            y_coordinate = mouse_config[2]
            # Sleep
            time.sleep(move.timeout)
            # Press key
            self.press_mouse(key, int(x_coordinate), int(y_coordinate))
        else:
            # Sleep
            time.sleep(move.timeout)
            # Press key
            self.press_key(key)

    def press_key(self, key: str) -> None:
        """
        Helper method to press a key.
        :param key: Key to be pressed.
        """
        # Set output to Pokemon Revolution Online
        self.wsh.AppActivate("Pokemon Revolution")
        # Send the keys press
        self.wsh.SendKeys(key)

    def press_mouse(self, key: str, x: int, y: int) -> None:
        """
        Helper method to press a mouse key.
        :param key: Key to be pressed.
        """
        if key == 'mouse_left':
            self.press_mouse_left(x, y)

    @staticmethod
    def press_mouse_left(x: int, y: int) -> None:
        """
        Static method to click mouse at position x, y.
        :param x: x coordinate.
        :param y: y coordinate.
        """
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

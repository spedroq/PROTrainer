import random
import time
import pythoncom
import win32api
import win32com.client as com_client
import win32con


class PROTrainerMove:
    """
    Class PROTrainer Move defines the data for a single move.
    """
    def __init__(self, input_characters: list=list(), iterations: int=1, timeout: float=0.25, random_deviation: float=0):
        self.input_characters = input_characters
        self.iterations = iterations
        self.timeout = timeout
        self.random_deviation = random_deviation

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
    def __init__(self, name: str="unnamed", move_sequence: list=list()):
        self.name = name
        self.move_sequence = move_sequence

    def __repr__(self):
        output_string = "PROTrainerMoveSequence: {}".format(self.move_sequence)
        output_string = output_string.replace(",", "_")
        return output_string


class SimulatedKeyboard:
    """
    Class SimulatedKeyboard defines the simulated keyboard output to PRO.
    """
    def __init__(self, farmer: 'Farmer', control: 'Control'):
        pythoncom.CoInitialize()
        # Init Windows Shell with WScript Shell
        self.wsh = com_client.Dispatch("WScript.Shell")
        self.farmer = farmer
        self.control_thread = control

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
        if not self.farmer.pause:
            print("Playing: {}".format(protms.name))
            self.control_thread.latest_move_sequence = protms
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
                    # Set default random_sleep in case the game is paused
                    random_sleep = 0.5
                    if not self.farmer.reset_mode:
                        if not self.farmer.pause:

                            """ AFK Check """

                            # AFK Check
                            if self.farmer.afk_timeout > 0:

                                """ Not AFK """

                                # TODO: Log AFK status
                                # print('Not AFK - timeout: {}'.format(self.farmer.afk_timeout))

                                # Check if we should validate the move or not
                                # So that validation method can run moves
                                if validate:
                                    self.farmer.validate()
                                # Get the key
                                key = keys[key_index]
                                # Process key
                                self.perform_move(key, move)
                                # Listen for radon output with PROWatch log
                                self.farmer.prowatch_thread.append_write_to_log(
                                    2,
                                    "protrainer simulated some input",
                                    key,
                                    move
                                )
                                # Increment index
                                key_index += 1
                                # Sleep every turn so we do not burn the pc
                                # Randomize the sleep so it is more human
                                random_sleep = random.uniform(move.timeout, move.timeout + move.random_deviation)
                                # Reduce the afk timeout
                                self.farmer.reduce_afk_timeout(random_sleep)
                                # Check if we should validate the move or not
                                # So that validation method can run moves
                                if validate:
                                    self.farmer.validate()
                            else:

                                """ AFK """
                                print('AFK')
                                # Reset the afk timeout
                                self.farmer.reset_afk_timeout()

                                # TODO: Log AFK status
                                # print('AFK - timeout: {} sleep for: {}'.format(self.farmer.afk_timeout,
                                #                                                self.farmer.get_afk_sleep()))

                                # AFK Sleep
                                time.sleep(self.farmer.get_afk_sleep())
                                # Check if we should validate the move or not
                                # So that validation method can run moves
                                if validate:
                                    # Validate after AFK
                                    self.farmer.validate()
                    else:
                        self.farmer.reset_mode = False
                        # Reset the move sequence
                        return None

                    # TODO: Log Random sleep status
                    #  print(random_sleep)

                    # Sleep for the move turn, partly randomized
                    # TODO: Make the sleep incrementally check radon
                    self.sleep(random_sleep)

                    # Check if we should validate the move or not
                    # So that validation method can run moves
                    if validate:
                        # Validate after sleep
                        self.farmer.validate()

    def sleep(self, sleep_amount: float):
        # Split the time into integer and fraction integer parts
        integer = int(sleep_amount)
        fraction = sleep_amount - integer
        # Sleep for the integer part
        if integer:
            for sec in range(0, integer):
                # Validate after sleep
                self.farmer.validate()
                # Sleep for a second
                time.sleep(sec)
                # Validate after sleep
                self.farmer.validate()

        # Sleep for the fraction part
        time.sleep(fraction)

    def perform_move(self, key: str, move: PROTrainerMove):
        if key != "nothing":
            if "mouse" in key:
                # Split the coordinates and mouse click
                mouse_config = key.split("%")
                key = mouse_config[0]
                x_coordinate = mouse_config[1]
                y_coordinate = mouse_config[2]
                # Press key
                self.press_mouse(key, int(x_coordinate), int(y_coordinate))
            else:
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

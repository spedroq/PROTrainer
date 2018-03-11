import time
import win32com.client as com_client


class PROTrainerMoveSequence:
    """
    Class PROTrainerMoveSequence defines data structure for a sequence of moves.
    """
    def __init__(self, move_sequence: list=list()):
        self.move_sequence = move_sequence

    def __repr__(self):
        return "PROTrainerMoveSequence: {}".format(self.move_sequence)


class SimulatedKeyboard:
    """
    Class SimulatedKeyboard defines the simulated keyboard output to PRO.
    """
    def __init__(self):
        # Init Windows Shell with WScript Shell
        self.wsh = com_client.Dispatch("WScript.Shell")
        self.timeout = 0.25

    def use_move_sequence(self, protms) -> int:
        """
        Method to run through a move sequence.
        Ex.:
            [ "w,s, |15", "w|15", "s|15"] -> [ "w", "s", " "] x 15, ["w"] x 15, ["s"] x 15
        :param protms: PRO Trainer Move Sequence object to execute.
        :return: the number of moves performed.
        """
        #
        count = 0
        # Iterate through moves in the move sequence
        for move in protms.move_sequence:
            # [ "w,s, |15"] -> ["w", "s", " "]
            keys = move.split("|")[0].split(",")
            # [ "w,s, |15"] -> 15
            loop_count = int(move.split("|")[1])
            # Iterate through number of repetitions
            for i in range(0, loop_count):
                # Iterate through number of keys
                for key in keys:
                    # Sleep
                    time.sleep(self.timeout)
                    # Press key
                    self.press_key(key)
                    # Add count
                    count += 1

        return count

    def press_key(self, key: str) -> None:
        """
        Helper method to press a key.
        :param key: Key to be pressed.
        """
        # Set output to Pokemon Revolution Online
        self.wsh.AppActivate("Pokemon Revolution")
        # Send the keys press
        self.wsh.SendKeys(key)

import time
import win32com.client as com_client


class PROTrainerMoveSequence:
    def __init__(self, move_sequence: list=list()):
        self.move_sequence = move_sequence


# KEYIN:Count
# 1:4
# 1:0 = press 1 forever


class SimulatedKeyboard:

    def __init__(self):
        # Init Windows Shell with WScript Shell
        self.wsh = com_client.Dispatch("WScript.Shell")
        self.timeout = 1

    def use_move_sequence(self, protms):

        # [ "w,s, |15", "w:15", "s:15"] -> [ "w", "s", " "]
        for move in protms.move_sequence:
            keys = move.split("|")[0].split(",")
            # [ "w,s, |15"] -> 15
            loop_count = int(move.split("|")[1])
            for key in keys:
                for i in range(0, loop_count):
                    time.sleep(self.timeout)
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

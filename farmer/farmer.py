from abc import abstractmethod
from pynput import keyboard
import win32com.client as com_client


class Farmer:
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
    def __init__(self):
        """
        Method to init the Farmer class.
        """
        # Init Windows Shell with WScript Shell
        self.wsh = com_client.Dispatch("WScript.Shell")

        # Init the flag to pause the farming
        self.pause = False
        # Init the flag to quit the farming
        self.quit = False

    """ Farm """

    def start_farming(self):
        listener = None
        # Run with keyboard listeners for pausing the farming
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            # Keep farming while quit is False
            while not self.quit:

                # Farm if pause is False
                if not self.pause:
                    # Farm away
                    self.farm()

        # If a listener thread was started, then exit it
        if listener is not None:
            listener.exit()

    @abstractmethod
    def farm(self):
        """
        Abstract method that implements farming. To be implemented by classes
        derived from Farmer.
        """
        pass

    """ Pause """

    def on_press(self, key):
        try:
            pass
        except AttributeError:
            print('special key {k} pressed. '
                  'self.quit:{q}, self.pause:{p}'.format(k=key,
                                                         q=self.quit,
                                                         p=self.pause))

    def on_release(self, key):
        try:
            if key.char.lower() == 'q':
                # Set quit to True to stop the farming
                self.quit = True

            if key.char.lower() == 'p':
                # Toggle pause between True or False
                self.pause = not self.pause
                print("Pause:{pause}".format(pause=self.pause))

        except AttributeError:
            print('special key {0} pressed'.format(
                key))

        if key == keyboard.Key.esc:
            # Stop listener
            return False

    """ Key Presses """

    def press_1(self):
        """
        Method to press key 1.
        """
        # Set output to Pokemon Revolution Online
        self.wsh.AppActivate("Pokemon Revolution")
        # Send the keys press
        self.wsh.SendKeys("1")

    def press_2(self):
        """
        Method to press key 2.
        """
        # Set output to Pokemon Revolution Online
        self.wsh.AppActivate("Pokemon Revolution")
        # Send the keys press
        self.wsh.SendKeys("2")

    def press_3(self):
        """
        Method to press key 3.
        """
        # Set output to Pokemon Revolution Online
        self.wsh.AppActivate("Pokemon Revolution")
        # Send the keys press
        self.wsh.SendKeys("3")

    def press_4(self):
        """
        Method to press key 4.
        """
        # Set output to Pokemon Revolution Online
        self.wsh.AppActivate("Pokemon Revolution")
        # Send the keys press
        self.wsh.SendKeys("4")

    def press_5(self):
        """
        Method to press key 5.
        """
        # Set output to Pokemon Revolution Online
        self.wsh.AppActivate("Pokemon Revolution")
        # Send the keys press
        self.wsh.SendKeys("5")

    def press_6(self):
        """
        Method to press key 6.
        """
        # Set output to Pokemon Revolution Online
        self.wsh.AppActivate("Pokemon Revolution")
        # Send the keys press
        self.wsh.SendKeys("6")

    def press_w(self):
        """
        Method to press key w.
        """
        # Set output to Pokemon Revolution Online
        self.wsh.AppActivate("Pokemon Revolution")
        # Send the keys press
        self.wsh.SendKeys("w")

    def press_s(self):
        """
        Method to press key s.
        """
        # Set output to Pokemon Revolution Online
        self.wsh.AppActivate("Pokemon Revolution")
        # Send the keys press
        self.wsh.SendKeys("s")

    def press_d(self):
        """
        Method to press key d.
        """
        # Set output to Pokemon Revolution Online
        self.wsh.AppActivate("Pokemon Revolution")
        # Send the keys press
        self.wsh.SendKeys("d")

    def press_a(self):
        """
        Method to press key a.
        """
        # Set output to Pokemon Revolution Online
        self.wsh.AppActivate("Pokemon Revolution")
        # Send the keys press
        self.wsh.SendKeys("a")

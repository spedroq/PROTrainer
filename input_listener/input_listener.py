import threading
import keyboard


class InputListener(threading.Thread):
    """
    Class InputListener that defines how to listen and react to input.
    """
    # Farmer instance to interact with
    farmer = None

    def run(self) -> None:
        """
        Method to init the Farmer class.
        """
        self.farmer = self._args[0]
        keyboard.hook(self.analyse_key_press)

    def analyse_key_press(self, key: keyboard.KeyboardEvent):
        """
        Method to analyse a key press and deal with it.
        :param key: a key to be analysed.
        """
        # Check if it was a key release
        if key.event_type == 'up':
            # Check for q
            if key.name == 'q':
                # Quit farming
                self.farmer.set_quit()
                print("Quit:(False)")
            # Check for p
            if key.name == 'p':
                # Toggle pause between True or False
                self.farmer.toggle_pause()
                print("Pause:{pause}".format(pause=self.farmer.pause))


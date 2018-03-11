import threading
import keyboard


class InputListener(threading.Thread):
    farmer = None

    def run(self) -> None:
        """
        Method to init the Farmer class.
        """
        self.farmer = self._args[0]
        keyboard.hook(self.analyse_key_press)

    def analyse_key_press(self, key: keyboard.KeyboardEvent):
        if key.event_type == 'up':
            if key.name == 'q':
                # Quit farming
                self.farmer.set_quit()
                print("Quit:(False)")

            if key.name == 'p':
                # Toggle pause between True or False
                self.farmer.toggle_pause()
                print("Pause:{pause}".format(pause=self.farmer.pause))


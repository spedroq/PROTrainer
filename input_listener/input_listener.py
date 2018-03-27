import threading
import keyboard


class InputListener(threading.Thread):
    """
    Class InputListener that defines how to listen and react to input.
    """
    # Farmer instance to interact with
    farmer = None
    cli = None
    prowatch = None

    def run(self) -> None:
        """
        Method to init the Farmer class.
        """
        self.farmer = self._args[0]
        self.cli = self._args[1]
        self.prowatch = self._args[2]
        if self.farmer.pause:
            self.cli.input_string_mode = "paused"
        else:
            self.cli.input_string_mode = "running"
        keyboard.hook(self.analyse_key_press)

    def analyse_key_press(self, key: keyboard.KeyboardEvent):
        """
        Method to analyse a key press and deal with it.
        :param key: a key to be analysed.
        """
        # Log this kep press
        logging_code = 90
        if key.event_type == 'up':
            logging_code = 91
        self.prowatch.append_write_to_log(
            logging_code,
            "a key press was detected",
            key.name,
            key.event_type
        )
        # Check if it was a key release
        """
        if key.event_type == 'up':
            # Check for q
            if key.name == 'q':
                # Quit farming
                self.farmer.set_quit()
                if self.farmer.quit:
                    self.cli.input_string_mode = "quitting"
                print("Quit:(False)")
            # Check for p
           
            if key.name == 'p':
                #
                #   Is it the first time we unpaused?
                #print(self.cli.cli_mode["state"])
                if self.cli.is_loading_screen:
                    #self.cli.cli_mode["state"] = "overview"
                    self.cli.show_overview_screen()
                    self.cli.is_loading_screen = False
                else:
                #
                    self.cli.is_loading_screen = True
                    #self.cli.cli_mode["state"] = "loading"
                    self.cli.show_loading_screen()                    

                # Toggle pause between True or False
                self.farmer.toggle_pause()
                print("Pause:{pause}".format(pause=self.farmer.pause))
                if self.farmer.pause:
                    self.cli.input_string_mode = "paused"
                if not self.farmer.pause:
                    self.cli.input_string_mode = "running"
            """
                




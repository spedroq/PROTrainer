import threading
import keyboard
import mouse

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
        #mouse.hook(self.analyse_mouse_interaction)


    def analyse_mouse_interaction(self, mouse_interaction):
        if type(mouse_interaction) == mouse.ButtonEvent:
            mouse_position = mouse.get_position()
            mouse_interaction_string = "a mouse click was detected @ ({}|{})".format(
               mouse_position[0], mouse_position[1]
            )
            logging_code = 92

            self.prowatch.append_write_to_log(
                logging_code,
                mouse_interaction_string,
                mouse_interaction.button,
                mouse_interaction.event_type
            )
        #if type(mouse_interaction) == mouse.MoveEvent:
        #    mouse_interaction_string = "a mouse movement was detected"
        #    logging_code = 93
            """
            self.prowatch.append_write_to_log(
                logging_code,
                mouse_interaction_string,
                str(mouse_interaction.x) + "|" + str(mouse_interaction.y),
                mouse_interaction.time
            )
            """
        if type(mouse_interaction) == mouse.WheelEvent:
            mouse_interaction_string = "a mouse scroll wheel input was detected"
            logging_code = 94
            self.prowatch.append_write_to_log(
                logging_code,
                mouse_interaction_string,
                mouse_interaction.delta,
                mouse_interaction.time
            )

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
        if key.event_type == "up":
            """
            #
            #   Start a new log
            #print(key.name)
            if key.name == 'f1':
                self.prowatch.start_logging()
            if key.name == 'f3':
                #
                #   Let's start our move sequence
                self.farmer.farm()
            """
            pass


        
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
        
                




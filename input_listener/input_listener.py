import threading
import keyboard
import mouse


class InputListener(threading.Thread):
    """
    Class InputListener that defines how to listen and react to input.
    """
    # OTHER THREAD MODULES
    control_thread = None
    farmer_thread = None
    cli_thread = None
    prowatch_thread = None
    radon_thread = None

    last_key_press = ""

    def run(self) -> None:
        """
        Method to init the Input Listener class thread.
        """
        self.control_thread = self._args[0]
        self.farmer_thread = self.control_thread.farmer_thread
        self.cli_thread = self.control_thread.cli_thread
        self.prowatch_thread = self.control_thread.prowatch_thread
        self.radon_thread = self.control_thread.radon_thread
        if self.farmer_thread.pause:
            self.cli_thread.input_string_mode = "paused"
        else:
            self.cli_thread.input_string_mode = "running"
        keyboard.hook(self.analyse_key_press)
        mouse.hook(self.analyse_mouse_interaction)


    def analyse_mouse_interaction(self, mouse_interaction):
        if type(mouse_interaction) == mouse.ButtonEvent:
            mouse_position = mouse.get_position()
            mouse_interaction_string = "a mouse cli_threadck was detected @ ({}|{})".format(
               mouse_position[0], mouse_position[1]
            )
            logging_code = 92

            self.prowatch_thread.append_write_to_log(
                logging_code,
                mouse_interaction_string,
                mouse_interaction.button,
                mouse_interaction.event_type
            )
            #
            #   Save the location of PRO
            did_set = False
            if mouse_interaction.event_type == "down":
                if self.last_key_press == "f7":

                    if self.radon_thread.TOP_LEFT_CORNER == (-1,-1,):
                        print("SETTING TOP LEFT {}".format(mouse_position))
                        self.radon_thread.TOP_LEFT_CORNER = mouse_position
                        did_set = True

                    if self.radon_thread.TOP_LEFT_CORNER != (-1,-1,) and self.radon_thread.BOTTOM_RIGHT_CORNER == (-1,-1,) and not did_set:
                        print("SETTING BOTTOM RIGHT {}".format(mouse_position))
                        self.radon_thread.BOTTOM_RIGHT_CORNER = mouse_position
                        print("RADON SET TO:\n{}, {}".format(
                            self.radon_thread.TOP_LEFT_CORNER,
                            self.radon_thread.BOTTOM_RIGHT_CORNER
                        ))
                if self.last_key_press == "f8":
                    print("RESETTING LOCATION")
                    self.radon_thread.TOP_LEFT_CORNER = (-1,-1,)
                    self.radon_thread.BOTTOM_RIGHT_CORNER = (-1,-1,)
            


        #if type(mouse_interaction) == mouse.MoveEvent:
        #    mouse_interaction_string = "a mouse movement was detected"
        #    logging_code = 93
            """1
            self.prowatch_thread.append_write_to_log(
                logging_code,
                mouse_interaction_string,
                str(mouse_interaction.x) + "|" + str(mouse_interaction.y),
                mouse_interaction.time
            )
            """
        if type(mouse_interaction) == mouse.WheelEvent:
            mouse_interaction_string = "a mouse scroll wheel input was detected"
            logging_code = 94
            self.prowatch_thread.append_write_to_log(
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
        self.last_key_press = key.name
        #print(self.last_key_press)
            


        # Log this kep press
        logging_code = 90
        if key.event_type == 'up':
            logging_code = 91
        self.prowatch_thread.append_write_to_log(
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
                self.prowatch_thread.start_logging()
            if key.name == 'f3':
                #
                #   Let's start our move sequence
                self.farmer_thread.farm()
            """
            pass


        
        if key.event_type == 'up':
            # Check for q
            if key.name == 'q':
                # Quit farming
                self.farmer_thread.set_quit()
                if self.farmer_thread.quit:
                    self.cli_thread.input_string_mode = "quitting"
                print("Quit:(False)")

            # Check for Caps Lock
            if key.name == 'caps lock':
                #
                #   Is it the first time we unpaused?
                #print(self.cli_thread.cli_thread_mode["state"])
                if self.cli_thread.is_loading_screen:
                    #self.cli_thread.cli_thread_mode["state"] = "overview"
                    self.cli_thread.show_overview_screen()
                    self.cli_thread.is_loading_screen = False
                else:
                    #
                    self.cli_thread.is_loading_screen = True
                    #self.cli_thread.cli_thread_mode["state"] = "loading"
                    self.cli_thread.show_loading_screen()

                # Toggle pause between True or False
                self.farmer_thread.toggle_pause()
                print("Pause:{pause}".format(pause=self.farmer_thread.pause))
                if self.farmer_thread.pause:
                    self.cli_thread.input_string_mode = "paused"
                if not self.farmer_thread.pause:
                    self.cli_thread.input_string_mode = "running"

            # Check for p
            if key.name == 'p':
                print("P has been pressed")
                # Toggle Farmer
                self.control_thread.toggle_farmer()

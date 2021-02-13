import threading
from farmer.farmer import Farmer
from farmer.modes import FarmerMode
#from input_listener.input_listener import InputListener
#from radon.Radon import *
#from cli.cli import *
#from prowatch.PROWatch import *


class Control(threading.Thread):
    """
    Class Control that defines how to control PROTrainer and all the different Modules.
    :attribute prowatch_thread: used for logging.
    :attribute farmer_thread: used to farm.
    :attribute radon_thread: used analyse screen.
    :attribute listener_thread: used listen for input.
    :attribute cli_thread: used output into the console client.
    """

    # Configuration
    farmer_pause = False
    radon_pause = False
    catch_pokemon = False
    emergency_reset = False

    latest_move_sequence = None
    farmer_mode = None

    # CONTROL THREADS
    prowatch_thread = None
    farmer_thread = None
    radon_thread = None
    listener_thread = None
    cli_thread = None

    def run(self) -> None:
        """
        Method to init the Control class thread.
        """
        """ LOAD CONFIGURATION FILE """
        self.load_configuration()

        """ PROWATCH """

        # Create the PROWatch logger
        #self.prowatch_thread = PROWatch()
        # Start the thread
        #self.prowatch_thread.start()

        """ CLI  """

        # Create the CLI
        #self.cli_thread = PROTrainerCLI(name="CLIThread")
        #self.cli_thread.start()

        """ FARMER """
        # Create the farmer thread
        self.farmer_thread = Farmer(name="FarmerThread", args=(self,))
        # Set the mode
        self.farmer_mode = FarmerMode(self)
        # Start the thread
        self.farmer_thread.start()

        """ RADON """

        # Create Radon thread for managing screenshots / OCR
        #self.radon_thread = Radon(name="TesseractInteractionThread",
        #                          args=(self,))
        # Start the thread
        #self.radon_thread.start()

        """ INPUT """

        # Input listener thread
        #self.listener_thread = InputListener(name="InputListenerThread",
        #                                     args=(self,))
        # Listen for input
        #self.listener_thread.start()

    def load_configuration(self):
        """
        Method to load a configuration file.
        """
        # Open file
        file = open("configuration.txt", "r")
        # Iterate through each line in the file
        for line in file:
            # Interpret each line
            self.interpret_configuration(line)

    def interpret_configuration(self, line):
        """
        Method to interpret each configuration line.
        :param line: configuration line to be interpreted.
        """
        # Parse the line
        attribute = self.get_config_attribute(line)
        value = self.get_config_value(line)
        # Report the line Loaded
        print("Loaded {attribute}: {value}".format(attribute=attribute, value=value))

        # Check which configuration to set
        if attribute == "farmer_pause":
            self.farmer_pause = True if value == "True" else False
        elif attribute == "radon_pause":
            self.radon_pause = True if value == "True" else False
        elif attribute == "catch_pokemon":
            self.catch_pokemon = True if value == "True" else False
        elif attribute == "emergency_reset":
            self.emergency_reset = True if value == "True" else False

    @staticmethod
    def get_config_attribute(line: str) -> str:
        """
        Static helper method to parse the configuration attribute from a given line.
        :param line: the line to be parsed.
        :return: the parsed attribute as a string.
        """
        # Split the line
        list_attributes = line.split(":")
        # Check if the line is formatted as expected
        if len(list_attributes) == 2:
            # Retrieve the attribute
            attribute = list_attributes[0].strip()
            return attribute
        else:
            raise Exception("Configuration file has incorrect format.")

    @staticmethod
    def get_config_value(line: str) -> str:
        """
        Static helper method to parse the configuration value from a given line.
        :param line: the line to be parsed.
        :return: the parsed value as a string.
        """
        # Split the line
        list_values = line.split(":")
        # Check if the line is formatted as expected
        if len(list_values) == 2:
            # Retrieve the value
            value = list_values[1].strip()
            return value
        else:
            raise Exception("Configuration file has incorrect format.")

    """ FARMER MODES """

    def toggle_farmer(self):
        """
        Method to toggle between farmer modes.
        """
        # Increment the index
        self.farmer_mode.toggle_mode()



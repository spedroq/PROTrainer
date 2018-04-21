import threading
from farmer.cave_famer import CaveFarmer
from farmer.fishing_rod_farmer import FishingRodFarmer
from farmer.fuchsia_fish_farmer import FuchsiaFishFarmer
from farmer.ghost_farmer import GhostTowerFarmer
from farmer.pikachu_farmer import PikachuFarmer
from farmer.surf_famer import SurfFarmer
from farmer.victory_road_farmer import VictoryRoadFarmer
from farmer.celadon_farmer import CeladonFarmer
from input_listener.input_listener import InputListener
from radon.Radon import *
from cli.cli import *
from prowatch.PROWatch import *
from protrainer_gui import *


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
        self.prowatch_thread = PROWatch()
        self.prowatch_thread.start()

        """ CLI  """

        # Create the CLI
        self.cli_thread = PROTrainerCLI(name="CLIThread")
        self.cli_thread.start()

        """ FARMER """

        # Create the fishing rod farmer
        self.farmer_thread = FishingRodFarmer(name="FarmerThread",
                                              args=(self,))
        # Farm
        self.farmer_thread.start()
        # Create Radon thread for managing screenshots / OCR
        self.radon_thread = Radon(name="TesseractInteractionThread",
                                  args=(self,))
        self.radon_thread.start()

        """ INPUT """

        # Input listener thread
        self.listener_thread = InputListener(name="InputListenerThread",
                                             args=(self,))
        # Listen for input
        self.listener_thread.start()

    def load_configuration(self):
        file = open("configuration.txt", "r")
        for line in file:
            self.interpret_configuration(line)

    def interpret_configuration(self, line):
        # Check which configuration to set
        if line == "farmer_pause":
            self.farmer_pause = bool(self.get_config_value(line))
        elif line == "radon_pause":
            self.radon_pause = bool(self.get_config_value(line))
        elif line == "catch_pokemon":
            self.catch_pokemon = bool(self.get_config_value(line))
        elif line == "emergency_reset":
            self.emergency_reset = bool(self.get_config_value(line))

    @staticmethod
    def get_config_value(line: str) -> str:
        list_values = line.split(":")
        if len(list_values) == 2:
            value = list_values[1]
            return value
        else:
            raise Exception("Configuration file has incorrect format.")

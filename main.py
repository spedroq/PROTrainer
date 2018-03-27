from farmer.cave_famer import CaveFarmer
from farmer.fishing_rod_farmer import FishingRodFarmer
from farmer.ghost_farmer import GhostTowerFarmer
from farmer.surf_famer import SurfFarmer
from farmer.victory_road_farmer import VictoryRoadFarmer
from input_listener.input_listener import InputListener
from radon.Radon import *
from cli.cli import *
from prowatch.PROWatch import *


def main():
    # Create the PROWatch logger
    prowatch = PROWatch()
    prowatch.start_logging()

    # Create the CLI
    cli = PROTrainerCLI(name="CLIThread")
    cli.start()
    # Create the fishing rod farmer
    farmer_thread = FishingRodFarmer(name="FarmerThread",
                                     args=(prowatch,))
    # Farm
    farmer_thread.start()

    # Input listener thread
    listener_thread = InputListener(name="InputListenerThread",
                                    args=(farmer_thread,cli,prowatch,))
    # Listen for input
    listener_thread.start()

    # Create Radon thread for managing screenshots / OCR
    radon_thread = Radon(name="TesseractInteractionThread",
                         args=(farmer_thread,cli,prowatch,))
    radon_thread.run()


# Start the main function
main()

from farmer.cave_famer import CaveFarmer
from farmer.fishing_rod_farmer import FishingRodFarmer
from farmer.ghost_farmer import GhostTowerFarmer
from farmer.surf_famer import SurfFarmer
from farmer.victory_road_farmer import VictoryRoadFarmer
from input_listener.input_listener import InputListener
from radon.Radon import *
from cli.cli import *

def main():
    # Create the CLI
    cli = PROTrainerCLI(name="CLIThread")
    cli.start()
    # Create the fishing rod farmer
    farmer_thread = VictoryRoadFarmer(name="FarmerThread")
    # Farm
    farmer_thread.start()

    # Input listener thread
    listener_thread = InputListener(name="InputListenerThread",
                                    args=(farmer_thread,cli,))
    # Listen for input
    listener_thread.start()

    # Create Radon thread for managing screenshots / OCR
    radon_thread = Radon(name="TesseractInteractionThread",
                         args=(farmer_thread,cli,))
    radon_thread.run()


# Start the main function
main()

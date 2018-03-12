from farmer.cave_famer import CaveFarmer
from farmer.fishing_rod_farmer import FishingRodFarmer
from farmer.ghost_farmer import GhostTowerFarmer
from farmer.surf_famer import SurfFarmer
from input_listener.input_listener import InputListener


def main():
    # Create the fishing rod farmer
    farmer_thread = FishingRodFarmer(name="FarmerThread")
    # Farm
    farmer_thread.start()

    # Input listener thread
    listener_thread = InputListener(name="InputListenerThread",
                                    args=(farmer_thread,))
    # Listen for input
    listener_thread.start()


# Start the main function
main()

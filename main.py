from farmer.fishing_rod_farmer import FishingRodFarmer
from farmer.ghost_farming import GhostTowerFarmer
from input_listener.input_listener import InputListener


def main():
    # Create the fishing rod farmer
    farmer_thread = GhostTowerFarmer(name="FarmerThread")
    # Farm
    farmer_thread.start()

    # Input listener thread
    listener_thread = InputListener(name="InputListenerThread",
                                    args=(farmer_thread,))
    # Listen for input
    listener_thread.start()


# Start the main function
main()

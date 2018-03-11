from farmer.fishing_rod_farmer import FishingRodFarmer
from inputlistener.inputlistener import InputListener


def main():
    # Create the fishing rod farmer
    fishing_rod_farmer_thread = FishingRodFarmer(name="FarmerThread")
    # Farm
    fishing_rod_farmer_thread.start()

    # Input listener thread
    listener_thread = InputListener(name="InputListenerThread",
                                    args=(fishing_rod_farmer_thread,))
    # Listen for input
    listener_thread.start()


# Start the main function
main()
from move_set.move_set import PROTrainerMoveSequence, PROTrainerMove


class FarmerMode:
    """
    Class FarmerMode that defines the Farmer modes.
    NOTE: Here we define the different move sequences for each farmer mode
    and allow changing between them.
    """

    def __init__(self, control_thread: 'Control'):
        """
        Method to initialize FarmerMode.
        :param control_thread: the control thread so as to access other threads.
        """
        # Set the control thread.
        self.control_thread = control_thread
        # Define the farmer modes to allow
        self.farmer_modes = [
            # Johto
            "GolderRodFarmer",
            # Kanto
            "VictoryRoadFarmer",
            "CaveFarmer",
            "FishingRodFarmer",
            "FuchsiaFishFarmer",
            "GhostTowerFarmer",
            "CeladonFarmer",
            # "PikachuFarmer",
            # "SurfFarmer",
        ]
        # Select the start farmer mode
        self.farmer_mode_index = 0
        self.farmer_mode = self.farmer_modes[self.farmer_mode_index]
        # Set the selected farmer mode
        self.set_farmer_mode()

    def increment_farmer_mode_index(self) -> None:
        """
        Helper method to encapsulate farmer mode index incrementation.
        """
        # Increment the index
        self.farmer_mode_index += 1
        # Wrap around the mode list, otherwise the index will increment towards infinity
        self.farmer_mode_index = self.farmer_mode_index % len(self.farmer_modes)

    def toggle_mode(self) -> None:
        """
        Method to toggle between farmer modes active.
        """
        # Increment the index
        self.increment_farmer_mode_index()
        # Get the new mode
        self.farmer_mode = self.farmer_modes[self.farmer_mode_index]
        # Set the new mode
        self.set_farmer_mode()

    def set_farmer_mode(self) -> None:
        """
        Method to set farmer mode.
        NOTE: This only sets the farmer mode, you will need to change 'self.farmer_mode' to whatever new mode
        before running this if you want to change the current running mode.
        """
        # Init the default_move_set and poke_center_move_set
        default_move_set, poke_center_move_set = None, None
        # Create the correct thread
        if self.farmer_mode == "CaveFarmer":
            default_move_set, poke_center_move_set = self.get_cave_farmer()
        elif self.farmer_mode == "FishingRodFarmer":
            default_move_set, poke_center_move_set = self.get_fishing_rod_farmer()
        elif self.farmer_mode == "FuchsiaFishFarmer":
            default_move_set, poke_center_move_set = self.get_fuchsia_fish_farmer()
        elif self.farmer_mode == "GhostTowerFarmer":
            default_move_set, poke_center_move_set = self.get_ghost_tower_farmer()
        elif self.farmer_mode == "CeladonFarmer":
            default_move_set, poke_center_move_set = self.get_celadon_farmer()
        elif self.farmer_mode == "PikachuFarmer":
            default_move_set, poke_center_move_set = self.get_pikachu_farmer()
        elif self.farmer_mode == "SurfFarmer":
            default_move_set, poke_center_move_set = self.get_surf_farmer()
        elif self.farmer_mode == "VictoryRoadFarmer":
            default_move_set, poke_center_move_set = self.get_victory_road_farmer()
        elif self.farmer_mode == "GolderRodFarmer":
            default_move_set, poke_center_move_set = self.get_golden_rod_farmer()
        else:
            print("Farmer Mode is Not Known.")
        # Print the farmer mode that has been activated
        print("New Farmer Mode: {}".format(self.farmer_mode))
        # Set farmer_threads move sequences
        self.control_thread.farmer_thread.default_move_set = default_move_set
        self.control_thread.farmer_thread.poke_center_move_set = poke_center_move_set
        # Tell farmer_thread to reset (since we just changed the mode)
        self.control_thread.farmer_thread.reset()

    @staticmethod
    def get_cave_farmer() -> (PROTrainerMoveSequence, PROTrainerMoveSequence):
        """
        Static method to create cave farmer move sequences.
        :return: default_move_set and poke_center_move_set as PROTrainerMoveSequence objects.
        """
        # Set the default farm sequence
        default_move_set = PROTrainerMoveSequence("CaveFarmer:default_move_set", [
                PROTrainerMove(["w"], 15, timeout=0.05, random_deviation=0.1),
                PROTrainerMove(["s"], 15, timeout=0.05, random_deviation=0.1),
                PROTrainerMove(["w"], 15, timeout=0.05, random_deviation=0.1),
                PROTrainerMove(["s"], 15, timeout=0.05, random_deviation=0.1),
                PROTrainerMove(["1"], 1, timeout=0.1, random_deviation=0.9)
        ])
        # Set the pokecenter sequence
        poke_center_move_set = PROTrainerMoveSequence("CaveFarmer:poke_center_move_set", [
            PROTrainerMove(["4", "s"], 45, timeout=0.05, random_deviation=0.1),
            PROTrainerMove(["1", " ", "w"], 25, timeout=0.05, random_deviation=0.1),
            PROTrainerMove(["w"], 25, timeout=0.05, random_deviation=0.1)
        ])

        return default_move_set, poke_center_move_set

    @staticmethod
    def get_fishing_rod_farmer() -> (PROTrainerMoveSequence, PROTrainerMoveSequence):
        """
        Static method to create fishing rod farmer move sequences.
        :return: default_move_set and poke_center_move_set as PROTrainerMoveSequence objects.
        """
        # Set the default farm sequence
        default_move_set = PROTrainerMoveSequence("FishingRodFarmer:default_move_set", [
            PROTrainerMove(["1"], 1, timeout=3, random_deviation=1)
        ])
        # Set the pokecenter sequence
        poke_center_move_set = PROTrainerMoveSequence("FishingRodFarmer:poke_center_move_set", [
            PROTrainerMove(["4", "w"], 66, timeout=0.10),
            PROTrainerMove(["1", " ", "s"], 20, timeout=0.10),
            PROTrainerMove(["s"], 120, timeout=0.10)
        ])

        return default_move_set, poke_center_move_set

    @staticmethod
    def get_golden_rod_farmer() -> (PROTrainerMoveSequence, PROTrainerMoveSequence):
        """
        Static method to create golden rod farmer move sequences.
        :return: default_move_set and poke_center_move_set as PROTrainerMoveSequence objects.
        """
        # Set the default farm sequence
        default_move_set = PROTrainerMoveSequence("FishingRodFarmer:default_move_set", [
            PROTrainerMove(["1"], 1, timeout=3, random_deviation=1)
        ])
        # Set the pokecenter sequence
        poke_center_move_set = PROTrainerMoveSequence("FishingRodFarmer:poke_center_move_set", [
            # Out of the route
            PROTrainerMove(["4", "a"], 15, timeout=0.5),
            PROTrainerMove(["w"], 23, timeout=0.3),
            # Wait to load the new area
            PROTrainerMove(["nothing"], 1, timeout=1.5),
            # Go to pokecenter
            PROTrainerMove(["w"], 11, timeout=0.3),
            PROTrainerMove(["a"], 4, timeout=0.3),
            # Into Nurse Joy
            PROTrainerMove(["w"], 40, timeout=0.1),
            PROTrainerMove(["1", " ", "s"], 20, timeout=0.10),
            # Out of the pokecenter
            PROTrainerMove(["s"], 30, timeout=0.10),
            # Onto the route
            PROTrainerMove(["d"], 4, timeout=0.3),
            # Back to farming
            PROTrainerMove(["s"], 100, timeout=0.1),
        ])

        return default_move_set, poke_center_move_set

    @staticmethod
    def get_fuchsia_fish_farmer() -> (PROTrainerMoveSequence, PROTrainerMoveSequence):
        """
        Static method to create fuchsia fish farmer move sequences.
        :return: default_move_set and poke_center_move_set as PROTrainerMoveSequence objects.
        """
        # Set the default farm sequence
        default_move_set = PROTrainerMoveSequence("FuchsiaFishFarmer:default_move_set", [
            # Farm
            PROTrainerMove(["1"], 10, timeout=.75, random_deviation=0.5)
        ])
        # Set the pokecenter sequence
        poke_center_move_set = PROTrainerMoveSequence("FuchsiaFishFarmer:poke_center_move_set", [
            # No PP, bail
            PROTrainerMove(["4"], 60, timeout=0.1),
            # Up to pokecenter
            PROTrainerMove(["w"], 110, timeout=0.10),
            # Right to the pokemon center down one to match it
            PROTrainerMove(["d"], 4, timeout=0.4),
            PROTrainerMove(["s"], 1, timeout=0.4),
            PROTrainerMove(["d"], 4, timeout=0.4),
            # Move to nurse joy and interact
            PROTrainerMove(["w"], 35, timeout=0.10),
            PROTrainerMove(["1", " ", "s"], 15, timeout=0.10),
            PROTrainerMove(["s"], 3, timeout=0.10),
            PROTrainerMove(["nothing"], 1, timeout=1),
            # Bail from the pokemon center
            PROTrainerMove(["s"], 3, timeout=0.25),
            PROTrainerMove(["a"], 7, timeout=0.4),
            PROTrainerMove(["s"], 6, timeout=0.25),
            PROTrainerMove(["nothing"], 1, timeout=1),
            # Back to the left
            PROTrainerMove(["a"], 6, timeout=0.25),
            # Down to the water
            PROTrainerMove(["s"], 20, timeout=0.10),
            PROTrainerMove(["d"], 1, timeout=0.25),
            PROTrainerMove(["s"], 100, timeout=0.10),
        ])

        return default_move_set, poke_center_move_set

    @staticmethod
    def get_ghost_tower_farmer() -> (PROTrainerMoveSequence, PROTrainerMoveSequence):
        """
        Static method to create ghost tower farmer move sequences.
        :return: default_move_set and poke_center_move_set as PROTrainerMoveSequence objects.
        """
        # Set the default farm sequence
        default_move_set = PROTrainerMoveSequence("GhostTowerFarmer:default_move_set", [
            PROTrainerMove(["w"], 15, timeout=0.05, random_deviation=0.1),
            PROTrainerMove(["s"], 15, timeout=0.05, random_deviation=0.1),
            PROTrainerMove(["w"], 15, timeout=0.05, random_deviation=0.1),
            PROTrainerMove(["s"], 15, timeout=0.05, random_deviation=0.1),
            PROTrainerMove([" "], 15, timeout=0.05, random_deviation=0.1),
            PROTrainerMove(["1"], 1, timeout=0.6, random_deviation=0.5)
        ])
        # Set the pokecenter sequence
        poke_center_move_set = PROTrainerMoveSequence("GhostTowerFarmer:poke_center_move_set", [
            PROTrainerMove(["4", "w"], 45, timeout=0.05, random_deviation=0.1),
            PROTrainerMove(["4", "d"], 25, timeout=0.05, random_deviation=0.1),
            PROTrainerMove(["1", " ", "a"], 25, timeout=0.05, random_deviation=0.1),
            PROTrainerMove(["a"], 25, timeout=0.05, random_deviation=0.1)
        ])

        return default_move_set, poke_center_move_set

    @staticmethod
    def get_celadon_farmer() -> (PROTrainerMoveSequence, PROTrainerMoveSequence):
        """
        Static method to create celadon farmer move sequences.
        :return: default_move_set and poke_center_move_set as PROTrainerMoveSequence objects.
        """
        # Set the default farm sequence
        default_move_set = PROTrainerMoveSequence("CeladonFarmer:default_move_set", [
            PROTrainerMove(["d"], 15, timeout=0.05, random_deviation=0.1),
            PROTrainerMove(["a"], 15, timeout=0.05, random_deviation=0.1),
            PROTrainerMove(["1"], 10, timeout=.75, random_deviation=0.5)
        ])
        # Set the pokecenter sequence
        poke_center_move_set = PROTrainerMoveSequence("CeladonFarmer:poke_center_move_set", [
            # No PP, bail, reach the left of the grass
            PROTrainerMove(["4", "a"], 50, timeout=0.1),
            # Down from the grass
            PROTrainerMove(["s"], 1, timeout=0.10),
            PROTrainerMove(["a", "s"], 2, timeout=0.15),
            # Left to near the pokemon center
            PROTrainerMove(["a"], 30, timeout=0.25),
            # Navigate into the pokemon center
            PROTrainerMove(["w"], 1, timeout=0.25),
            PROTrainerMove(["w"], 1, timeout=0.25),
            PROTrainerMove(["w"], 1, timeout=0.25),
            PROTrainerMove(["w"], 1, timeout=0.25),
            PROTrainerMove(["w"], 1, timeout=0.25),
            PROTrainerMove(["a"], 1, timeout=0.25),
            PROTrainerMove(["a"], 1, timeout=0.25),
            PROTrainerMove(["w"], 1, timeout=0.25),
            # Move to nurse joy and interact
            PROTrainerMove(["w"], 35, timeout=0.10),
            PROTrainerMove(["1", " ", "s"], 25, timeout=0.10),
            # Bail from the pokemon center
            PROTrainerMove(["s"], 8, timeout=0.10),
            # Back to the right
            PROTrainerMove(["d"], 25, timeout=0.25),
            # Up to the wall
            PROTrainerMove(["w"], 1, timeout=0.25),
            PROTrainerMove(["w"], 1, timeout=0.25),
            PROTrainerMove(["w"], 1, timeout=0.25),
            PROTrainerMove(["w"], 1, timeout=0.25),
            PROTrainerMove(["w"], 1, timeout=0.25),
            PROTrainerMove(["w"], 1, timeout=0.25),
            PROTrainerMove(["w"], 1, timeout=0.25),
            PROTrainerMove(["w"], 1, timeout=0.25),
            # Into the grass
            PROTrainerMove(["d"], 12, timeout=0.25),
            PROTrainerMove(["w"], 1, timeout=0.5),
        ])

        return default_move_set, poke_center_move_set

    @staticmethod
    def get_pikachu_farmer() -> (PROTrainerMoveSequence, PROTrainerMoveSequence):
        """
        Static method to create pikachu farmer move sequences.
        :return: default_move_set and poke_center_move_set as PROTrainerMoveSequence objects.
        """
        # Set the default farm sequence
        default_move_set = PROTrainerMoveSequence("PikachuFarmer:default_move_set", [
            PROTrainerMove(["d"], 5, timeout=0.05, random_deviation=0.1),
            PROTrainerMove(["a"], 5, timeout=0.05, random_deviation=0.1),
            PROTrainerMove(["d"], 5, timeout=0.05, random_deviation=0.1),
            PROTrainerMove(["a"], 5, timeout=0.05, random_deviation=0.1),
            PROTrainerMove(["1"], 1, timeout=0.6, random_deviation=0.5)
        ])
        # Set the pokecenter sequence
        poke_center_move_set = PROTrainerMoveSequence("PikachuFarmer:poke_center_move_set", [
            # Go to the tunnel
            PROTrainerMove(["4", "a"], 25, timeout=0.25),
            PROTrainerMove(["4", "w"], 25, timeout=0.25),
            PROTrainerMove(["4", "d"], 1, timeout=0.5),
            PROTrainerMove(["w"], 2, timeout=0.5),
            PROTrainerMove(["nothing"], 1, timeout=2, random_deviation=2),
            # Through the tunnel
            PROTrainerMove(["w"], 9, timeout=0.5),
            PROTrainerMove(["nothing"], 1, timeout=2, random_deviation=2),
            # Up to the next transition screen
            PROTrainerMove(["w"], 13, timeout=0.5),
            PROTrainerMove(["d"], 12, timeout=0.5),
            PROTrainerMove(["w"], 9, timeout=0.5),
            PROTrainerMove(["d"], 5, timeout=0.5),
            PROTrainerMove(["w"], 19, timeout=0.5),
            PROTrainerMove(["nothing"], 1, timeout=2, random_deviation=2),
            # Through the town and into the pokecenter
            PROTrainerMove(["w"], 11, timeout=0.5),
            PROTrainerMove(["d"], 8, timeout=0.5),
            PROTrainerMove(["w"], 9, timeout=0.5),
            PROTrainerMove(["nothing"], 1, timeout=2, random_deviation=2),
            # In the pokecenter
            PROTrainerMove(["w"], 7, timeout=0.5),
            # Talk to nurse Joy
            PROTrainerMove(["w", " "], 10, timeout=0.5),
            PROTrainerMove(["1", " ", "s"], 5, timeout=0.5),
            PROTrainerMove(["s"], 5, timeout=0.5),
            # To the route
            PROTrainerMove(["s"], 8, timeout=0.5),
            PROTrainerMove(["a"], 9, timeout=0.5),
            PROTrainerMove(["s"], 11, timeout=0.5),
            PROTrainerMove(["nothing"], 1, timeout=2, random_deviation=2),
            # Through the route to the tunnel
            PROTrainerMove(["s"], 18, timeout=0.5),
            PROTrainerMove(["a"], 4, timeout=0.5),
            PROTrainerMove(["s"], 9, timeout=0.5),
            PROTrainerMove(["a"], 12, timeout=0.5),
            PROTrainerMove(["s"], 15, timeout=0.5),
            PROTrainerMove(["nothing"], 1, timeout=2, random_deviation=2),
            # Through the tunnel
            PROTrainerMove(["s"], 9, timeout=0.5),
            PROTrainerMove(["nothing"], 1, timeout=2, random_deviation=2),
            # Back to farming spot
        ])

        return default_move_set, poke_center_move_set

    @staticmethod
    def get_surf_farmer() -> (PROTrainerMoveSequence, PROTrainerMoveSequence):
        """
        Static method to create surf farmer move sequences.
        :return: default_move_set and poke_center_move_set as PROTrainerMoveSequence objects.
        """
        # Set the default farm sequence
        default_move_set = PROTrainerMoveSequence("SurfFarmer:default_move_set", [
            PROTrainerMove(["s", "1", "mouse_left%1071%580"], 12),
            PROTrainerMove(["w", "1"], 4)
        ])
        # Set the pokecenter sequence
        poke_center_move_set = PROTrainerMoveSequence("SurfFarmer:poke_center_move_set", [
            PROTrainerMove(["4", "w"], 30),
            PROTrainerMove(["4", "w", " "], 15),
            PROTrainerMove(["1", " ", "s"], 15),
            PROTrainerMove(["1", " ", "s", "mouse_left%1071%580"], 15)
        ])

        return default_move_set, poke_center_move_set

    @staticmethod
    def get_victory_road_farmer() -> (PROTrainerMoveSequence, PROTrainerMoveSequence):
        """
        Static method to create victory road farmer move sequences.
        :return: default_move_set and poke_center_move_set as PROTrainerMoveSequence objects.
        """
        # Set the default farm sequence
        poke_center_move_set = default_move_set = PROTrainerMoveSequence("VictoryRoadFarmer:default_move_set", [
            PROTrainerMove(["w"], 15, timeout=0.05, random_deviation=0.1),
            PROTrainerMove(["s"], 15, timeout=0.05, random_deviation=0.1),
            PROTrainerMove(["w"], 15, timeout=0.05, random_deviation=0.1),
            PROTrainerMove(["s"], 15, timeout=0.05, random_deviation=0.1),
            PROTrainerMove(["1"], 1, timeout=0.5, random_deviation=0.5),
        ])
        # Set the pokecenter sequence
        #poke_center_move_set =
        NONE = PROTrainerMoveSequence("VictoryRoadFarmer:poke_center_move_set", [
            # Get out of the cave
            PROTrainerMove(["w", "4"], 20, 0.1),
            # Walk out
            PROTrainerMove(["a", "4"], 1, 0.1),
            PROTrainerMove(["w", "4"], 1, 0.1),
            # To Pokecenter
            PROTrainerMove(["w", "4"], 2, 0.1),
            PROTrainerMove(["d"], 4, 0.2),
            PROTrainerMove(["w"], 20, 0.2),
            PROTrainerMove(["d"], 9, 0.2),
            PROTrainerMove(["w"], 2, 0.2),
            # In Pokecenter
            PROTrainerMove(["w"], 4, 0.2),
            PROTrainerMove(["a"], 6, 0.2),
            # Nurse Joy
            PROTrainerMove(["w", " "], 10, 0.20),
            PROTrainerMove(["1", " ", "s"], 10, 0.2),
            # Get out of the Pokecenter
            PROTrainerMove(["d"], 10, 0.2),
            PROTrainerMove(["s"], 10, 0.2),
            PROTrainerMove(["a"], 12, 0.2),
            # Into the cave
            PROTrainerMove(["s", "1"], 20, 1),
            PROTrainerMove(["d", "1"], 20, 1)
        ])

        return default_move_set, poke_center_move_set


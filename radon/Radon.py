#   
#                            .o8                        
#                           "888                        
#   oooo d8b  .oooo.    .oooo888   .ooooo.  ooo. .oo.   
#   `888""8P `P  )88b  d88' `888  d88' `88b `888P"Y88b  
#    888      .oP"888  888   888  888   888  888   888  
#    888     d8(  888  888   888  888   888  888   888  
#   d888b    `Y888""8o `Y8bod88P" `Y8bod8P' o888o o888o 
#
#
#   R A D O N
#   Image analysis for PRO (Pokemon Revolution Online) using Tesseract.
#

from radon.pytesseract.pytesser import *
from prowatch.PROWatch import *
#from pyautogui import press, typewrite, hotkey
from PIL import ImageGrab, Image
import sys
import threading
import time
from random import shuffle
import datetime

exitFlag = 0
current_key = "1"


#
# R A D O N
# Radon
#
# A class to handle optical character recognition using Google's
# tesseract library.
#
# Analysis functionality is also handled here.
#
# Input is a screenshot taken from the OS.
#
class Radon(threading.Thread):
    radon_timer_a = None
    radon_timer_b = None
    colours = {
        #"button_green": (),
        "button_login_yellow": (159,160,33,), # PASS
        "button_login_red": (152,29,42,), # PASS
        "button_login_blue": (15,119,167,), # PASS
        "button_learn_move_red": (158,48,54,), # PASS
        "button_learn_move_blue": (42,117,196,), # PASS
        "button_learn_move_confirm_green": (24,200,1,),
        "button_learn_move_confirm_red": (200,1,1,),
        "button_accept_green": (33,165,17,), # ~
        "button_accept_red": (202,4,4,), # PASS
        "button_close_private_message": (186,186,186,), # 
        "button_pokeball_colour": (255,148,58,), # 
        "button_pwo_login_green_light": (136,184,91,),
        "button_pwo_login_blue": (100,182,160,),
        "button_pwo_login_green_dark": (95,184,118,),
        #"button_close_private_message": (71,71,71,), # 
        #"button_close_private_message": (71,71,71,), # 
        #"button_close_private_message": (17,17,17,), # 
    }
    grid_width = 8
    grid_height = 8
    debug_is_printing_text = False
    last_poke_save_time = time.time()
    last_poke_name = ""
    
    prowatch = None
    farmer = None

    TOP_LEFT_CORNER = (-1,-1,)
    BOTTOM_RIGHT_CORNER = (-1,-1,)

    with open("radon/splash.txt") as r:
        print(r.read())

    def mainline(self, input_screenshot=None):
        while True:
            self.start_timer()
            # Read the text from an screenshot taken right now
            #if screenshot == None:
            screenshot = self.get_screenshot_pil_image()
            if input_screenshot != None:
                screenshot = input_screenshot
            text = self.read_text_from_pil_image(screenshot)
            # Ok, cool we have the text, let's check for colours
            radon_status = self.get_radon_status_from_text(text)
            #   We need to login            
            if radon_status.get("code") == 10:
                matching_tiles = []

                matching_tiles = self.get_tiles_matching_colour_from_pil_image_within_tolerance(
                    screenshot, self.colours["button_login_yellow"], 0.25
                )
                #print("MATCHES: {}".format(len(matching_tiles)))
                #
                #   We should only select tiles below the center line
                max_tile_y = 0
                min_tile_y = 99999
                for tile in matching_tiles:
                    #print(tile)
                    if int(tile["info"]["y"]) > max_tile_y:
                        max_tile_y = int(tile["info"]["y"])
                    if int(tile["info"]["y"]) < min_tile_y:
                        min_tile_y = int(tile["info"]["y"])
                #
                #   Select a mid point, if the tiles are above it, omit them
                
                minimum_valid_y_value = max_tile_y / 2
                #print("MIN: {} | MAX: {} | THRESHOLD: {}".format(
                #    min_tile_y, max_tile_y, minimum_valid_y_value
                #))
                valid_tiles = []
                for tile in matching_tiles:
                    if tile["info"]["y"] >= minimum_valid_y_value:
                        valid_tiles.append(tile)

                matching_tiles = valid_tiles
                #print("FILTERED: {}".format(len(matching_tiles)))
                shuffle(matching_tiles)
                radon_status["tiles"] = matching_tiles

            #   This pokemon needs to evolve
            elif radon_status.get("code") == 21:
                self.grid_width = 6
                self.grid_height = 6
                matching_tiles = []
                matching_tiles = self.get_tiles_matching_colour_from_pil_image_within_tolerance(
                    screenshot, self.colours["button_accept_red"], 0.75
                )
                shuffle(matching_tiles)
                radon_status["tiles"] = matching_tiles
                self.grid_width = 8
                self.grid_height = 8

            #   This pokemon needs to learn a move
            elif radon_status.get("code") == 22:
                matching_tiles = []
                matching_tiles = self.get_tiles_matching_colour_from_pil_image_within_tolerance(
                    screenshot, self.colours["button_learn_move_red"], 0.15
                )
                shuffle(matching_tiles)
                radon_status["tiles"] = matching_tiles

            #   We need to close this private message
            elif radon_status.get("code") == 12:
                matching_tiles = []
                self.grid_width = 6
                self.grid_height = 6
                matching_tiles = self.get_tiles_matching_colour_from_pil_image_within_tolerance(
                    screenshot, self.colours["button_close_private_message"], 0.00
                )
                #
                #   Fix the x co-ord by 26px
                final_tiles = []
                for tile in matching_tiles:
                    if int(tile["info"]["y_center"]) > 150 and int(tile["info"]["y_center"]) < 650:
                        tile["info"]["x_center"] = int(tile["info"]["x_center"]) + 26
                        final_tiles.append(tile)
                radon_status["tiles"] = final_tiles
                self.grid_width = 8
                self.grid_height = 8

            # We need to use a pokeball
            elif radon_status.get("code") == 13:
                matching_tiles = []
                self.grid_width = 6
                self.grid_height = 6
                matching_tiles = self.get_tiles_matching_colour_from_pil_image_within_tolerance(
                    screenshot, self.colours["button_pokeball_colour"], 0.00
                )
                shuffle(matching_tiles)
                for tile in matching_tiles:
                    tile["info"]["x_center"] = int(tile["info"]["x_center"]) + 75
                radon_status["tiles"] = matching_tiles
                self.grid_width = 8
                self.grid_height = 8


            # We need to confirm this selection
            elif radon_status.get("code") == 11:
                self.grid_width = 6
                self.grid_height = 6
                matching_tiles = []
                matching_tiles = self.get_tiles_matching_colour_from_pil_image_within_tolerance(
                    screenshot, self.colours["button_learn_move_confirm_green"], 0.75
                )
                #print(matching_tiles)
                shuffle(matching_tiles)
                radon_status["tiles"] = matching_tiles
                self.grid_width = 8
                self.grid_height = 8


            #
            #   Start PWO
            
            if radon_status.get("code") == 110:
                #
                #   P W O  L O G I N
                matching_tiles = []
                self.grid_width = 4
                self.grid_height = 5
                matching_tiles = self.get_tiles_matching_colour_from_pil_image_within_tolerance(
                    screenshot, self.colours["button_pwo_login_green_light"], 0.03
                )
                shuffle(matching_tiles)
                max_tile_y = 0
                min_tile_y = 99999
                for tile in matching_tiles:
                    #print(tile)
                    if int(tile["info"]["y"]) > max_tile_y:
                        max_tile_y = int(tile["info"]["y"])
                    if int(tile["info"]["y"]) < min_tile_y:
                        min_tile_y = int(tile["info"]["y"])
                #
                #   Select a mid point, if the tiles are above it, omit them
                
                minimum_valid_y_value = max_tile_y / 2
                #print("MIN: {} | MAX: {} | THRESHOLD: {}".format(
                #    min_tile_y, max_tile_y, minimum_valid_y_value
                #))
                valid_tiles = []
                for tile in matching_tiles:
                    if tile["info"]["y"] >= minimum_valid_y_value:
                        valid_tiles.append(tile)

                matching_tiles = valid_tiles
                radon_status["tiles"] = matching_tiles
                self.grid_width = 8
                self.grid_height = 8
            #   End PWO
            #   


            #
            #   Let's fix the status string to put the time in there
            radon_status = self.insert_process_time_into_radon_status(radon_status)

            #
            #   Development
            if self.farmer:
                #print(text)
                self.farmer.deliver_radon_status(radon_status)
                    # Metrics
                self.end_timer()
                self.cli.input_string_last_radon_time = str(self.get_processing_time_in_seconds())
                self.cli.input_string_last_radon_status = str(radon_status["code"])
                self.cli.input_string_last_radon_info = radon_status["status"]
                self.prowatch.append_write_to_log(
                    radon_status["code"],
                    radon_status["status"],
                    self.get_processing_time_in_seconds(),
                    "None"
                )
                #
                #   Wipe the memory of the current screenshot
                screenshot = None
            else:
                #
                #   Test Framework
                return [radon_status, text]
                break
                

    # Initialise
    def run(self):
        #self.prowatch.start_logging()
        print("R A D O N  I S  S T A R T I N G  U P . . . ")
        self.farmer = self._args[0]
        self.cli = self._args[1]
        self.prowatch = self._args[2]
        self.mainline()
        #print("Radon completed in [{}s]".format(self.get_processing_time_in_seconds()))


                

    #
    #    M E T R I C S
    #    Metrics
    #
    #    Timers for timing processing of function
    def start_timer(self):
        self.radon_timer_a = time.time()
        #print(self.radon_timer_a)
    def end_timer(self):
        self.radon_timer_b = time.time()
        #print(self.radon_timer_b)
    def get_processing_time_in_seconds(self):
        a = self.radon_timer_a
        b = self.radon_timer_b
        time_difference = b - a
        return round(time_difference, 1)
        #round(time_difference, 3)


    #
    # A function to define the center point of an image
    def get_center_point_of_tile(self, tile):
        center = (
            int(tile["info"]["x"] / 2),
            int(tile["info"]["y"] / 2),
        )
        return center

    def get_radon_status_from_text_for_pwo(self, text, check_text):
        radon_status = {
            "code": 0,
            "status": "0: [pwo] radon could not gather any useful information during this analysis of text"
        }

        #
        #   Incoming private message from another player
        #   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =
        login_terms = [
            ("P 0 K 6 M C N", text,),
            ("POKeMON", text,),
            ("p o k e m o n", check_text),
        ]
        for term in login_terms:
            if term[0] in term[1]:
                radon_status = {
                    "code": 110,
                    "status": "110: we need to login"
                }

        return radon_status


    #
    #   A function to return a Radon Status
    def get_radon_status_from_text(self, text):
        #
        #   S T A T U S  D E F I N I T O N S
        #
        #   0:      Unknown
        #   10-19:  Game/Input related
        #   20-29:  Relating to Pokemon
        #   30-39:  
        #   40-49:  
        #   50-59:  
        #   60-69:  
        #   70-79:  
        #   80-89:  
        #   90-99:  
        #
        #
        if self.debug_is_printing_text:
            print("\n\n{}\n\n".format(text))
        radon_status = {
           "code": 0,
           "status": "0: radon could not gather any useful information during this analysis of text"
        }
        #
        #   Exact matches only
        check_text = text.lower()

        #
        #   PWO CODE
        pwo_enabled = False
        if pwo_enabled:
            pwo_radon_status = self.get_radon_status_from_text_for_pwo(text, check_text)
            return pwo_radon_status

        #   END PWO CODE
        #

        #
        #   Incoming private message from another player
        #   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =
        pm_terms = [
            (" PM", text,),
            ("chat", check_text,)
        ]
        for term in pm_terms:
            if term[0] in term[1]:
                radon_status = {
                    "code": 12,
                    "status": "12: some rando is trying to private message us"
                }

        #
        #   We need to login
        #   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =
        login_terms = [
            ("login red", check_text,),
            ("login blue", check_text,),
            ("login yellow", check_text,)
        ]
        for term in login_terms:
            if term[0] in term[1]:
                radon_status = {
                   "code": 10,
                   "status": "10: warning, we are not logged in"
                } 

        #
        #   Our pokemon is trying to learn a new move
        #   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =
        learn_move_terms = [
            ("this move", check_text,),
            ("not learn", check_text,),
            ("forget ", check_text,),
            ("learn move", check_text,)
        ]
        for term in learn_move_terms:
            if term[0] in term[1]:
                radon_status = {
                    "code": 22,
                    "status": "22: our pokemon is trying to learn a move"
                }
 
        #
        #   Currently we are probably in the battle scene
        #   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =
        battle_scene_menu_terms = [
            ("wait", check_text,),
            ("please", check_text,),
        ]
        for term in battle_scene_menu_terms:
            if term[0] in term[1]:
                radon_status = {
                    "code": 14,
                    "status": "14: we are probably in a battle"
                }

        #
        #   The menu for selecting to throw a pokeball is open
        #   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =
        pokeball_menu_terms = [
            ("chuuseltem", check_text,),
            ("(house Item", check_text,),
            ("choose item", check_text,),
            ("pokeball", check_text,),
            (" Item", text,)
        ]
        for term in pokeball_menu_terms:
            if term[0] in term[1]:
                radon_status = {
                    "code": 13,
                    "status": "13: we are trying to catch a pokemon using a pokeball"
                }


        #
        #   Our pokemon is trying to evolve to its next stage
        #   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =
        evolve_menu_terms = [
            ("yw wan", check_text,),
            ("evolving", check_text,),
            ("no yes", check_text,),
            ("no ves", check_text,),
            ("evolv", check_text,),
            ("ynur", check_text,)
        ]
        for term in evolve_menu_terms:
            if term[0] in term[1]:
                radon_status = {
                    "code": 21,
                    "status": "21: our pokemon wants to evolve"
                }

        #
        #   We need to confirm a "Cancel"/"Ok" input on the screen
        #   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =
        confirm_selection_menu_terms = [
            ("cancel ok", check_text,),
            ("cancel", check_text,),
        ]
        for term in confirm_selection_menu_terms:
            if term[0] in term[1]:
                radon_status = {
                    "code": 11,
                    "status": "11: we need to confirm our selection"
                }

        #
        #   Our Pokemon has run out of PP
        #   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =
        pp_check_terms = [
            ("left!!", check_text,),
            ("has no", check_text,),
        ]
        for term in pp_check_terms:
            if term[0] in term[1]:
                radon_status = {
                    "code": 20,
                    "status": "20: our pokemon has run out of pp for this move"
                }

        #
        #   Check Radon to see if we are fighint a wild pokemon, verify it has a valid name
        #   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =
        if "wild" in check_text or "VS" in text or "vS=" in text:
            #
            #   Don't check for this if we need to catch [13] or learn move [22]
            if radon_status["code"] != 22 and radon_status["code"] != 13 and radon_status["code"] != 20:
                #
                #   Set default "unknown" poke status
                radon_status = {
                    "code": 28,
                    "status": "28: an unknown wild pokemon is fighting us"
                }
                #
                #   Check to see if we are fighting an NPC
                #   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =   -   =
                trainer_battle_terms = [
                    ("Gamer", text,),
                    ("Maniac", text,),
                ]
                for term in trainer_battle_terms:
                    if term[0] in term[1]:
                        radon_status = {
                            "code": 27,
                            "status": "27: we are probably in a battle with an npc"
                        }
                #
                #   Manual fixes for pokemon names (tesseract errors)
                error_list = [
                    ("magnemmte", "magnemite",),
                    ("pmdgey", "pidgey",),
                    ("ratmcate", "raticate",),
                    ("ratmzate", "raticate",),
                    ("taterpme", "bellsprout",),
                    ("x=k=====", "kakuna",),
                    ("persman", "persian",)
                ]
                for error in error_list:
                    if error[0] in check_text:
                        check_text = check_text.replace(error[0], error[1])
                #
                #   Set our status, if it's 100, it's still unknown
                pokemon_radon_status = self.search_radon_text_for_pokemon_name(check_text)
                #print(radon_status["code"])
                #
                #   If the pokemon was valid and we are not in trainer battle
                if pokemon_radon_status["code"] != 100 and radon_status["code"] != 27:
                    radon_status = pokemon_radon_status

        if radon_status.get("tiles"):
            print(radon_status)

        #
        #   If Debug, print
        if self.debug_is_printing_text:
            print(radon_status)
        return radon_status

    #
    #   A function to insert the process time into a status string
    def insert_process_time_into_radon_status(self, radon_status):
        parts = radon_status["status"].split(" ")
        updated_status_string = ""
        i = 0
        for part in parts:
            updated_status_string += part + " "
            if i == 0:
                self.end_timer()
                updated_status_string += "[{}] ".format(
                    self.get_processing_time_in_seconds()
                )
            i += 1
        #print(updated_status_string)
        radon_status["status"] = updated_status_string
        return radon_status

    #
    #   A function to check and see if there is a pokemon present in radon text
    def search_radon_text_for_pokemon_name(self, check_text):
        #
        #   Output status (temporary)
        radon_status = {
            "code": 100,
            "status": "100: this is an empty status from an initialised variable"
        }
        pokemands = []
        poke_file_data = ""
        with open("pokemon.txt", "r") as pokefile:
            poke_file_data = pokefile.read()
        for poke in poke_file_data.split("\n"):
            pokemands.append(poke)
        #
        #   Run a check here
        status_string = ""
        is_found = False
        for line in check_text.split("\n"):
            for pokemand in pokemands:
                if pokemand.lower() in line.lower() and pokemand != "mew" and "we are fighting a" not in line and " go " not in line.lower():
                    print(line)
                    try:
                        self.farmer.last_poke_name = pokemand
                    except:
                        pass
                    status_string = datetime.datetime.now().strftime("[%y-%m-%d-%H-%M-%S]\t")
                    status_string += "29\t29: we are fighting a pokemon\t"
                    fixed_typed_pokemand = ""
                    for c in pokemand:
                        fixed_typed_pokemand += c + ":"
                    status_string += str(pokemand) + "\n"
                    radon_status = {
                        "code": 29,
                        "status": "29: we are fighting a pokemon: {}".format(fixed_typed_pokemand)
                    }
                    break
                        
        if status_string != "":
            with open("seenpokemon.txt", "a") as seen_pokefile:
                if time.time() - self.last_poke_save_time > 15:
                    seen_pokefile.write(status_string)
                    self.last_poke_save_time = time.time()

        return radon_status


    #
    #    A function to count the number of tiles that match in colour
    def get_tiles_matching_colour_from_pil_image_within_tolerance(self, pil_image, colour_to_find, tolerance):
        pil_tiles = self.get_radon_image_objects_from_pil_image(pil_image)
        #
        #    Colour analysis
        #self.start_timer()
        matching_tiles = 0
        matched_tiles = []
        for tile in pil_tiles:
            colour_analysis_results = self.colour_analysis_for_given_colour(
                tile["image"], colour_to_find, tolerance)
            if colour_analysis_results["overall_analysis"]:
                """
                print("\tMATCHING TILE [{}px x {}px]: x: {}, y: {}".format(
                    grid_width, grid_height, tile["info"]["x"], 
                    tile["info"]["y"]
                ))
                """
                matching_tiles += 1
                matched_tiles.append(tile)
        return matched_tiles


    #
    #    I M A G E S
    #    Images
    #
    #    Return a screenshot from the current system as a PIL Image
    def get_screenshot_pil_image(self):
        #
        #    See import PIL
        screenshot = ImageGrab.grab()
        #
        #   Ok, so here we can cut it down to size if the user gave us the window size
        if self.TOP_LEFT_CORNER != (-1,-1,) and self.BOTTOM_RIGHT_CORNER != (-1,-1,):
            #
            #   Crop this image
            a = self.TOP_LEFT_CORNER
            b = (self.BOTTOM_RIGHT_CORNER[0], self.TOP_LEFT_CORNER[1])
            c = (self.TOP_LEFT_CORNER[0], self.BOTTOM_RIGHT_CORNER[1])
            d = self.BOTTOM_RIGHT_CORNER
            box = (
                self.TOP_LEFT_CORNER[0], self.TOP_LEFT_CORNER[1],
                self.BOTTOM_RIGHT_CORNER[0], self.BOTTOM_RIGHT_CORNER[1]
            )
            screenshot = screenshot.crop(box)
        return screenshot
    #
    #    Return a list of RadonImage objects
    def get_radon_image_objects_from_pil_image(self, pil_image):
        #
        #    Read and store the input image information
        origin_width, origin_height = pil_image.size
        #
        #    Define grid
        grid_width = self.grid_width
        grid_height = self.grid_height
        square_horizontal = int(origin_width / grid_width)
        square_vertical = int(origin_height / grid_height)
        total_squares = square_vertical * square_horizontal
        #print("G R I D  @  {}x{}px  =  {}x{}".format(grid_width,grid_height, square_vertical, square_horizontal))
        #
        #    Using this grid, create the images sections we need and return them
        x,y = 0,0


        tiles = []
        for current_grid_tile in range(0, total_squares):
            tile_data = {
                "x": x,
                "y": y,
                "x_center": int(x + (grid_width / 2)),
                "y_center": int(y + (grid_height / 2)),
                "coordinates": (x,y,x+grid_width,y+grid_height,)
            }
            #
            #    Now that we have the information about the tile_data, get the image for this tile
            #    by cutting it from our source image
            tile_image = pil_image.crop(tile_data["coordinates"])
            #
            #    Convert this into RGB
            tile_image_rgb = tile_image.convert('RGB')
            #
            #    Store this as an output object
            tile = {
                "info": tile_data,
                "image": tile_image_rgb
            }
            #   tile = {
            #       "info": {
            #           "x":0,
            #           "y":0,
            #           "coordinates": (0,0), (1,1)          
            #       },
            #       "image": pil_image
            #   } 
            #
            #    Save to our output array
            #
            #   If we have modified the size of our Radon screenshot, update it here
            if self.TOP_LEFT_CORNER != (-1,-1,) and self.BOTTOM_RIGHT_CORNER != (-1,-1,):
                #
                #   Modify the co-ordinates back to the real PC
                alt_x = int(tile["info"]["x"]) + self.TOP_LEFT_CORNER[0]
                alt_y = int(tile["info"]["y"]) + self.TOP_LEFT_CORNER[1]
                tile_data = {
                    "x": alt_x,
                    "y": alt_y,
                    "x_center": int(alt_x + (grid_width / 2)),
                    "y_center": int(alt_y + (grid_height / 2)),
                    "coordinates": (alt_x,alt_y,alt_x+grid_width,alt_y+grid_height,)
                }
                tile["info"] = tile_data
            tiles.append(tile)
            #
            #    Iterate through our grid, updating our co-ordinated each time
            x += grid_width
            if x > origin_width:
                x = 0
                if y > origin_height:
                    y = 0
                else:
                    y += grid_height

        return tiles

    #
    #    A function to handle colour analysis
    # Tolerance here is a percentage representated as a decimal
    def colour_analysis_for_given_colour(self, pil_image_rgb, search_colour=(255,255,255,), tolerance=0.1):
        #
        #    Ok, so let's adapt our search_colour for tolerance
        toleranced_search_colour_max = (
            int(search_colour[0] * (tolerance + 1)), 
            int(search_colour[1] * (tolerance + 1)), 
            int(search_colour[2] * (tolerance + 1)),)
        toleranced_search_colour_min = (
            int(search_colour[0] / (tolerance + 1)), 
            int(search_colour[1] / (tolerance + 1)), 
            int(search_colour[2] / (tolerance + 1)),)
        #
        #    Quick checks, if bigger than 255, fix this
        if toleranced_search_colour_max[0] > 255:
            toleranced_search_colour_max = (255, 
                toleranced_search_colour_max[1], 
                toleranced_search_colour_max[2])
        if toleranced_search_colour_max[1] > 255:
            toleranced_search_colour_max = (toleranced_search_colour_max[0], 
                255, 
                toleranced_search_colour_max[2])
        if toleranced_search_colour_max[2] > 255:
            toleranced_search_colour_max = (toleranced_search_colour_max[0], 
                toleranced_search_colour_max[1], 
                255)
        #
        #    Ok, so now let's look at the center pixel
        x_width, y_height = pil_image_rgb.size
        #
        #    What colour is this pixel?
        r, g, b = pil_image_rgb.getpixel(
            (int(x_width / 2), int(y_height / 2))
        )
        #
        #    Analyse this colour, if it matches each of our inputs - we are valid
        is_valid_red, is_valid_blue, is_valid_green = False,False,False
        if r >= toleranced_search_colour_min[0] and r <= toleranced_search_colour_max[0]:
            is_valid_red = True
        if g >= toleranced_search_colour_min[1] and g <= toleranced_search_colour_max[1]:
            is_valid_green = True
        if b >= toleranced_search_colour_min[2] and b <= toleranced_search_colour_max[2]:
            is_valid_blue = True        
        #
        #    Return our values
        overall_analysis = False
        if is_valid_red and is_valid_green and is_valid_blue:
            overall_analysis = True
        analysis = {
            "overall_analysis": overall_analysis,
            "r_analysis": is_valid_red,
            "g_analysis": is_valid_green,
            "b_analysis": is_valid_blue
        }
        return analysis


    #
    #    O C R
    #    Optical Character Recognition
    #
    #    Using Google's Tesseract, read the text from an PIL image
    def read_text_from_pil_image(self, pil_image):
        text = ""
        #
        #    Use Google's Tesseract to read that image, see import pytesseract.pytesser
        text = image_to_string(pil_image)

        return text





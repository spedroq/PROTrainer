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

    # Initialise
    def run(self):
        #self.prowatch.start_logging()
        while True:
            self.start_timer()
            self.farmer = self._args[0]
            self.cli = self._args[1]
            self.prowatch = self._args[2]
            # Read the text from an screenshot taken right now
            screenshot = self.get_screenshot_pil_image()
            text = self.read_text_from_pil_image(screenshot)
            # Ok, cool we have the text, let's check for colours
            radon_status = self.get_radon_status_from_text(text)
            # Is it a tile delivery?
            is_tile_delivery = False

            #   We need to login            
            if radon_status.get("code") == 10:
                matching_tiles = []
                matching_tiles = self.get_tiles_matching_colour_from_pil_image_within_tolerance(
                    screenshot, self.colours["button_login_yellow"], 0.25
                )
                shuffle(matching_tiles)
                radon_status["tiles"] = matching_tiles
                is_tile_delivery = True
                self.farmer.deliver_radon_status(radon_status)

            #   This pokemon needs to evolve
            elif radon_status.get("code") == 21:
                matching_tiles = []
                matching_tiles = self.get_tiles_matching_colour_from_pil_image_within_tolerance(
                    screenshot, self.colours["button_accept_red"], 0.33
                )
                shuffle(matching_tiles)
                radon_status["tiles"] = matching_tiles
                is_tile_delivery = True
                self.farmer.deliver_radon_status(radon_status)

            #   This pokemon needs to learn a move
            elif radon_status.get("code") == 22:
                matching_tiles = []
                matching_tiles = self.get_tiles_matching_colour_from_pil_image_within_tolerance(
                    screenshot, self.colours["button_learn_move_red"], 0.15
                )
                shuffle(matching_tiles)
                radon_status["tiles"] = matching_tiles
                is_tile_delivery = True
                self.farmer.deliver_radon_status(radon_status)

            #   We need to close this private message
            elif radon_status.get("code") == 12:
                matching_tiles = []
                self.grid_width = 6
                self.grid_height = 6
                matching_tiles = self.get_tiles_matching_colour_from_pil_image_within_tolerance(
                    screenshot, self.colours["button_close_private_message"], 0.00
                )
                #print(matching_tiles)
                #shuffle(matching_tiles)
                #matching_tiles.reverse()
                #
                #   Fix the x co-ord by 26px
                final_tiles = []
                for tile in matching_tiles:
                    if int(tile["info"]["y_center"]) > 150 and int(tile["info"]["y_center"]) < 650:
                        tile["info"]["x_center"] = int(tile["info"]["x_center"]) + 26
                        final_tiles.append(tile)
                radon_status["tiles"] = final_tiles
                is_tile_delivery = True
                self.farmer.deliver_radon_status(radon_status)
                self.grid_width = 8
                self.grid_height = 8

            # We need to use a pokeball
            elif radon_status.get("code") == 13:
                matching_tiles = []
                self.grid_width = 4
                self.grid_height = 4
                matching_tiles = self.get_tiles_matching_colour_from_pil_image_within_tolerance(
                    screenshot, self.colours["button_pokeball_colour"], 0.00
                )
                shuffle(matching_tiles)
                for tile in matching_tiles:
                    tile["info"]["x_center"] = int(tile["info"]["x_center"]) + 75
                radon_status["tiles"] = matching_tiles
                is_tile_delivery = True
                self.grid_width = 8
                self.grid_height = 8
                self.farmer.deliver_radon_status(radon_status)

            # We need to confirm this selection
            elif radon_status.get("code") == 11:
                matching_tiles = []
                matching_tiles = self.get_tiles_matching_colour_from_pil_image_within_tolerance(
                    screenshot, self.colours["button_learn_move_confirm_green"], 0.33
                )
                #print(matching_tiles)
                shuffle(matching_tiles)
                radon_status["tiles"] = matching_tiles
                is_tile_delivery = True
                self.farmer.deliver_radon_status(radon_status)


            # It's just a normal delivery, no tiles to click on 
            if not is_tile_delivery:
                self.farmer.deliver_radon_status(radon_status)

            # Metrics
            self.end_timer()
            self.cli.input_string_last_radon_time = str(self.get_processing_time_in_seconds())
            self.cli.input_string_last_radon_status = str(radon_status["code"])
            self.cli.input_string_last_radon_info = radon_status["status"]
            self.prowatch.append_write_to_log(
                radon_status["code"],
                radon_status["status"],
                "None",
                "None"
            )
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
    #
    #
    #   N E W
    #
    #
    #

    def test(self):
        while True:
            #text = self.read_text_from_pil_image(self.get_screenshot_pil_image())
            #self.get_radon_status_from_text(text)
            screenshot = self.get_screenshot_pil_image()
            tolerance = 0.25
            # do a colour analysis
            for key,colour in self.colours.items():
                #print(key)
                #print(colour)
                #
                #   Read this colour
                tiles = self.get_tiles_matching_colour_from_pil_image_within_tolerance(
                    screenshot, colour, tolerance
                )
                if len(tiles) > 0:
                    print("{} = {} tiles @ {}% tolerance".format(
                        key, len(tiles), tolerance*100
                    ))
                    for tile in tiles:
                        print(self.get_center_point_of_tile(tile))

    #
    # A function to define the center point of an image
    def get_center_point_of_tile(self, tile):
        center = (
            int(tile["info"]["x"] / 2),
            int(tile["info"]["y"] / 2),
        )
        return center


    #
    #   A function to return a Radon Status
    def get_radon_status_from_text(self, text):
        if self.debug_is_printing_text:
            print("\n\n{}\n\n".format(text))
        radon_status = {
           "code": 0,
           "status": "0: radon could not gather any useful information during this analysis of text"
        }
        #
        #   Exact matches only
        check_text = text.lower()
        if " PM" in text and "chat" in check_text:
            radon_status = {
                "code": 12,
                "status": "12: some rando is trying to private message us"
            }
            #print(check_text)
            #print(radon_status)
        if "login red" in check_text or "login blue" in check_text or "login yellow" in check_text:
            # PASS
            radon_status = {
               "code": 10,
               "status": "10: warning, we are not logged in"
            }
        if "left!!" in check_text or "has no" in check_text:
            # PASS
            radon_status = {
               "code": 20,
               "status": "20: this pokemon has run out of pp for this move"
            }
        if "evolving" in check_text or "no yes" in check_text or "no ves" in check_text or "evolv" in check_text:
            # PASS
            radon_status = {
               "code": 21,
               "status": "21: this pokemon needs to evolve"
            }
        if "learn move" in check_text or "cancel ok" in check_text or "cancel" in check_text or "learn" in check_text or "lmrn mmra" in check_text:
            # PASS
            radon_status = {
               "code": 11,
               "status": "11: we need to confirm our selection"
            }
        if "this move" in check_text:
            # PASS
            radon_status = {
               "code": 22,
               "status": "22: this pokemon is trying to learn a move"
            }
        if "choose item" in check_text or "pokeball" in check_text or "(hoose" in check_text or " Item" in text :
            # PASS
            radon_status = {
               "code": 13,
               "status": "13: we are trying to catch a pokemon using a pokeball"
            }
        

        #
        #   Test, get the names of the pokemon we meed
        #print(check_text)
        if "wild" in check_text:
            #
            #   Pokemon data
            pokemands = []
            poke_file_data = ""
            with open("pokemon.txt", "r") as pokefile:
                poke_file_data = pokefile.read()
            for poke in poke_file_data.split("\n"):
                pokemands.append(poke)
            #
            #   Run a check here
            for line in check_text.split("\n"):
                    for pokemand in pokemands:
                        if pokemand in line:
                            try:
                                self.farmer.last_poke_name = pokemand
                            except:
                                pass
                            status_string = datetime.datetime.now().strftime("[%y-%m-%d-%H-%M-%S]\t")
                            status_string += "29\t29: we are fighting a pokemon\t"
                            status_string += str(pokemand) + "\n"
                            print(status_string.split("\n")[0])
                            with open("seenpokemon.txt", "a") as seen_pokefile:
                                if time.time() - self.last_poke_save_time > 30:
                                    seen_pokefile.write(status_string)
                                    self.last_poke_save_time = time.time()                                    
                                    #self.farmer.change_to_catch_pokemon_move_sequence()
        if self.debug_is_printing_text:
            print(radon_status)
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
    #
    #
    #   E N D  N E W
    #
    #
    #

    #
    #    I M A G E S
    #    Images
    #
    #    Return a screenshot from the current system as a PIL Image
    def get_screenshot_pil_image(self):
        #
        #    See import PIL
        return ImageGrab.grab()
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


def main():
    r = Radon()



    while True:
        r.test()
    sys.exit(0)

#main()


print("\tradon started analysing the screen")


from radon.pytesseract.pytesser import *
#from pyautogui import press, typewrite, hotkey
from PIL import ImageGrab, Image
import sys
import threading
import time


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

    # Initialise
    def run(self):
        while True:
            self.farmer = self._args[0]
            self.farmer.deliver_radon_text(self.read_text_from_pil_image(self.get_screenshot_pil_image()))

    #
    # M E T R I C S
    # Metrics
    #
    # Timers for timing processing of function
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
        return time_difference
        #round(time_difference, 3)

    #
    # D E B U G  /  T E S T
    def test(self):
        #colour_to_find = (223,54,54,) # cancel button move
        colour_to_find = (203, 4, 4,) # No to evolve
        grid_width = 8
        grid_height = grid_width

        #
        # Get screenshot
        self.start_timer()
        screenshot = self.get_screenshot_pil_image()
        self.end_timer()
        print("SCREENSHOT : {}".format(self.get_processing_time_in_seconds()))
        #
        # Get PIL tiles
        self.start_timer()
        pil_tiles = self.get_radon_image_objects_from_pil_image(screenshot, grid_width, grid_height)
        #self.end_timer()
        #print("CREATE PIL TILES FROM SOURCE IMAGE : {}".format(self.get_processing_time_in_seconds()))
        #
        # Colour analysis
        #self.start_timer()
        matching_tiles = 0
        matched_tiles = []
        for tile in pil_tiles:
            colour_analysis_results = self.colour_analysis_for_given_colour(
                tile["image"], colour_to_find, 0.5)
            if colour_analysis_results["overall_analysis"]:
                """
                print("\tMATCHING TILE [{}px x {}px]: x: {}, y: {}".format(
                    grid_width, grid_height, tile["info"]["x"], 
                    tile["info"]["y"]
                ))
                """
                matching_tiles += 1
                matched_tiles.append(tile)

        self.end_timer()
        print("COLOUR ANALYSIS : {}".format(self.get_processing_time_in_seconds()))
        print("MATCHING TILES : {}".format(matching_tiles))
        for tile in matched_tiles:
            print(tile["info"]["x"], tile["info"]["y"])
        #
        # Tesseract
        self.start_timer()
        text = self.read_text_from_pil_image(screenshot)
        if "remember password" in text.lower():
            print("W E  A R E  N O T  L O G G E D  I N")
        self.end_timer()
        print("TESSERACT : {}".format(self.get_processing_time_in_seconds()))


    #
    # I M A G E S
    # Images
    #
    # Return a screenshot from the current system as a PIL Image
    def get_screenshot_pil_image(self):
        #
        # See import PIL
        return ImageGrab.grab()
    #
    # Return a list of RadonImage objects
    def get_radon_image_objects_from_pil_image(self, pil_image, grid_width, grid_height):
        #
        # Read and store the input image information
        origin_width, origin_height = pil_image.size
        #
        # Define grid
        grid_width = 8
        grid_height = 8
        square_horizontal = int(origin_width / grid_width)
        square_vertical = int(origin_height / grid_height)
        total_squares = square_vertical * square_horizontal
        #print("G R I D  @  {}x{}px  =  {}x{}".format(grid_width,grid_height, square_vertical, square_horizontal))
        #
        # Using this grid, create the images sections we need and return them
        x,y = 0,0
        tiles = []
        for current_grid_tile in range(0, total_squares):
            tile_data = {
                "x": x,
                "y": y,
                "coordinates": (x,y,x+grid_width,y+grid_height,)
            }
            #
            # Now that we have the information about the tile_data, get the image for this tile
            # by cutting it from our source image
            tile_image = pil_image.crop(tile_data["coordinates"])
            #
            # Convert this into RGB
            tile_image_rgb = tile_image.convert('RGB')
            #
            # Store this as an output object
            tile = {
                "info": tile_data,
                "image": tile_image_rgb
            }
            #
            # Save to our output array
            tiles.append(tile)
            #
            # Iterate through our grid, updating our co-ordinated each time
            x += grid_width
            if x > origin_width:
                x = 0
                if y > origin_height:
                    y = 0
                else:
                    y += grid_height
        return tiles

    #
    # A function to handle colour analysis
    def colour_analysis_for_given_colour(self, pil_image_rgb, search_colour=(255,255,255,), tolerance=0.1):
        #
        # Ok, so let's adapt our search_colour for tolerance
        toleranced_search_colour_max = (
            int(search_colour[0] * (tolerance + 1)),
            int(search_colour[1] * (tolerance + 1)),
            int(search_colour[2] * (tolerance + 1)),)
        toleranced_search_colour_min = (
            int(search_colour[0] / (tolerance + 1)),
            int(search_colour[1] / (tolerance + 1)),
            int(search_colour[2] / (tolerance + 1)),)
        #
        # Quick checks, if bigger than 255, fix this
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
        # Ok, so now let's look at the center pixel
        x_width, y_height = pil_image_rgb.size
        #
        # What colour is this pixel?
        r, g, b = pil_image_rgb.getpixel(
            (int(x_width / 2), int(y_height / 2))
        )
        #
        # Analyse this colour, if it matches each of our inputs - we are valid
        is_valid_red, is_valid_blue, is_valid_green = False,False,False
        if r >= toleranced_search_colour_min[0] and r <= toleranced_search_colour_max[0]:
            is_valid_red = True
        if g >= toleranced_search_colour_min[1] and g <= toleranced_search_colour_max[1]:
            is_valid_green = True
        if b >= toleranced_search_colour_min[2] and b <= toleranced_search_colour_max[2]:
            is_valid_blue = True
        #
        # Return our values
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
    # O C R
    # Optical Character Recognition
    #
    # Using Google's Tesseract, read the text from an PIL image
    def read_text_from_pil_image(self, pil_image):
        text = ""
        #
        # Use Google's Tesseract to read that image, see import pytesseract.pytesser
        text = image_to_string(pil_image)

        return text


class TesseractInteraction (threading.Thread):
    def __init__(self, threadID, name, counter, args):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.args = args
    def run(self):
        while True:
            #print("Starting " + self.name)
            text = read_text_from_screenshot_taken_right_now()
            #print("Exiting " + self.name)


class KeyboardInteraction (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        while True:
            #print("Starting " + self.name)
            #print(current_key)
            simulated_keyboard()
            time.sleep(1)

            #print("Exiting " + self.name)


def read_text_from_screenshot_taken_right_now():
    #
    # Take a screenshot
    a = time.time()
    im = ImageGrab.grab()
    b = time.time()
    length_of_time = round((b - a), 3)
    print("S C R E E N S H O T  G E N E R A T E D\t{}".format(length_of_time))

    #
    # OK, let's analyse this image and read the colours
    a = time.time()
    width, height = im.size
    origin_width, origin_height = im.size
    #
    # Define grid
    grid_width = 8
    grid_height = 8
    square_horizontal = int(width / grid_width)
    square_vertical = int(height / grid_height)
    total_squares = square_vertical * square_horizontal
    print("G R I D  @  {}x{}px  =  {}x{}".format(grid_width,grid_height, square_vertical, square_horizontal))

    x,y = 0,0
    #
    # For each tile
    grid_coordinates = []
    for current_grid_tile in range(0, total_squares):
        grid_coordinates.append((x,y,))
        #print("\tG R I D  S Q U A R E  #{}  : {},{}".format(current_grid_tile, x, y))
        x += grid_width
        if x > width:
            x = 0
            if y > height:
                y = 0
            else:
                y += grid_height


    #
    # Create squares
    squares = []
    for grid_coordinate in grid_coordinates:
        x = grid_coordinate[0]
        y = grid_coordinate[1]
        square = {
            "x": x,
            "y": y,
            "coordinates": (x,y,x+grid_width,y+grid_height,)
        }
        #print(square)
        squares.append(square)

    grid_image_data = []
    squares_that_contain_red_pixels = []
    for square in squares:
        square_img = im.crop(square["coordinates"])

        #
        # Ok, so while we are here, iterate and get the pixel info
        rgb_im = square_img.convert('RGB')
        i = {
            "square": square,
            "image": rgb_im
        }

        #time.sleep(10)
        width, height = rgb_im.size

        #
        # Get the centre pixed of this oject
        r, g, b = rgb_im.getpixel((width / 2, height / 2))
        if r > g + b:
            #
            # This pixel is more red than anything else
            squares_that_contain_red_pixels.append(i)

        grid_image_data.append(i)

    #
    # Ok, now rebuild the image but use white tiles to replace the empty tiles
    x,y = 0,0
    #
    # For each tile
    final_tiles = []

    white_square = Image.new('RGB', (grid_width,grid_height,), (255,255,255))
    final_image = Image.new('RGB', (origin_width, origin_height,), (255,255,255))
    for current_grid_tile in range(0, total_squares):
        added_to_final_tiles = False
        #
        # Is this tile in our red array
        final_tile = ""
        for tile in squares_that_contain_red_pixels:
            #print(tile["square"]["x"], )
            #print(tile["square"]["x"])
            #print(tile["square"]["x"],tile["square"]["y"], x,y)

            if int(tile["square"]["x"]) == x and int(tile["square"]["y"]) == y:
                final_tile = {
                    "square": tile["square"],
                    "image": tile["image"]
                }

                final_tiles.append(final_tile)
                added_to_final_tiles = True
                #print("RED TILE")
                break
        if not added_to_final_tiles:
            final_tile = {
                    "square": squares[current_grid_tile],
                    "image": white_square
                }

            final_tiles.append(final_tile)

        #
        # A D D  T O  O U T P U T
        #print(final_tile)
        final_image.paste(final_tile["image"], final_tile["square"]["coordinates"])
        #print("\tG R I D  S Q U A R E  #{}  : {},{}".format(current_grid_tile, x, y))
        x += grid_width
        if x > origin_width:
            x = 0
            if y > origin_height:
                y = 0
            else:
                y += grid_height

    #
    # Finally, re-assemble this image
    final_image.save("MODIFIED.png")

    #print(final_tiles)
    #print(len(final_tiles))
    #print(len(grid_coordinates))

    #print(grid_image_data[0])
    #print(squares)
    b = time.time()
    length_of_time = round((b - a), 3)

    print("I M A G E  C O L O U R  A N A L Y S I S  : {}".format(length_of_time))
    percentage_red = round(len(squares_that_contain_red_pixels) / len(grid_image_data), 2)
    print("S Q U A R E S  T H A T  C O N T A I N  R E D  :  {} ({}%)".format(len(squares_that_contain_red_pixels), percentage_red))



    #
    # Read the text from that image
    a = time.time()
    text = image_to_string(im)
    b = time.time()
    length_of_time = round((b - a), 3)
    print("T E S S R A C T  I N\t{}".format(length_of_time))


    text = image_to_string(im)
    #print(text)
    pp_checker(text)
    ocr_analysis(text)
    return text

def ocr_analysis(text):
    if "not not learn" in text:
        print("D O  N O T  L E A R N")
    if "learn"  in text:
        print("L E A R N")
    if "this move"  in text:
        print("T H I S  M O V E")



def pp_checker(text):
    if "no PP left" in text:
        print("!!! NO PP !!!")
        current_key = "4"
        for i in range(0, 50):
            print("4")
            press("4")
            print("W")
            press("w")
            time.sleep(0.25)


        for i in range(0, 32):
            print("<space>, s")
            press(" ")
            press("s")

            time.sleep(0.25)



def simulated_keyboard():
    press("1")


# Create new threads
#thread_tesseract = TesseractInteraction(1, "TESSERACT", 5, "no_pp.png")
#thread_keyboard = KeyboardInteraction(2, "KEYBOARD", 1)

# Start new Threads
#thread_tesseract.start()
#thread_keyboard.start()

print("Exiting Main Thread")


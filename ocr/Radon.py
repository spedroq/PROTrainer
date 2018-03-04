# pip install Pillow
import sys
import random
import os
import string
import time
from stat import S_ISREG, ST_CTIME, ST_MODE
#
#    Pillow image library
from PIL import Image
from PIL import ImageFilter
from PIL import ImageGrab



#
#    R A D O N
#    Radon
#
#    A class that is used to read text data from images
#    It's also able to save images from print screen
class Radon:
    #
    #    When constructing Radon we need the python access library for Tesseract
    def __init__(self, tesseract):
        self.tesseract = tesseract
        self.dir_screenshots = "./screenshots/"
        self.screenshot_file_extension = ".png"
        self.screenshots_limit = 2
        self.screenshots_saved = 0
        if not os.path.isdir(self.dir_screenshots):
            os.mkdir(self.dir_screenshots)
        self.clear_cache()
    #
    #    A function to read the text from an image and return it as a string
    def read_text_from_image(self, filename):
      
            #
            #    Read the image using Pillow, converts into bytes I think
            input_image = Image.open(filename)
            #
            #    Read the words from this image using Google's Tesseract through a python
            #    library passed to us at runtime
            words = self.tesseract.image_to_string(input_image, lang="eng")
            #
            #    Return the words, pretty sure it's a UTF-8 string
            return words
        
    #
    #    A function to save a screenshot
    def save_screenshot(self):
        #
        #    If no output filename was given, create a random one
        output_filename = str(self.screenshots_saved)
        self.screenshots_saved += 1
        output_filepath = self.dir_screenshots + output_filename + self.screenshot_file_extension
        #
        #    Take a screenshot using Pillow
        img = ImageGrab.grab().convert('L')
        #
        #    Is there enough space to save?
        self.screenshot_cache_handler()

        img.save(output_filepath)
        return output_filepath

    #
    #    A function to ensure we don't save too many files
    def screenshot_cache_handler(self):
        cache_full = False
        file_list = self.get_directory_files_by_created_ascending(self.dir_screenshots)
        #print(file_list)
        if len(file_list) > self.screenshots_limit:
            os.remove(file_list[0]["filepath"])
            print("deleted a file {} in the cache".format(file_list[0]["filepath"]))
        return cache_full

    #
    #    A function to clear the cache
    def clear_cache(self):
        for file in os.listdir(self.dir_screenshots):
            os.remove(self.dir_screenshots + file)

    #
    #    A function to delete a file
    def delete_screenshot(self, filepath):
        os.remove(filepath)
    #
    #    Generate a random lowercase string of letters n
    def random_generator(size=6, chars=string.ascii_lowercase):
        return "123123123"


    #
    #    A function to get a list of the files in a directory by created time
    #    ascending
    def get_directory_files_by_created_ascending(self, dirpath):
        # get all entries in the directory w/ stats
        entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
        entries = ((os.stat(path), path) for path in entries)

        # leave only regular files, insert creation date
        entries = ((stat[ST_CTIME], path)
                   for stat, path in entries if S_ISREG(stat[ST_MODE]))
        #NOTE: on Windows `ST_CTIME` is a creation date 
        #  but on Unix it could be something else
        #NOTE: use `ST_MTIME` to sort by a modification date
        els = []
        for cdate, path in sorted(entries):
            els.append({
                "created": cdate,
                "filepath": path
        })
        return els



"""
def test():
    filename = "test.png"
    r = Radon(pt)
    print(r.read_text_from_image(filename))

    print("\n\n\n")
    for i in range(0, 10):
        time.sleep(1)
        r.save_screenshot()

test()
"""
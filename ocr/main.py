# pip install Pillow
import sys
import random
import os
try:
	import Image
except ImportError:
	from PIL import Image
	from PIL import ImageFilter
	from PIL import ImageGrab
import pytesseract as pt
import string

import time

#
#
#	R A D O N
#	Radon
#
#	A class that is used to read text data from images
#	It's also able to save images from print screen
class Radon:
	#
	#	When constructing Radon we need the python access library for Tesseract
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
	#	A function to read the text from an image and return it as a string
	def read_text_from_image(self, filename):
		try:
			#
			#	Read the image using Pillow, converts into bytes I think
			input_image = Image.open(filename).convert("L")
			#
			#	Read the words from this image using Google's Tesseract through a python
			#	library passed to us at runtime
			words = self.tesseract.image_to_string(input_image, lang="eng")
			#
			#	Return the words, pretty sure it's a UTF-8 string
			return words
		except IOError:
			#
			#	Read error thrown, file was not found probably
			#	Could also be a tesseract error, needs to be looked at
			sys.stderr.write('ERROR: Could not open file "%s"\n' % filename)
	#
	#	A function to save a screenshot
	def save_screenshot(self):
		#
		#	If no output filename was given, create a random one
		output_filename = str(self.screenshots_saved)
		self.screenshots_saved += 1
		output_filepath = self.dir_screenshots + output_filename + self.screenshot_file_extension
		#
		#	Take a screenshot using Pillow
		img = ImageGrab.grab()
		#
		#	Is there enough space to save?
		self.screenshot_cache_handler()

		img.save(output_filepath)
		return output_filepath

	#
	#	A function to ensure we don't save too many files
	def screenshot_cache_handler(self):
		cache_full = False
		file_list = os.listdir(self.dir_screenshots)
		print(file_list)
		if len(file_list) > self.screenshots_limit:
			fp = self.dir_screenshots +  file_list[0]
			os.remove(fp)
			print("deleted a file {} in the cache".format(fp))
		return cache_full

	#
	#	A function to clear the cache
	def clear_cache(self):
		for file in os.listdir(self.dir_screenshots):
			os.remove(self.dir_screenshots + file)

	#
	#	A function to delete a file
	def delete_screenshot(self, filepath):
		os.remove(filepath)
	#
	#	Generate a random lowercase string of letters n
	def random_generator(size=6, chars=string.ascii_lowercase):
		return "123123123"




def test():
	filename = "test.png"
	r = Radon(pt)
	print(r.read_text_from_image(filename))

	print("\n\n\n")
	for i in range(0, 10):
		time.sleep(1)
		r.save_screenshot()

test()
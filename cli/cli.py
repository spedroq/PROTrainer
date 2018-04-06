import colorama
import click
import random
import time
import sys
import threading
import os
if getattr(sys, 'frozen', False):
    CurrentPath = sys._MEIPASS
# If it's not use the path we're on now
else:
    CurrentPath = os.path.dirname(__file__)
#
#	Define a CLI Class to hold everything
class PROTrainerCLI(threading.Thread):
	screen_width_in_characters = 120 # characters, set in template
	screen_height_in_characters = 30 # characters
	fps = 15
	screen_template_overview_filepath = os.path.join(CurrentPath, "templates/screen_template_overview.txt")
	screen_template_loading_filepath =  os.path.join(CurrentPath, "templates/screen_template_loading.txt")
	start_time = time.time()
	border_character = "^"
	branch_string = "development"
	#
	#	Strings that will be updated by the farmer
	input_string_mode = "<mode>"
	input_string_move_sequence = "<move sequence>"
	input_string_last_radon_time = "<last radon time>"
	input_string_last_radon_status = "<last radon status>"
	input_string_last_radon_info = "<last radon info>"
	#
	#	FLow control
	debug = False
	cli_mode = {
		"state": "loading"
	}
	is_loading_screen = True
	# state: [ loading, overview ]
	loading_screen_position = 0

	last_screen_update_string = ""

	def run(self):
		#self.show_loading_screen()
		while True:
			#
			pass
			#self.render_screen_to_console(self.fps)

	#
	#	A function to return the string of the correct template
	#	file for the active mode
	def get_screen_template_string_using_active_mode(self):
		template_text = "error"
		if not self.is_loading_screen:
			with open(self.screen_template_overview_filepath, "r") as f:
				template_text = f.read()
		if self.is_loading_screen:
			with open(self.screen_template_loading_filepath, "r") as f:
				template_text = f.read()
			max_lines = len(template_text.split("\n"))
			if self.loading_screen_position > max_lines:
				self.loading_screen_position = 0
			else:
				self.loading_screen_position += 1

		return template_text


	#
	#	A function to change to loading screen mode
	def show_loading_screen(self):
		self.is_loading_screen = True

	#
	#	A function to change to overview mode
	def show_overview_screen(self):
		self.is_loading_screen = False
		
	#
	#	A function to generate an entire screen string
	def draw_screen(self):
		#
		#	Open the template file
		template_text = self.get_screen_template_string_using_active_mode()
		split_lines = template_text.split("\n")
		if self.is_loading_screen:
			#
			#	If we are on the loading screen, snip this text
			updated_template_text = ""
			i = 0
			start_line = self.loading_screen_position
			end_line = start_line + self.screen_height_in_characters
			first_lines = []
			template_text_lines = split_lines
			for line in template_text_lines:
				if i < self.screen_height_in_characters:
					first_lines.append(line)
				if i > start_line:
					updated_template_text += line + "\n"
				i += 1
				if i >= end_line:
					break
			#
			#	Are there enough lines?
			lines_left_in_template = len(template_text_lines) - self.loading_screen_position
			if self.screen_height_in_characters > lines_left_in_template:
				for j in range(0, self.screen_height_in_characters - lines_left_in_template - 1):
					updated_template_text += first_lines[j] + "\n"

			template_text = updated_template_text
			split_lines = updated_template_text.split("\n")
		#
		#	Replace our variables
		entire_screen_string = ""
		l = 0
		for line in split_lines:
			#
			#	Save the length of a line, will be the expected length
			correct_line_length = len(line)
			if "[branch]" in line:
				line = line.replace("[branch]", self.branch_string)
			if "[mode_type]" in line:
				line = line.replace("[mode_type]", self.input_string_mode)
			if "[move_sequence]" in line:
				line = line.replace("[move_sequence]", self.input_string_move_sequence)
			if "[last_radon_time]" in line:
				line = line.replace("[last_radon_time]", self.input_string_last_radon_time + "s")
			if "[last_radon_status]" in line:
				line = line.replace("[last_radon_status]", self.input_string_last_radon_status)
			if "[last_radon_info]" in line:
				line = line.replace("[last_radon_info]", self.input_string_last_radon_info)

			if "[uptime]" in line:
				now = time.time()
				uptime = round(now - self.start_time, 1)
				uptime_string = self.get_time_letter_from_time(uptime)
				line = line.replace("[uptime]", uptime_string)
			#
			#	Fix the length of the line
			
			if len(line) < self.screen_width_in_characters:
				#
				#	Adjust the length of this line to the max character length
				for i in range(0, correct_line_length - len(line)):
					line += " "
				#
				#	If we're not on the loading screen, add the border character
				if not self.is_loading_screen:
					line = line[:-1] + self.border_character
			if len(line) > self.screen_width_in_characters:
				line = str(line[:self.screen_width_in_characters - 6])
				line += "... "
				if not self.is_loading_screen:
					line += self.border_character

			if len(line) > 1:
				entire_screen_string += line + "\n"
			if split_lines[l] == split_lines[len(split_lines) - 1] and self.is_loading_screen:
				entire_screen_string += "\n                                                    press p to start"
			l += 1

		return entire_screen_string

	def get_time_letter_from_time(self, seconds):
		#
		#	Figure out what letter to display
		final_letter = "s"
		output_string = ""
		time_shards = {
			"d": 8640,
			"h": 360,
			"m": 60,
			"s": 1			
		}
		for letter,size in time_shards.items():
			if (seconds / size) - size < 0 and seconds > 60:
				#
				#	Use this one
				final_letter = letter
				output_string = "{}{}".format(
					round(seconds / size, 1), letter
				)
			if seconds < 60:
				output_string = "{}s".format(round(seconds, 1))
		return output_string

	def print_screen(self, entire_screen_string):
		#
		#	Clear the screen
		if self.debug:
			print(entire_screen_string)
		else:
			click.clear()
			print("\r" + entire_screen_string)

	#
	#	A Loop to continually display the screen with a timeout
	def render_screen_to_console(self, fps=30):
		delay = 1 / fps
		#
		#	Clear the screen
		#sys.stdout.flush()
		#
		#	Update the screen at that speed
		screen_update = self.draw_screen()
		self.print_screen(screen_update)
		time.sleep(delay)

		

			
"""
start_time = time.time()

cli = PROTrainerCLI()
fps = 5
cli.render_screen_to_console(fps)
input()
"""
from radon.Radon import *
from PIL import Image
import time

#	Radon object
r = Radon()



def test(r, test_name, screenshot_path, expected_error_code):
	passes = 0
	fails = 0
	with open("temp.txt", "w") as f:
		f.write("")
	#
	#	Test for no pp
	screenshot = Image.open(screenshot_path)
	#screenshot.show()
	text = r.read_text_from_pil_image(screenshot)
	#print(text)
	# Ok, cool we have the text, let's check for colours
	radon_status = r.get_radon_status_from_text(text)
	print("\n")
	print(test_name + " TEST  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -")
	print("\t" + str(radon_status))
	matching_tiles = []
	#   We need to login			
	if radon_status.get("code") == 10:
		matching_tiles = r.get_tiles_matching_colour_from_pil_image_within_tolerance(
			screenshot, r.colours["button_login_yellow"], 0.25
		)
		shuffle(matching_tiles)
		radon_status["tiles"] = matching_tiles
		is_tile_delivery = True
		
	#   This pokemon needs to evolve
	elif radon_status.get("code") == 21:
		matching_tiles = r.get_tiles_matching_colour_from_pil_image_within_tolerance(
			screenshot, r.colours["button_accept_red"], 0.5
		)
		shuffle(matching_tiles)
		radon_status["tiles"] = matching_tiles
		is_tile_delivery = True

	#   This pokemon needs to learn a move
	elif radon_status.get("code") == 22:
		matching_tiles = r.get_tiles_matching_colour_from_pil_image_within_tolerance(
			screenshot, r.colours["button_learn_move_red"], 0.15
		)
		shuffle(matching_tiles)
		radon_status["tiles"] = matching_tiles
		is_tile_delivery = True

	# We need to confirm this selection
	elif radon_status.get("code") == 11:
		matching_tiles = r.get_tiles_matching_colour_from_pil_image_within_tolerance(
			screenshot, r.colours["button_learn_move_confirm_green"], 0.5
		)
		#print(matching_tiles)
		shuffle(matching_tiles)
		radon_status["tiles"] = matching_tiles
		is_tile_delivery = True


	if radon_status.get("code") != expected_error_code:
		fails += 1
		print("\t{} TEST | FAILED".format(test_name))
		with open("radon/tests/{}.txt".format(test_name), "w") as fi:
			fi.write(text)
	else:
		passes += 1
		print("\t{} TEST | PASSED".format(test_name))
		if radon_status.get("tiles"):
			print("\t{} TILES TO CLICK".format(len(
				radon_status.get("tiles")))
			)

	
	
	#time.sleep(1)

	if fails == 1:
		return False
	if passes == 1:
		return True

passes = 0
fails = 0

evolve_test = test(r, "EVOLVE", "radon/screenshots/evolve.png", 21)
if evolve_test:
	passes += 1
else:
	fails += 1

pp_text = test(r, "PP", "radon/screenshots/no_pp.png", 20)
if pp_text:
	passes += 1
else:
	fails += 1

do_not_learn_this_move_text = test(r, "DO NOT LEARN THIS MOVE", "radon/screenshots/learn_move.png", 22)
if do_not_learn_this_move_text:
	passes += 1
else:
	fails += 1

confirm_not_learn_move_text = test(r, "DO NOT LEARN THIS MOVE CONFIRM", "radon/screenshots/confirm_not_learn_move.png", 11)
if confirm_not_learn_move_text:
	passes += 1
else:
	fails += 1

login_text = test(r, "LOGIN", "radon/screenshots/login_screen.png", 10)
if login_text:
	passes += 1
else:
	fails += 1




print("\n\nRESULTS  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -")
print("\n\tPASSES: {}/{}\n\tFAILS: {}/{}\n\tOVERALL: {}%".format(
	passes,(passes + fails), fails,(passes + fails), round(passes / (passes + fails) * 100, 1)
))
print("\nTESTING COMPLETE  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -")

print("\nPress any key to exit")
input()
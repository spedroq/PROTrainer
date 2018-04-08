from radon.Radon import *
from PIL import Image
import time
import os
#    Radon object




def test_all_screenshots(r):
   

    mappings = [
        ("interaction_cancel_ok", 11),
        ("learnthismoveselect", 22),
        ("login", 10),
        ("pokebattle", 15),
        ("pokecenter", -1),
        ("pokeevolveprompt", 21),
        ("pokemoncenteroutside", -1),
    ]

    #
    #   Get the screenshots
    screenshot_paths = []
    screenshot_dir = "radon/screenshots"
    for s_f in os.listdir(screenshot_dir):
        if len(s_f) > 2:
            screenshot_paths.append(
                screenshot_dir + "/" + s_f
            )
    #
    #   For each screenshot, run a test
    for screenshot_path in screenshot_paths:
        #
        #   Get the test type
        test_type = ""
        test_expected_error = -2
        for mapping in mappings:
            if mapping[0] in screenshot_path:
                test_type = mapping[0]
                test_expected_error = mapping[1]

        #
        #   Run the test
        outcome = radon_test(r, test_type, screenshot_path, test_expected_error)


def radon_test(r, test_name, screenshot_path, expected_error_code):
    print("\n\n\n")
    screenshot = Image.open(screenshot_path)
    print(screenshot_path)
    r.start_timer()
    resp = r.mainline(screenshot)
    #print(resp)
    radon_status = resp[0]
    print(radon_status["status"])
    radon_text = resp[1]
    passes = 0
    fails = 0
    
    if radon_status.get("code") != expected_error_code:
        fails += 1
        print("\t{} TEST | FAILED".format(test_name))
        print(radon_text)
        with open("radon/tests/{}.txt".format(test_name), "w") as fi:
            fi.write(radon_text)
    else:
        passes += 1
        print("\t{} TEST | PASSED".format(test_name))
        if radon_status.get("tiles"):
            print("\t{} TILES TO CLICK".format(len(
                radon_status.get("tiles")))
            )

    
    
    #time.sleep(1)
    r.end_timer()
    print("Radon completed in [{}s]".format(r.get_processing_time_in_seconds()))

    if fails == 1:
        return False
    if passes == 1:
        return True

r = Radon()
test_all_screenshots(r)

"""
magikarp_test = test(r, "MAGIKARP TESTS", "radon/screenshots/magikarp.png", 13)
if magikarp_test:
    passes += 1
else:
    fails += 1
"""

"""
items_menu_pokeball = test(r, "ITEMS MENU POKEBALL", "radon/screenshots/items_screen.png", 13)
if items_menu_pokeball:
    passes += 1
else:
    fails += 1



private_message_test = test(r, "INCOMING RANDO MESSAGE #1", "radon/screenshots/private_message.png", 12)
if private_message_test:
    passes += 1
else:
    fails += 1


private_message_test = test(r, "INCOMING RANDO MESSAGE #2", "radon/screenshots/private_message_2.png", 12)
if private_message_test:
    passes += 1
else:
    fails += 1



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

confirm_not_learn_move_text = test(r, "DO NOT LEARN THIS MOVE CONFIRM #1", "radon/screenshots/confirm_not_learn_move.png", 11)
if confirm_not_learn_move_text:
    passes += 1
else:
    fails += 1

confirm_not_learn_move_text = test(r, "DO NOT LEARN THIS MOVE CONFIRM #2", "radon/screenshots/confirm_not_learn_move_2.png", 11)
if confirm_not_learn_move_text:
    passes += 1
else:
    fails += 1




login_text = test(r, "LOGIN", "radon/screenshots/login.png", 10)
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

"""
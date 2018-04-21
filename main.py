from control.control import Control
from protrainer_gui import *


def main():

    # Start the control
    control = Control(name="ControlThread")
    control.start()


# Start the main function
main()

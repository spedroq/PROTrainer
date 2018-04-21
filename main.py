from control.control import Control
from protrainer_gui import *


def main():

    """ CONTROL """

    # Start the control
    control_thread = Control(name="ControlThread")
    control_thread.start()

    """ GUI """

    # S E T U P
    root = tk.Tk()

    # S T A R T
    pro_gui = PROTrainerGUI(root=root, control_thread=control_thread)
    
    pro_gui.mainloop()


# Start the main function
main()

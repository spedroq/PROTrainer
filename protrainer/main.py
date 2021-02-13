from control.control import Control
#from protrainer_gui import *
import pytesseract
from PIL import Image


def main():

    """ CONTROL """

    # Start the control
    control_thread = Control(name="ControlThread")
    control_thread.start()

    """ GUI """

    # S E T U P
    #root = tk.Tk()

    # S T A R T
    #pro_gui = PROTrainerGUI(root=root, control_thread=control_thread)
    
    #pro_gui.mainloop()
    #pytesseract.pytesseract.tesseract_cmd = r'/snap/bin/tesseract'
    file_path = "/home/louis/Desktop/PROTrainer/radon/screenshots/interaction_cancel_ok_1.png"
    results = pytesseract.image_to_string(
        Image.open(file_path),
        lang="eng",
        output_type="dict"
    )
    print("\n\n", results, "\n\n")


# Start the main function
main()

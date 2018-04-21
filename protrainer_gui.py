import tkinter as tk
from tkinter import font

import time


class PROTrainerGUI(tk.Frame):
    width = 720
    height = 405
    base_padding = 5
    padding = {
        "0.5em": base_padding * 0.5,
        "0.75em": base_padding * 0.75,
        "0.8em": base_padding * 0.8,
        "1em": base_padding * 1,
        "2em": base_padding * 2,
        "3em": base_padding * 3
    }
    colours = {
        "background": "#333333",
        "foreground": "#cccccc"
    }
    default_padding = "1em"
    #
    #   Initialise
    def __init__(self, root, control_thread):
        super().__init__(root)
        self.pack(fill=tk.BOTH, expand=1)
        #
        #   Import control thread
        self.control_thread = control_thread
        #
        #   Define everything
        self.setup_window()
        

        self.draw_gui_thread_safe()



    def draw_gui_thread_safe(self):

        try:
            time.sleep(5)
            self.define_variables()
            self.draw_gui()
        except AttributeError:
            time.sleep(0.1)
            self.draw_gui_thread_safe()

    #
    #   A function to setup our window
    def setup_window(self):
        self.master.title("PROTrainerGUI")
        #
        #   Set the resolution to 720p
        self.master.maxsize(self.width, self.height)
        self.master.minsize(self.width, self.height)
        default_font = font.Font(family='Helvetica', size=12, weight='bold')
        self.master.option_add("*Font", default_font)

    #
    #   A function to define our variables
    def define_variables(self):
        self.intvar_protrainer_pause = tk.IntVar()
        self.intvar_radon_pause = tk.IntVar()
        #print("FARMER STATUS: {}".format(self.control_thread.farmer_thread.pause))
        if self.control_thread.farmer_thread.pause:
            self.intvar_protrainer_pause.set(1)
        if self.control_thread.radon_thread.pause:
            self.intvar_radon_pause.set(1)
       
    #
    #   A function to draw our GUI
    def draw_gui(self):
        #
        #   Define our frames, left and right for now
        self.frame_top = tk.Frame(
            self,
            bg="#333333",
            borderwidth=1,
            width=self.width,
            height=self.height / 4,
            padx=self.padding[self.default_padding],
            pady=self.padding[self.default_padding]
        )
        self.frame_left = tk.Frame(
            self, 
            bg="#444444", 
            borderwidth=1,
            width=int(self.width/2),
            height=self.height / 4 * 3,
            padx=self.padding[self.default_padding],
            pady=self.padding[self.default_padding]
        )
        self.frame_right = tk.Frame(
            self, 
            bg="#555555",
            borderwidth=1, 
            width=int(self.width/2),
            height=self.height / 4 * 3,
            padx=self.padding[self.default_padding],
            pady=self.padding[self.default_padding]
        )        

        self.frame_left.grid_rowconfigure(0, weight=1)
        self.frame_left.grid_rowconfigure(1, weight=1)

        #
        #   Grid it up
        self.frame_top.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.frame_left.grid(row=1, column=0, sticky="nsew")
        self.frame_right.grid(row=1, column=1, sticky="nsew")

        #
        #   Now add our elements
        self.label_header = tk.Label(self.frame_top, text="PROTrainer", fg=self.colours["foreground"], bg=self.colours["background"])

        #
        #   Create our widgets for checkboxes
        self.checkbox_protrainer_pause = tk.Checkbutton(
            self.frame_left, 
            text="PROTrainer Pause", 
            variable=self.intvar_protrainer_pause,
            bg=self.colours["foreground"],
            command=self.control_thread.farmer_thread.toggle_pause
        )
        self.checkbox_radon_pause = tk.Checkbutton(
            self.frame_left, 
            text="Radon Pause", 
            variable=self.intvar_radon_pause,
            bg=self.colours["foreground"],
            command=self.control_thread.radon_thread.toggle_pause
        )



        #self.label_header.pack()11
        #
        #   Grid up the widgets
        self.label_header.grid(row=0, column=0)
        self.checkbox_protrainer_pause.grid(row=0, column=0)
        self.checkbox_radon_pause.grid(row=1, column=0)


        #
        #   Configure containers
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)


#
#   S E T U P
#root = tk.Tk()

#
#   S T A R T
#pro_gui = PROTrainerGUI(master=root)
#pro_gui.mainloop()
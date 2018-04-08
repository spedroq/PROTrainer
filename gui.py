
class NFOReader:
    def __init__(self, nfo_file_path):
        self.nfo_file_path = nfo_file_path
        self.lines_in_frame = 30
        self.nfo_lines = []
        self.read_lines_from_nfo_to_memory()

    def read_lines_from_nfo_to_memory(self):
        nfo_text = ""
        with open(self.nfo_file_path, "r") as nfo:
            nfo_text = nfo.read()
        nfo_lines = nfo_text.split("\n")
        self.nfo_lines = nfo_lines



    def get_frame_of_nfo_from_line(self, line=0, overlay="", overlay_height=0):
        #
        #   Read the lines
        frame_text = ""
        for i in range(line, self.lines_in_frame + line):
            try:
                frame_text += self.nfo_lines[i] + "\n"
            except:
                #
                #   If we get to here, we are trying to access an index that doesn't
                #   exist, that means we should select from 0
                frame_text += self.nfo_lines[i % self.lines_in_frame] + "\n"
        if overlay != "":
            #
            #   Replace the last line with a message
            f_e = frame_text.split("\n")
            i = 0
            frame_text = ""
            for i in range(0, len(f_e) - 1):
                if i >= len(f_e) - overlay_height - 1:
                    #
                    #   Print our message
                    frame_text += overlay
                else:
                    frame_text += f_e[i] + "\n"

        return frame_text





from tkinter import Tk, Label, Button, Entry, Text, IntVar, StringVar, END, W, E, N, S
import tkinter as tk
import time
import datetime
class GUIFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.nfo_reader = NFOReader("screen_template_loading.txt")


        self.text = tk.Text(self, 
            height=30, 
            width=120,
            bg="#011640",
            fg="#DDEEF2"
        )
        self.text.configure(state="disabled")
        #self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        #self.text.configure(yscrollcommand=self.vsb.set)
        #self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
        self.fps = 7
        self.frame_delay = int(1000 / self.fps)
        #self.add_timestamp()

        self.line_offset = 0
        self.update_console_window()

    def insert_text_onto_top_of_console_window(self, text):
        self.text.configure(state="normal")
        self.text.delete('1.0', END)        
        self.text.insert("1.0", text)
        self.text.see("1.0")
        self.text.configure(state="disabled")
        

    def update_console_window(self):
        frame_text = self.nfo_reader.get_frame_of_nfo_from_line(
            self.line_offset, "\n                                                    press p to start\n", 3
        )
        self.line_offset += 1
        self.insert_text_onto_top_of_console_window(frame_text)
        self.after(self.frame_delay, self.update_console_window)
        

        

if __name__ == "__main__":
    root =tk.Tk()
    frame = GUIFrame(root)
    frame.pack(fill="both", expand=True)
    root.mainloop()



import time
import win32com.client as comclt


def press_1():
    while True:
        # Init
        wsh = comclt.Dispatch("WScript.Shell")
        # Choose the application
        wsh.AppActivate("Pokemon Revolution")
        # send the keys you want
        wsh.SendKeys("1")

        time.sleep(1)

press_1()

# 111

from PIL import ImageTk, Image
from tkinter import Tk
import constants
import os
import sys
sys.path.insert(0, "gui")
sys.path.insert(0, "signlang")

import gui_mouse
import gui_calibrate
import gui_main
import gui_menu
import gui_type_calibrate
import gui_type_cam
import gui_type_menu

def initPics():
    constants.imgLogo = ImageTk.PhotoImage(Image.open("../res/logo.png").resize((734, 205), Image.ANTIALIAS))
    constants.imgExit = ImageTk.PhotoImage(Image.open("../res/exit.png").resize((256, 256), Image.ANTIALIAS))
    constants.imgSave = ImageTk.PhotoImage(Image.open("../res/save.png").resize((128, 128), Image.ANTIALIAS))
    constants.imgCheck = ImageTk.PhotoImage(Image.open("../res/check.png").resize((128, 128), Image.ANTIALIAS))
    constants.imgToggle = ImageTk.PhotoImage(Image.open("../res/toggle.png").resize((128, 128), Image.ANTIALIAS))
    constants.imgStart = ImageTk.PhotoImage(Image.open("../res/start.png").resize((800, 160), Image.ANTIALIAS))
    constants.imgTitle = ImageTk.PhotoImage(Image.open("../res/title.png").resize((1800, 353), Image.ANTIALIAS))
    constants.imgHeader = ImageTk.PhotoImage(Image.open("../res/header.png").resize((1878, 172), Image.ANTIALIAS))
    constants.imgMouse = ImageTk.PhotoImage(Image.open("../res/mouse.png").resize((256, 256), Image.ANTIALIAS))
    constants.imgKeyboard = ImageTk.PhotoImage(Image.open("../res/keyboard.png").resize((256, 256), Image.ANTIALIAS))
    constants.imgHand = ImageTk.PhotoImage(Image.open("../res/hand.png").resize((256, 256), Image.ANTIALIAS))

def buildGUI():
    root = Tk()
    root.resizable(width = False, height = False)
    root.title("GripAid")
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", close)
    # root.geometry("1920x1080")
    # if os.name == "nt":
    #     root.iconbitmap(bitmap = os.path.abspath("../misc/icon.ico"))
    # else:
    #     root.iconbitmap(bitmap = "@" + os.path.abspath("../misc/icon.xbm"))
    root.grid_rowconfigure(0, weight = 1)
    root.grid_columnconfigure(0, weight = 1)
    constants.root = root
    initPics()

    mouse = gui_mouse.Mouse()
    calib = gui_calibrate.Calibrate()
    menu = gui_menu.Menu()
    type_calib = gui_type_calibrate.Type_Calibrate()
    type_cam = gui_type_cam.Type_Cam()
    type_menu = gui_type_menu.Type_Menu()
    main = gui_main.Main()

    mouse.setup()
    calib.setup()
    menu.setup()
    type_calib.setup()
    type_cam.setup()
    type_menu.setup()
    main.setup()

    constants.root.mainloop()

def close(e):
    constants.root.destroy()

if __name__ == "__main__":
    buildGUI()
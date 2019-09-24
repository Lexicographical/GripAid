from tkinter import Tk, Grid, Frame, Button, Label
from tkinter.font import Font
import constants
import gui_base

EXIT = 0
TOGGLE = 1

def action(code):
    if code == EXIT:
        constants.flagSave = True
        gui_base.switchLayout(constants.TYPE_MENU)
    elif code == TOGGLE:
        constants.streamState = not constants.streamState

class Type_Cam(gui_base.GUI):
    def __init__(self):
        super().__init__()

    def setup(self):
        btnExit = Button(self.frame, image=constants.imgLogo, command=lambda: action(EXIT), relief="flat")
        btnToggle = Button(self.frame, image=constants.imgToggle, command=lambda: action(TOGGLE), relief="flat")
        constants.lblTypeCamStream = Label(self.frame)
        constants.lblTypeCamStream.grid(columnspan=2)

        super().addElement(btnExit, 0, 0)
        super().addElement(btnToggle, 0, 1)
        super().addElement(constants.lblTypeCamStream, 1, 0)

        super().configureGrid()
        constants.frames[constants.TYPE_CAM] = self.frame
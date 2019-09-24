from tkinter import Tk, Grid, Frame, Button, Label
from tkinter.font import Font
import constants
import gui_base

class Type_Menu(gui_base.GUI):
    def __init__(self):
        super().__init__()

    def setup(self):
        lblInstruction = Button(self.frame, text="Keyboard Menu", command=lambda: gui_base.switchLayout(constants.MENU), font=constants.fontTitle, relief="flat")
        btnCam = Button(self.frame, text="Start Typing", compound="left", font=constants.fontMenu, image=constants.imgKeyboard, command=lambda: gui_base.switchLayout(constants.TYPE_CAM), relief="flat")
        btnCalibrate = Button(self.frame, text="Calibrate", compound="left", font=constants.fontMenu, image=constants.imgHand, command=lambda: gui_base.switchLayout(constants.TYPE_CALIBRATE), relief="flat")

        super().addElement(lblInstruction, 0, 0)
        super().addElement(btnCam, 1, 0)
        super().addElement(btnCalibrate, 2, 0)

        super().configureGrid()
        constants.frames[constants.TYPE_MENU] = self.frame
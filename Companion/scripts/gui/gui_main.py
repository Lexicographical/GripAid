from tkinter import Tk, Grid, Frame, Button, Label
from tkinter.font import Font
import constants
import gui_base

class Main(gui_base.GUI):
    def __init__(self):
        super().__init__()

    def setup(self):
        lblHeader = Label(self.frame, image=constants.imgHeader)
        lblHeader.grid(columnspan=5)
        lblLogo = Label(self.frame, image=constants.imgTitle)
        lblLogo.grid(columnspan=5)
        btnStart = Button(
            self.frame,
            image=constants.imgStart,
            command=lambda: gui_base.switchLayout(constants.MENU),
            relief="flat")
        btnStart.grid(columnspan=5)

        super().addElement(lblHeader, 0, 0)
        super().addElement(lblLogo, 1, 0)
        super().addElement(btnStart, 2, 0)
        super().addElement(None, 3, 4)

        super().configureGrid()
        constants.frames[constants.MAIN] = self.frame
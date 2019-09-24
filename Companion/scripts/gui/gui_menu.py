from tkinter import Tk, Grid, Frame, Button, Label
from tkinter.font import Font
import constants
import gui_base

class Menu(gui_base.GUI):
    def __init__(self):
        super().__init__()

    def setup(self):
        lblInstruction = Button(self.frame, text="Main menu", command=lambda: gui_base.switchLayout(constants.MAIN), font=constants.fontTitle, relief="flat")
        btnMouse = Button(self.frame, text="Mouse", compound="left", font=constants.fontMenu, image=constants.imgMouse, command=lambda: gui_base.switchLayout(constants.MOUSE), relief="flat")
        btnKeyboard = Button(self.frame, text="Keyboard", compound="left", font=constants.fontMenu, image=constants.imgKeyboard, command=lambda: gui_base.switchLayout(constants.TYPE_MENU), relief="flat")

        super().addElement(lblInstruction, 0, 0)
        super().addElement(btnMouse, 1, 0)
        super().addElement(btnKeyboard, 2, 0)

        super().configureGrid()
        constants.frames[constants.MENU] = self.frame
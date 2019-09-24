from tkinter import Tk, Grid, Frame, Button, Label
from tkinter.font import Font
import constants
import gui_base

def buildHandHist():
    frameHandHist = Frame(constants.root)
    frameHandHist.grid(row = 0, column = 0, sticky = "nsew")

    btnS = Button(frameHandHist, image=constants.imgSave, command = lambda: press("s"), relief = "solid", borderwidth=1)
    btnS.grid(row = 0, column = 0, sticky = "nsew")

    btnT = Button(frameHandHist, image=constants.imgToggle, command= lambda: press("t"), relief = "solid", borderwidth=1)
    btnT.grid(row=0, column=1, stick="nsew")

    btnC = Button(frameHandHist, image=constants.imgCheck, command = lambda: press("c"), relief = "solid", borderwidth=1)
    btnC.grid(row = 0, column = 2, sticky = "nsew")

    constants.lblHandHistStream = Label(frameHandHist)
    constants.lblHandHistStream.grid(row=1, column=0, columnspan=3)

    for i in range(2):
        Grid.rowconfigure(frameHandHist, i, weight = 1)
    for i in range(3):
        Grid.columnconfigure(frameHandHist, i, weight = 1)

    constants.frames[constants.HANDHIST] = frameHandHist

SAVE = 0
TOGGLE = 1
CALIBRATE = 2

def press(code):
    if code == SAVE:
        constants.flagSave = True
        gui_base.switchLayout(constants.TYPE_MENU)
    if code == TOGGLE:
        constants.streamState = not constants.streamState
    if code == CALIBRATE:
        constants.flagCalibrate = True

class Type_Calibrate(gui_base.GUI):
    def __init__(self):
        super().__init__()

    def setup(self):
        btnSave = Button(self.frame, image=constants.imgSave, command=lambda: press(SAVE), relief="flat")
        btnToggle = Button(self.frame, image=constants.imgToggle, command=lambda: press(TOGGLE), relief="flat")
        btnCalibrate = Button(self.frame, image=constants.imgCheck, command=lambda: press(CALIBRATE), relief="flat")
        constants.lblTypeCalibrateStream = Label(self.frame)
        constants.lblTypeCalibrateStream.grid(columnspan=3)

        super().addElement(btnSave, 0, 0)
        super().addElement(btnToggle, 0, 1)
        super().addElement(btnCalibrate, 0, 2)
        super().addElement(constants.lblTypeCalibrateStream, 1, 0)

        super().configureGrid()
        constants.frames[constants.TYPE_CALIBRATE] = self.frame
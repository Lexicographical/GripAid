from PIL import ImageTk, Image
from tkinter import Tk, Grid, Frame, Button, Label, messagebox
import constants
import util
import calibrate
import mouse

import set_hand_hist
import fun_util

class GUI:
    def __init__(self):
        self.frame = Frame(constants.root)
        self.frame.grid(row = 0, column = 0, sticky="nsew")
        self.row = self.col = 0

    def addElement(self, element, row, column):
        if element is not None:
            element.grid(row = row, column = column, sticky="nsew")
        else:
            print("Added null element!")
        self.row = max(self.row, row)
        self.col = max(self.col, column)

    def setup(self):
        pass

    def configureGrid(self):
        for i in range(self.row + 1):
            Grid.rowconfigure(self.frame, i, weight = 1)
        for i in range(self.col + 1):
            Grid.columnconfigure(self.frame, i, weight = 1)

def switchLayout(n):
    constants.frames[n].tkraise()
    if n == constants.CALIBRATE:
        calibrate.calibrate()
    elif n == constants.MOUSE:
        mouse.start_mouse()
    elif n == constants.TYPE_CALIBRATE:
        set_hand_hist.get_hand_hist()
    elif n == constants.TYPE_CAM:
        fun_util.recognize()
    if constants.frameCache == constants.CALIBRATE and n == constants.MAIN:
        util.activateFlag(constants.FLAG_SAVE)
    if constants.frameCache == constants.MOUSE and n == constants.MAIN:
        constants.flagSave = True
    constants.frameCache = n

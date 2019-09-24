from tkinter import Tk, Grid, Frame, Button, Label
import constants
import util
import gui_base

class Calibrate(gui_base.GUI):
    def __init__(self):
        super().__init__()

    def setup(self):
        btnTitle = Button(self.frame, text="GripAid", font=constants.fontTitle2, command=lambda: gui_base.switchLayout(constants.MAIN), relief = "flat")
        constants.lblCalibrateStream = Label(self.frame)
        constants.lblCalibrateStream.grid(columnspan=4)
        lblInstructions = Label(self.frame, text= "Put the neon part of the glove inside the green box.", font = constants.fontText)
        btnTest = Button(self.frame, text = "Test", command = util.toggleStreamState, relief = "solid")
        btnCalibrate = Button(self.frame, text = "Calibrate", command = lambda: util.activateFlag(constants.FLAG_CALIBRATE), relief = "solid")

        lblInstructions.grid(pady = 50)
        btnTest.grid(pady = 50, padx = 10)
        btnCalibrate.grid(pady = 50, padx = 10)

        btnTest.configure(font=constants.fontText)
        btnCalibrate.configure(font=constants.fontText)

        super().addElement(btnTitle, 0, 1)
        super().addElement(constants.lblCalibrateStream, 1, 1)
        super().addElement(lblInstructions, 2, 1)
        super().addElement(btnTest, 2, 3)
        super().addElement(btnCalibrate, 2, 4)

        super().configureGrid()
        Grid.rowconfigure(self.frame, 1, weight = 10)
        Grid.columnconfigure(self.frame, 1, weight = 3)
        Grid.columnconfigure(self.frame, 5, weight=1)
        constants.frames[constants.CALIBRATE] = self.frame
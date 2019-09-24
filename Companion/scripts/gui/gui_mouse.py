from tkinter import Tk, Grid, Frame, Button, Label, Checkbutton, Canvas
import constants
import util
import gui_base

btnTest = None
i = 0

coords1 = [0, 0, 0, 0]
coords2 = [0, 0, 0, 0]
canv1 = canv2 = None


def click1(e):
    coords1[0] = e.x
    coords1[1] = e.y


def click2(e):
    coords2[0] = e.x
    coords2[1] = e.y


def drag1(e):
    coords1[2] = e.x
    coords1[3] = e.y
    canv1.create_line(coords1[0], coords1[1], coords1[2], coords1[3], width=3)
    coords1[0] = coords1[2]
    coords1[1] = coords1[3]


def drag2(e):
    coords2[2] = e.x
    coords2[3] = e.y
    canv2.create_line(coords2[0], coords2[1], coords2[2], coords2[3], width=3)
    coords2[0] = coords2[2]
    coords2[1] = coords2[3]


def clearCanvas(canvas):
    canvas.delete("all")
    canvas.create_text(
        260, 50, fill="black", font="Roboto 16", text="Click and drag to draw")

def mouseOut():
    constants.flagSave = True
    gui_base.switchLayout(constants.MENU)

class Mouse(gui_base.GUI):
    def __init__(self):
        super().__init__()

    def setup(self):
        global btnTest, canv1, canv2
        btnTitle = Button(
            self.frame,
            image=constants.imgLogo,
            font=constants.fontTitle2,
            command=mouseOut,
            relief="flat")
        btnTitle.grid(columnspan=5)
        constants.lblMouseStream = Label(self.frame)
        chk1 = Checkbutton(self.frame, text="Checkbox 1", font=constants.fontText)
        chk2 = Checkbutton(self.frame, text="Checkbox 2", font=constants.fontText)
        btnTest = Button(
            self.frame, text="Click me!", relief="solid", command=changeColor, font=constants.fontText)
        w, h = 400, 300
        canv1 = Canvas(
            self.frame, width=w, height=h, relief="solid", borderwidth=1)
        canv2 = Canvas(
            self.frame, width=w, height=h, relief="solid", borderwidth=1)
        btnClear1 = Button(
            self.frame,
            text="Clear canvas",
            font=constants.fontText,
            command=lambda: clearCanvas(canv1),
            relief="solid")
        btnClear2 = Button(
            self.frame,
            text="Clear canvas",
            font=constants.fontText,
            command=lambda: clearCanvas(canv2),
            relief="solid")

        chk1.grid(pady=50)
        chk2.grid(pady=50)
        btnTest.grid(pady=50, padx=10)

        canv1.grid(padx=50, pady=150)
        canv2.grid(padx=50, pady=150)

        btnClear1.grid(padx=150, pady=50)
        btnClear2.grid(padx=150, pady=50)

        clearCanvas(canv1)
        clearCanvas(canv2)

        canv1.bind("<ButtonPress-1>", click1)
        canv1.bind("<B1-Motion>", drag1)

        canv2.bind("<ButtonPress-1>", click2)
        canv2.bind("<B1-Motion>", drag2)

        super().addElement(btnTitle, 0, 0)
        super().addElement(constants.lblMouseStream, 1, 1)
        super().addElement(canv1, 1, 0)
        super().addElement(canv2, 1, 2)
        super().addElement(btnClear1, 2, 0)
        super().addElement(btnClear2, 2, 2)
        super().addElement(chk1, 3, 0)
        super().addElement(chk2, 3, 1)
        super().addElement(btnTest, 3, 2)

        super().configureGrid()
        center, side = 1, 5
        Grid.columnconfigure(self.frame, 1, weight=center)
        Grid.columnconfigure(self.frame, 0, weight=side)
        Grid.columnconfigure(self.frame, 2, weight=side)
        constants.frames[constants.MOUSE] = self.frame


def changeColor():
    global i, btnTest
    if btnTest is not None:
        colors = [
            "red", "orange", "yellow", "green", "blue", "indigo",
            constants.root.cget("bg")
        ]
        btnTest.configure(bg=colors[i])
        i += 1
        i %= len(colors)
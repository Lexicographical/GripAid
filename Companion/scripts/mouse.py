import cv2
import numpy as np
import pyautogui as gui
import pickle
from threading import Thread
import constants
from PIL import Image, ImageTk

gui.FAILSAFE = False

def top(collection, key, n):
    collection = sorted(collection, key = key, reverse = True)
    returnable = []
    for i in range(n):
        returnable.append(collection[i])
    return returnable

# lower = np.array([30, 133, 140])
lower = np.array([255, 255, 255])
upper = np.array([255, 255, 255])
screen_width, screen_height = gui.size()
frame_width, frame_height = 640, 480
center, old_center = [[0,0]] * 2, [[0,0]] * 2          # center of 2 fingers together or 2 fingers separate
area1 = area2 = 0
damping = 0.5
sx, sy = (screen_width/frame_width)/damping, (screen_height/frame_height)/damping

is_mouse_down = False

# flags for 0 fingers, 1 finger and 2 finger
flags = [True, False, False] 

# frame count for 0 fingers, 1 finger and 2 fingers
finger_frame_count = [0, 0, 0]
cam = None

# Frames threshold for left click
lc_thresh = 5
#  Frames threshold for right click
rc_thresh = 10

def start_mouse():
    global cam, lower, upper
    with open("range.pickle", "rb") as f:
        t = pickle.load(f)
        lower = np.array([t[0], t[1], t[2]])                       # HSV green lower
        upper = np.array([t[3], t[4], t[5]])
    cam = cv2.VideoCapture(1)
    if cam.read()[0]==False:
        cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    render()
    
def render():
    global lower, upper, frame_width, frame_height, center, old_center, area1, area2, damping, sx, sy
    global is_mouse_down, flags, finger_frame_count, cam
    _, img = cam.read()
    img = cv2.flip(img, 1)
    bordersize=1
    img=cv2.copyMakeBorder(img, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType= cv2.BORDER_CONSTANT, value=0 )
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, lower, upper)
    blur = cv2.medianBlur(mask, 15)
    blur = cv2.GaussianBlur(blur , (5,5), 0)
    thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    thresh = cv2.dilate(thresh, np.ones((5, 5), np.uint8), iterations=3)
    contours = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[1]
    mposx, mposy = gui.position()

    #print(flags)
    if len(contours) >= 2:
        old_center[0] = center[0]
        if is_mouse_down:
            Thread(target=gui.mouseUp, args=()).start()
            is_mouse_down = False
        # if left click was done
        if flags[1] == True:
            is_mouse_down = False

            # do a right click if the fingers were together for 10-20 frames and then released
            if finger_frame_count[1] >= lc_thresh and finger_frame_count[1] <= rc_thresh:
                # pass
                gui.rightClick()
            # else if fingers were together for less than 10 frames then do a left click
            elif finger_frame_count[1] < lc_thresh:
                # pass
                gui.click()
            finger_frame_count[1] = 0
        finger_frame_count[2] += 1

        c1, c2 = top(contours, cv2.contourArea, 2)

        rect1 = cv2.minAreaRect(c1)
        (w, h) = rect1[1]
        area1 = w*h
        center1 = np.int0(rect1[0])
        box = cv2.boxPoints(rect1)
        box = np.int0(box)
        cv2.drawContours(img,[box],0,(0,0,255),2)

        rect2 = cv2.minAreaRect(c2)
        (w, h) = rect2[1]
        area2 = w*h
        center2 = np.int0(rect2[0])
        box = cv2.boxPoints(rect2)
        box = np.int0(box)
        cv2.drawContours(img,[box],0,(0,0,255),2)

        center[0] = np.int0((center1 + center2)/2)
        cv2.line(img, tuple(center1), tuple(center2), (255, 0, 0), 2)
        cv2.circle(img, tuple(center[0]), 2, (255, 0, 0), 3)

        if not flags[0]:
            if np.any(abs(center[0] - old_center[0]) > 5):
                Thread(target=gui.moveTo, args=(mposx+(center[0][0]-old_center[0][0])*sx, mposy + (center[0][1]-old_center[0][1])*sy,\
                 0.1, gui.easeInOutQuad)).start()
                # pass

        flags = [False, False, True]      

    elif len(contours) == 1:
        old_center[1] = center[1]
        c1 = max(contours, key = cv2.contourArea)
        rect1 = cv2.minAreaRect(c1)
        (w, h) = rect1[1]
        area3 = w*h
        center[1] = np.array(rect1[0])
        box = cv2.boxPoints(rect1)
        box = np.int0(box)
        cv2.drawContours(img,[box],0,(0,0,255),2)

        error = abs((area1+area2-area3)/area3*100)
        if (error < 40):
            finger_frame_count[1] += 1
            # do a left click and hold if the fingers were together for more than 20 frames
            if finger_frame_count[1] > rc_thresh:
                if not is_mouse_down:
                    gui.mouseDown()
                    is_mouse_down = True
                if np.any(abs(center[1] - old_center[1]) > 5):
                    Thread(target=gui.moveTo, args=(mposx+(center[1][0]-old_center[1][0])*sx, mposy + (center[1][1]-old_center[1][1])*sy, \
                        0.1, gui.easeInOutQuad)).start()     
                    # pass
            flags = [False, True, False]
        else:
            flags = [True, False, False]

    else:
        if is_mouse_down:
            Thread(target=gui.mouseUp, args=()).start()
            # thread.start_new_thread(gui.mouseUp, ())
            is_mouse_down = False
        flags = [True, False, False]

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    timg = Image.fromarray(img).resize(constants.stream_dimens, Image.ANTIALIAS)
    timgtk = ImageTk.PhotoImage(image = timg)
    constants.lblMouseStream.imgtk = timgtk
    constants.lblMouseStream.configure(image = timgtk)

    if constants.flagSave:  
        constants.flagSave = False
        cam.release()
        cv2.destroyAllWindows()
        return

    constants.lblMouseStream.after(1, render)
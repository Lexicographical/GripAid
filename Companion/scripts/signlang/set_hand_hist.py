import cv2
import numpy as np
import pickle
import constants
from PIL import Image, ImageTk
from tkinter import messagebox
import time
import util

cam = None
imgCrop = hist = None
pic = vstream = raw = None

def build_squares(img):
	x, y, w, h = 450, 180, 13, 13
	d = 10
	imgCrop = None
	x1, y1 = x, y
	for i in range(10):
		for j in range(5):
			if np.any(imgCrop is None):
				imgCrop = img[y:y + h, x:x + w]
			else:
				imgCrop = np.vstack((imgCrop, img[y:y + h, x:x + w]))
			x += w + d
		x = 420
		y += h + d
	cv2.rectangle(img, (x1, y1), (x1 + (w + d) * 5, y1 + (h + d) * 5), (0, 255, 0), 2)
	return imgCrop

def get_hand_hist():
	global cam
	cam = cv2.VideoCapture(1)
	if cam.read()[0]==False:
		cam = cv2.VideoCapture(0)
	cam.set(cv2.CAP_PROP_FRAME_WIDTH, constants.frame_width)
	cam.set(cv2.CAP_PROP_FRAME_HEIGHT, constants.frame_height)
	render()

flagC = False

def render():
	global cam, imgCrop, hist, pic, flagC
	img = cam.read()[1]
	img = cv2.flip(img, 1)
	bordersize=1
	img=cv2.copyMakeBorder(img, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType= cv2.BORDER_CONSTANT, value=0 )
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	thresh = None
	if constants.flagCalibrate:
		constants.flagCalibrate = False
		constants.calibrated = True
		flagC = True
		print("recalibrate")
		hsvCrop = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2HSV)
		hist = cv2.calcHist([hsvCrop], [0, 1], None, [180, 256], [0, 180, 0, 256])
		cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
	elif constants.flagSave:
		constants.flagSave = False
		print("Stopped cam")
		cam.release()
		cv2.destroyAllWindows()
		with open("hist", "wb")as f:
			pickle.dump(hist, f)
		constants.streamState = True
		return	
	if flagC:
		dst = cv2.calcBackProject([hsv], [0, 1], hist, [0, 180, 0, 256], 1)
		disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
		cv2.filter2D(dst, -1, disc, dst)
		blur = cv2.GaussianBlur(dst, (11, 11), 0)
		blur = cv2.medianBlur(blur, 15)
		ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		thresh = cv2.merge((thresh, thresh, thresh))
		res = cv2.bitwise_and(img, thresh)
		# cv2.imshow("res", thresh)
	if not constants.flagSave:
		imgCrop = build_squares(img)
	if constants.streamState or not flagC:
		pic = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		build_squares(pic)
	else:
		cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB)
		build_squares(thresh)
		pic = thresh
	timg = Image.fromarray(pic).resize(constants.stream_dimens, Image.ANTIALIAS)
	timgtk = ImageTk.PhotoImage(image = timg)
	constants.lblTypeCalibrateStream.imgtk = timgtk
	constants.lblTypeCalibrateStream.configure(image = timgtk)
	constants.lblTypeCalibrateStream.after(1, render)
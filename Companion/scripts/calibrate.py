import cv2
import numpy as np
import pickle
import constants
from PIL import Image, ImageTk
from tkinter import messagebox
import time
import util

cam = None
imgCrop = None
pic = vstream = raw = None

def build_squares(img):
	x, y, w, h = 420, 140, 10, 10
	d = 5
	imgCrop = None
	x1, y1 = x, y
	x2 = (x1 + (w + d) * 5)
	y2 = (y1 + (h + d) * 5)
	cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
	return img[y1:y2, x1:x2]

def calibrate():
	global cam
	cam = cv2.VideoCapture(constants.camera_driver)
	render()

def render():
	global cam, imgCrop, hist, pic
	img = cam.read()[1]
	img = cv2.flip(img, 1)
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	thresh = None
	if constants.flagCalibrate:
		constants.flagCalibrate = False
		print("recalibrate")
		hsvCrop = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2HSV)
		hist = cv2.calcHist([hsvCrop], [0, 1], None, [150, 256], [0, 150, 0, 256])
		cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
		constants.hist = hist
		constants.calibrated = True
	elif constants.flagSave:
		print("Stopped cam")
		cam.release()
		cv2.destroyAllWindows()
		constants.flagSave = False
		with open("hist", "wb")as f:
			pickle.dump(constants.hist, f)
		return
	if constants.calibrated:
		dst = cv2.calcBackProject([hsv], [0, 1], constants.hist, [0, 150, 0, 256], 1)
		disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
		cv2.filter2D(dst, -1, disc, dst)
		blur = cv2.GaussianBlur(dst, (11, 11), 0)
		blur = cv2.medianBlur(blur, 15)
		ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		thresh = cv2.merge((thresh, thresh, thresh))
		res = cv2.bitwise_and(img, thresh)
		# cv2.imshow("res", res)
	if not constants.flagSave:
		imgCrop = build_squares(img)
	if not constants.streamState:
		pic = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		build_squares(pic)
	else:
		# cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB)
		build_squares(thresh)
		pic = thresh
	timg = Image.fromarray(pic).resize(constants.stream_dimens, Image.ANTIALIAS)
	timgtk = ImageTk.PhotoImage(image = timg)
	constants.lblCalibrateStream.imgtk = timgtk
	constants.lblCalibrateStream.configure(image = timgtk)
	constants.lblCalibrateStream.after(1, render)
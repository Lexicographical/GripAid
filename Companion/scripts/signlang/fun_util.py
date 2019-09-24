import cv2, pickle
import numpy as np
import tensorflow as tf
from cnn_tf import cnn_model_fn
import os
import sqlite3
from keras.models import load_model
import constants
from PIL import Image, ImageTk
from threading import Thread
import util
import time

speaking = True
vstream = raw = None

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
model = load_model('signlang/cnn_model_keras2.h5')
file = open("dump.txt", "w")

def get_image_size():
	img = cv2.imread('signlang/gestures/0/100.jpg', 0)
	return img.shape

image_x, image_y = get_image_size()

def write_word(text):
	print("Wrote:", text)
	try:
		file.write(text)
		file.flush()
		os.fsync(file.fileno())
	except Exception:
		pass

def keras_process_image(img):
	img = cv2.resize(img, (image_x, image_y))
	img = np.array(img, dtype = np.float32)
	img = np.reshape(img, (1, image_x, image_y, 1))
	return img

def keras_predict(model, image):
	processed = keras_process_image(image)
	pred_probab = model.predict(processed)[0]
	pred_class = list(pred_probab).index(max(pred_probab))
	return max(pred_probab), pred_class

def get_pred_text_from_db(pred_class):
	conn = sqlite3.connect("signlang/gesture_db.db")
	cmd = "SELECT g_name FROM gesture WHERE g_id=" + str(pred_class)
	cursor = conn.execute(cmd)
	for row in cursor:
		return row[0]

def get_hand_hist():
	with open("hist", "rb")as f:
		hist = pickle.load(f)
	return hist

came = None
x, y, w, h = 300, 100, 300, 300
hist = None
text = word = ""
count_frame = 0

def recognize():
	global cam, hist
	cam = cv2.VideoCapture(1)
	if cam.read()[0]==False:
		cam = cv2.VideoCapture(0)
	cam.set(cv2.CAP_PROP_FRAME_WIDTH, constants.frame_width)
	cam.set(cv2.CAP_PROP_FRAME_HEIGHT, constants.frame_height)
	hist = get_hand_hist()
	render()

def render():
	global cam, hist, text, word, count_frame
	img = cam.read()[1]
	img = cv2.flip(img, 1)
	imgCrop = img[y:y + h, x:x + w]
	imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	dst = cv2.calcBackProject([imgHSV], [0, 1], hist, [0, 180, 0, 256], 1)
	disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
	cv2.filter2D(dst, -1, disc, dst)
	blur = cv2.GaussianBlur(dst, (11, 11), 0)
	blur = cv2.medianBlur(blur, 15)
	thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
	thresh = cv2.merge((thresh, thresh, thresh))
	thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
	fullthresh = thresh
	thresh = thresh[y:y + h, x:x + w]
	contours = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[1]

	old_text = text
	if len(contours) > 0:
		contour = max(contours, key = cv2.contourArea)
		#print(cv2.contourArea(contour))
		if cv2.contourArea(contour) > 10000:
			x1, y1, w1, h1 = cv2.boundingRect(contour)
			save_img = thresh[y1:y1 + h1, x1:x1 + w1]
			
			if w1 > h1:
				save_img = cv2.copyMakeBorder(save_img, int((w1 - h1)/2), int((w1 - h1)/2), 0, 0, cv2.BORDER_CONSTANT, (0, 0, 0))
			elif h1 > w1:
				save_img = cv2.copyMakeBorder(save_img, 0, 0, int((h1 - w1)/2), int((h1 - w1)/2), cv2.BORDER_CONSTANT, (0, 0, 0))
			pred_probab, pred_class = keras_predict(model, save_img)
			print(pred_class, pred_probab)
			if pred_probab * 100 > 70:
				text = get_pred_text_from_db(pred_class)

			if old_text == text:
				count_frame += 1
			else:
				count_frame = 0

			if count_frame == 20:
				word = word + text
		elif cv2.contourArea(contour) < 1000:
			word = word.strip()
			if len(word) > 0:
				print(word)
				write_word(word + " ")
			text = ""
			word = ""
	else:
		word = word.strip()
		if len(word) > 0:
			print(word)
			write_word(word + " ")
		text = ""
		word = ""
	blackboard = np.zeros((200, 640, 3), dtype = np.uint8)
	blackboard[0:3, 0:] = (0, 255, 255)
	#splitted_text = split_sentence(text, 2)
	#put_splitted_text_in_blackboard(blackboard, splitted_text)
	cv2.putText(blackboard, text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255))
	cv2.putText(blackboard, word, (30, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255))
	
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	fullthresh = cv2.cvtColor(fullthresh, cv2.COLOR_GRAY2RGB)

	cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
	cv2.rectangle(fullthresh, (x,y), (x+w, y+h), (0,255,0), 2)
	res = None
	if constants.streamState:
		res = img
	else:
		res = fullthresh
	pic = np.vstack((res, blackboard))
	timg = Image.fromarray(pic).resize(constants.stream_dimens, Image.ANTIALIAS)
	timgtk = ImageTk.PhotoImage(image = timg)
	constants.lblTypeCamStream.imgtk = timgtk
	constants.lblTypeCamStream.configure(image = timgtk)
	if constants.flagSave:
		constants.flagSave = False
		print(word)
		cam.release()
		cv2.destroyAllWindows()
		file.close()
	else:
		constants.lblTypeCamStream.after(10, render)

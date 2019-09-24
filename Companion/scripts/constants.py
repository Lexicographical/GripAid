root = None
frameCache = 0
frames = [0 for i in range(7)]
lblImg = btnSelect = btnDebugMode = img = None
imgHeader = imgLogo = imgExit = imgTitle = imgStart = imgSettings = imgRead = imgSave = imgHand = imgCheck = imgToggle = None
imgMouse = imgKeyboard = imgHand = None
lblCalibrateStream = None
lblTypeCalibrateStream = lblTypeCamStream = None
lblMouseStream = None
start = True
camera_driver = 0
flagCalibrate = flagSave = False
streamState = True
calibrated = False
# 640*480
# stream_dimens = (960, 720)
stream_dimens = (640, 480)
frame_width = 640
frame_height = 480

# Frame Keys
# incorporate enums
MAIN = 0
MENU = 1
CALIBRATE = 2
MOUSE = 3
TYPE_MENU = 4
TYPE_CALIBRATE = 5
TYPE_CAM = 6

FLAG_NONE = 0
FLAG_CALIBRATE = 1
FLAG_SAVE = 2

# streamState Keys
NORMAL = False
THRESH = True

hist = None

fontText = ("Roboto", 16)
fontMenu = ("Futura Md BT", 25)
fontTitle = ("Futura Md BT", 50)
fontTitle2 = ("Proxima Nova Alt Rg", 20)
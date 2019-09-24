import constants


def activateFlag(flag):
    constants.flagCalibrate = flag & constants.FLAG_CALIBRATE
    constants.flagSave = flag & constants.FLAG_SAVE

def toggleStreamState():
    if constants.calibrated:
        constants.streamState = not constants.streamState
import cv2
import pynetworktables

videoCapture = None
visionTable = None

def main():
	videoCapture = cv2.videoCapture(0)
	setupVisionTable()
	runVision()
	releaseCapture()

def setupVisionTable():
	global visionTable
	NetworkTable.SetIpAddress("10.46.69.2")
	NetworkTable.SetClientMode()
	NetworkTable.Initialize()
	visionTable = NetworkTable.getTable("vision")

def runVision():
	global visionTable
	while(True):
		if visionTable.isConnected() and getRunVision():
			frame1 = getCameraImage()
			turnOnLight()
			frame2 = getCameraImage()
			turnOffLight()
			processedFrame = threshold(getGrayscale(getDifference(frame1, frame2)))
			hull = getConvexHull(getMaxContour(getContours(processedFrame)))
			putValuesOnVisionTable(hull)
			setRunVision(False)

def putValuesOnVisionTable(hull):
	return

def setRunVision(b):
	global visionTable
	visionTable.putBoolean("runVision", b)

def getRunVision():
	global visionTable
	return visionTable.getBoolean("runVision", False)

def releaseCapture():
	global videoCapture
	videoCapture.release()

def turnOnLight():
	global visionTable
	if (visionTable.getBoolean("lightOn", True) == False):
		visionTable.putBoolean("lightOn", True)
		while(True):
			if (getLightOnDone()):
				return

def getLightOnDone():
	global visionTable
	return visionTable.getBoolean("lightOnDone", False)

def turnOffLight():
	global visionTable
	if (visionTable.getBoolean("lightOn", False) == True):
		visionTable.putBoolean("lightOn", False)
		while(True):
			if(getLightOnDone() == False):
				return

def getCameraImage():
	global videoCapture
	retval, frame = videoCapture.read()
	return frame

def getDifference(frame1, frame2):
	diff = cv2.subtract(frame2, frame1)
	return diff

def getGrayscale(frame):
	grayscale = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
	return grayscale

def threshold(frame):
	newFrame = cv2.threshold(frame, 50, 255, cv2.THRESH_BINARY)
	return newFrame

def getContours(frame):
	contoursList, hierarchy = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	return contoursList

def getMaxContour(contoursList):
	maxContour = None
	if (len(contoursList)>0):
		maxContour = contoursList[0]
		maxArea = cv2.contourArea(maxContour)
		for contour in contoursList:
			area = cv2.contourArea(contour)
			if (area>maxArea):
				maxContour = contour
				maxArea = area
	return maxContour

def getConvexHull(contour):
	hull = cv2.convexHull(contour)
	return hull

main()
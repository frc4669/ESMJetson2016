import cv2
import time
from networktables import NetworkTable

videoCapture = None
visionTable = None

def main():
	global videoCapture
	videoCapture = cv2.VideoCapture()
	videoCapture.open(0)
	if (videoCapture.isOpened()):
		print("Camera is open")
	else:
		print("Camera is NOT open")
	setupVisionTable()
	runVision()
	releaseCapture()

def setupVisionTable():
	global visionTable
	NetworkTable.setIPAddress("10.46.69.21")
	NetworkTable.setClientMode()
	NetworkTable.initialize()
	visionTable = NetworkTable.getTable("vision")

def runVision():
	global visionTable
	while(True):
		#print(visionTable.isConnected())
		#print(getRunVision())
		if visionTable.isConnected() and getRunVision():
			frame1 = getCameraImage()
			turnOnLight()
			time.sleep(1)
			frame2 = getCameraImage()
			turnOffLight()
			processedFrame = threshold(getGrayscale(getDifference(frame1, frame2)))
			hull = getConvexHull(getMaxContour(getContours(processedFrame)))
			putValuesOnVisionTable(hull)
			setRunVision(False)

def putValuesOnVisionTable(hull):
	print("Success")
	print(hull)

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
	visionTable.putBoolean("lightOn", True)
	while(True):
		if (getLightOnDone()):
			return

def getLightOnDone():
	global visionTable
	return visionTable.getBoolean("lightOnDone", False)

def turnOffLight():
	global visionTable
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
	grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	return grayscale

def threshold(frame):
	th, newFrame = cv2.threshold(frame, 50, 255, cv2.THRESH_BINARY)
	return newFrame

def getContours(frame):
	contoursList, hierarchy = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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

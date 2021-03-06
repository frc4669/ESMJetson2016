import cv2
from networktables import NetworkTable

videoCapture = None
visionTable = None

#image size is 640x480

def main():
	global videoCapture
	videoCapture = cv2.VideoCapture()
	setupVisionTable()
	runVision()

def setupVisionTable():
	global visionTable
	NetworkTable.setIPAddress("10.46.69.21")
	NetworkTable.setClientMode()
	NetworkTable.initialize()
	visionTable = NetworkTable.getTable("vision")
	setRunVision(False)
	turnOffLight()

def runVision():
	global visionTable
	while(True):
		#print(visionTable.isConnected())
		#print(getRunVision())
		if visionTable.isConnected() and getRunVision():
			for i in xrange(30):
				frame1 = getCameraImage()
			#cv2.namedWindow("frame1", cv2.WINDOW_NORMAL)
			#cv2.imshow("frame1", frame1)
			#cv2.imwrite("frame1.jpg", frame1)
			turnOnLight()
			cv2.waitKey(100)
			for i in xrange(30):
				frame2 = getCameraImage()
			#cv2.namedWindow("frame2", cv2.WINDOW_NORMAL)
			#cv2.imshow("frame2", frame2)
			#cv2.imwrite("frame2.jpg", frame2)
			cv2.waitKey(100)
			turnOffLight()
			processedFrame = threshold(getGrayscale(getDifference(frame1, frame2)))
			hull = getConvexHull(getMaxContour(getContours(processedFrame)))
			putValuesOnVisionTable(hull)
			setRunVision(False)

def putValuesOnVisionTable(hull):
	x,y,w,h = cv2.boundingRect(hull)
	#print("Success")
	print(x,y,w,h)
	visionTable.putNumber("x", x)
	visionTable.putNumber("y", y)
	visionTable.putNumber("w", w)
	visionTable.putNumber("h", h)

def setRunVision(b):
	global visionTable
	visionTable.putBoolean("runVision", b)

def getRunVision():
	global visionTable
	return visionTable.getBoolean("runVision", False)

def openCapture():
	global videoCapture
	while (not videoCapture.isOpened()):
		print("Camera is NOT open")
		videoCapture.open(0)
	#print("Camera is open")
	#videoCapture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1920)
	#videoCapture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 1080)

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
	#videoCapture = cv2.VideoCapture()
	openCapture()
	retval, frame = videoCapture.read()
	#releaseCapture()
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

import cv2
import time

camera_port = 0
ramp_frames = 30
firstim = 0
secondim = 0

camera = cv2.VideoCapture(camera_port)

def get_image():
 retval, im = camera.read()
 return im

for frame in (1,2):
	if frame == 1:
	 for i in xrange(ramp_frames):
	  temp = get_image()
	 print("Taking first image...")
	 firstim = get_image()
	 print("sleep")
	 time.sleep(5)
	elif frame == 2:
	 for i in xrange(ramp_frames):
	  temp = get_image()
	 print("Taking second image...")
	 secondim = get_image()
	
	del(temp)
cv2.imwrite("image1.png", firstim)
cv2.imwrite("image2.png", secondim)

subbed_image = cv2.subtract(firstim,secondim)
subbed_grayscale = cv2.cvtColor(subbed_image, cv2.COLOR_BGR2GRAY)

cv2.imwrite("imagediff.png", subbed_grayscale)

maxArea=0
maxIdx=-1

src = subbed_grayscale

thresh = 50 
maxValue = 255

th, dst = cv2.threshold(src, thresh, maxValue, cv2.THRESH_BINARY);

contours,hierarchy=cv2.findContours(dst,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

i=0
for ct in contours:
	area=cv2.contourArea(ct)
	if area > maxArea:
		maxArea = area
		maxIdx = i
	print(i,area)	
	i=i+1

cnt=contours[maxIdx]
hull=cv2.convexHull(cnt)
print(hull)

print(maxIdx)

cv2.drawContours(dst,[hull],0,(255,255,255),2) #-1,3
cv2.imwrite("img_contour.png", dst)

cv2.namedWindow("Contour", cv2.WINDOW_NORMAL)
cv2.imshow("Contour",dst)
cv2.waitKey(0)

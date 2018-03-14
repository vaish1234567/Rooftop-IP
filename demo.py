import cv2 
import numpy as np
import imutils
from imutils import contours
from scipy.spatial import distance as dist
from imutils import perspective
from matplotlib import pyplot as plt


# Read image
src = cv2.imread("img.png", cv2.IMREAD_GRAYSCALE)
org = cv2.imread("img.png")
plt.subplot(221),plt.imshow(org,cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])


# threshold image
blur = cv2.GaussianBlur(src,(5,5),0)
ret, threshed_img = cv2.threshold(blur,100,200, cv2.THRESH_BINARY)
#threshed_img = cv2.adaptiveThreshold(src, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 45, 10)
#print ret
#Edges Detection
edges = cv2.Canny(threshed_img,100,250)
plt.subplot(222),plt.imshow(edges,cmap = 'gray')
plt.title('Edges'), plt.xticks([]), plt.yticks([])

threshed_img=threshed_img+edges

# find contours and get the external one
image, contours, hier = cv2.findContours(threshed_img, cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
max_area = -1
for c in contours:
	area=cv2.contourArea(c) 
	print area
	if area > max_area:
		max_area=area

for c in contours: 
	# get the bounding rect
	x, y, w, h = cv2.boundingRect(c)
	area=cv2.contourArea(c)
	#print(area)
	if area == max_area:

	# draw a white rectangle to visualize the bounding rect
		#cv2.rectangle(org, (x, y), (x+w, y+h),(255, 0, 0), 2)
		print x,y,w,h
	# get the min area rect
   		rect = cv2.minAreaRect(c)
    		box = cv2.boxPoints(rect)
    	#convert all coordinates floating point values to int
    		box = np.int0(box)
		width = abs(box[0,0] - box[1,0])
		height = abs(box[0,1] - box[1,1])
		try:
			with open('data.txt','a') as f:
				f.write(str(width)),f.write(','),f.write(str(height)),f.write('\n')
		except IOError as e:
			print("Couldn't open or write to file (%s)." % e)

		#print width,height
		print (box)
    	# draw a red 'nghien' rectangle
    		cv2.drawContours(org, [box], 0, (0, 0, 255),5)
	else:
		continue

#cv2.drawContours(org, contours, -1, (0, 255,0), 2)


font = cv2.FONT_HERSHEY_SIMPLEX
plt.subplot(223),plt.imshow(threshed_img,cmap = 'gray')
plt.title('Binary Thresholding'), plt.xticks([]), plt.yticks([])
plt.subplot(224),plt.imshow(org,cmap = 'gray')
plt.title('Bounding box'), plt.xticks([]), plt.yticks([])
plt.show()
 
cv2.waitKey(0)
cv2.destroyAllWindows()

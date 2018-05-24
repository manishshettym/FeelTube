import numpy as np
import cv2
import imutils
import argparse
import dlib



#EXTRA HELPERS Defined:

#rectangle to bounding box function for face 

def rect_to_bb(rect):
	#takes the bounding that dlib predicts and converts to opencv format
	x= rect.left() #x
	y=rect.top()	#y
	w= rect.right()-x #width
	h=rect.bottom()-y #height

	return (x,y,w,h)

#the dlib face detector returns a shape object containing facial landmarks
# this is converted into a numpy array

def shape_to_np(shape, dtype="int"):
	
	#initilaize with zeros
	coords = np.zeros((68,2),dtype=dtype)

	#loop over 68 facial landmarks to make (x,y) 
	for i in range (0,68):
		coords[i]= (shape.part(i).x , shape.part(i).y)

	return coords



#COOL : creating an argument parser for the command
#-p : path argument
#-i : img argument

ap = argparse.ArgumentParser();
ap.add_argument("-p","--shape-predictor" , required=True , help="path to prediction")
ap.add_argument("-i","--image",required=True,help="path to ip image")
args= vars(ap.parse_args())


#initializing dlib face detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])


#BUT detect face first

image = cv2.imread(args["image"])
image = imutils.resize(image,width=500)
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

rects = detector(gray,1)

#rects now has the x.y coords of the faces

for (i,rect) in enumerate(rects):

	#create the shape object from predictor created

	shape = predictor(gray, rect)
	shape = shape_to_np(shape)

	#draw the bounding box using opencv
	(x, y, w, h) = rect_to_bb(rect)
	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
 
	#marking the face number @(x-10,y-10)
	cv2.putText(image,"Face #{}".format(i+1), (x - 10, y - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

	#drawing the facial landmarks over the image 
	for (x, y) in shape:
		cv2.circle(image, (x, y), 1, (0, 0, 255), -1)


# show the output image with the face detections + facial landmarks
cv2.imshow("Output", image)
cv2.waitKey(0)




import math,itertools,numpy
import cv2
import imutils
import dlib
from collections import OrderedDict

#defining a dictionary that maps the landmark regions points to specific face regions
#NOTE: shape object has (x,y) coords of all points

facial_landmarks_index = OrderedDict([
	("mouth",(48,68)),
	("r_eyebrow",(17,22)),
	("l_eyebrow",(22,27)),
	("r_eye",(36,42)),
	("l_eye",(42,48)),
	("nose",(27,36)),
	("jaw",(0,17))

	])


def generateFeatures(image,shape,colors=None,alpha=0.75):

		#creating copies
		overlay = image.copy()
		output = image.copy()

		#color list for each feature as BGR values(opencv)
		if colors is None:
			colors = [(19, 199, 109), (79, 76, 240), (230, 159, 23),
				(168, 100, 168), (158, 163, 32),
				(163, 38, 32), (180, 42, 220)]

		#alpha= opacity of overlay

		for (i,name) in enumerate(facial_landmarks_index.keys()):

			(j,k)=facial_landmarks_index[name]
			pts= shape[j:k]

			#simply slice the portion of the shape list that has the 
			#range of coordinates for the required features


			if name=="jaw":
				#jaw is actually a non enclosed region so it should not
				#form loops.Thus we cannot use the drawContours method
				#just simply use .line()

				for m in range(1,len(pts)):
					ptstart = tuple(pts[m-1])
					ptend = tuple(pts[m])
					cv2.line(overlay,ptstart,ptend,colors[i],2)

			else:
				hull = cv2.convexHull(pts)
				cv2.drawContours(overlay,[hull],-1,colors[i],-1)



		# apply the transparent overlay
		cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
 
		# return the output image
		return output



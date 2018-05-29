import os
import matplotlib.pyplot as plt
import numpy as np
import cv2
from mpl_toolkits.axes_grid1 import ImageGrid
from skimage.feature import local_binary_pattern as lbp
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.model_selection import KFold as KF
from sklearn.model_selection import cross_val_score


# Here we load the images, and based on the name of the file we identify the
# class, in this case is a number from 1 to 7 that we can find in the 3 and 4th
# character of the filename.

data_path = '/home/manish/ACADEMICS/PROJECTS/EmoVie/jaffe/'
imgs =[]
fs = (12,12)#fixing the size of all images so that accuracy is improved

filenames = sorted(os.listdir(data_path))

#temp=filenames[0]
#print temp[3:5] SLICING used to get data from the filename

classes = {"NE":1 , "HA":2 ,"SA":3, "SU":4,
			 "DI":5,"AN":6,"FE":7}

d = [] #array of classification labels

for img_name in filenames :
	img = cv2.imread(data_path + img_name)
	#This is because cv2 read images in (b,g,r)
	(b, g, r)=cv2.split(img)
	img=cv2.merge([r,g,b])
	imgs.append(img)
	d.append(int(classes[img_name[3:5]]))


imgs = np.asarray(imgs)
d = np.asarray(d)
index = np.random.randint(0,len(imgs)-1,5)


#some of the images are to just view it
plt.figure(figsize=fs)

for i,im in enumerate(imgs[index]):
	plt.subplot(1,5,i+1)
	plt.imshow(im,cmap='gray')
	plt.xticks(())
	plt.yticks(())
	plt.title('IMG'+str(index[i]))
plt.show()




#Using the Local Binary Pattern (LBP) recognizing features

b = [i for i in range(0,55)]
b.append(255)

lbp_imgs = []
lbp_hists = []

for im in imgs:
	im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) #needed to be added because otherwise expected im should be 2d array with rgb
	aux = lbp(im, 8, 28, method='default')
	lbp_imgs.append(aux)

	aux2, _ = np.histogram(aux,bins=b)
	lbp_hists.append(aux2)

lbp_hists = np.asarray(lbp_hists)



#some of the histograms are to jsut view it
plt.figure(figsize=(12,2))

for i,hist in enumerate(lbp_hists[index]):
    plt.subplot(1, 5, i+1)
    plt.bar(b[:len(b)-2], hist[:len(hist)-1])
    plt.xticks(())
    plt.yticks(())
    plt.xlim(5)
    plt.title('HIST' + str(index[i]))
plt.show()


# Now we will try to predict the emotions represented in five random images
# training a simple classifier with the rest. The classifier that we will use
# is the K-Nearest Neighbor (KNN).

# In this step we divide the dataset in training and testing images.
# This can be performed in many ways, the simplest one is K-Fold.



X = np.asarray(lbp_hists) #array of all thos histograms created
kf = KF(n_splits=30, shuffle=True).split(X) #using 30 fold split to get train and test datasets

train_indices, test_indices =  next(kf)
print('Training images:', train_indices, '\n')
print('Testing images:', test_indices, '\n')

X_train = X[train_indices] #lbp hists of training data
y_train = d[train_indices] #(1-7)labels of the training data

X_test = X[test_indices] #lbp hists of test data
y_test = d[train_indices] #(1-7)labels of the test data


knn = KNN(n_neighbors=1).fit(X_train, y_train) # fit(featuresmatirx , classlabels)
class_prediction = knn.predict(X_test) #predict for testmatrix

print('Predicted Classes:', class_prediction, '\n')
print('Real Classes:', d[test_indices], '\n') 
# reference from dataset is from https://github.com/X-zhangyang/Real-World-Masked-Face-Dataset
# partial reference for code from https://data-flair.training/blogs/face-mask-detection-with-python/ and https://towardsdatascience.com/how-i-built-a-face-mask-detector-for-covid-19-using-pytorch-lightning-67eb3752fd61
# learnt about deep learning from https://www.youtube.com/watch?v=iCPvzMpLl88
# importing all the packages used in the code
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.utils import to_categorical
from imutils import paths 
import matplotlib.pyplot as plt
import numpy as np
# reference for sklearn library from the following video https://www.youtube.com/watch?v=0Lt9w-BxKFQ
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os

# initialize the initial learning rate, number of epochs to train for,
# and batch size
INIT_LR = 1e-4   # slow learning rate results in less to get better accuracy
EPOCHS = 20
BS = 32

dir_path = os.path.dirname(os.path.realpath(__file__))
dataset_path = dir_path + "/dataset"

DIRECTORY = dataset_path  #reffering to the dataset in the same folder, used to train our model
CATEGORIES = ["people_wearing_masks", "people_not_wearing masks"]  # name of the 2 files 

# grab the list of images in our dataset directory, then initialize
# the list of data (i.e., images) and class images


data = []      #to append all the image array
labels = []    # label of the image whether they are with or without mask

for category in CATEGORIES:     #looping through both the folders in dataset
    path = os.path.join(DIRECTORY, category)  #to get the path of the folder (people_wearing_masks and people_not_wearing_masks)
    for img in os.listdir(path):              #lists all the images inside directory
    	img_path = os.path.join(path, img)  #concatinating path components to get the location of the image 
    	image = load_img(img_path, target_size=(224, 224))  #load_img comes from kera(line 13), target makes a common height and width of photographs
    	image = img_to_array(image)          #imported from keras(line 12)
    	image = preprocess_input(image)      #because we are using mobile nets


    	data.append(image)       # we append the array to the data list
    	labels.append(category)  # categories are with mask and without mask

# perform one-hot encoding on the labels
lb = LabelBinarizer()    # converting people_wearing_masks and people_not_wearing_masks to numerical values since the labels are in alphabets
labels = lb.fit_transform(labels)
labels = to_categorical(labels)

data = np.array(data, dtype="float32") # converting the data into numpy array
labels = np.array(labels)

(trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.20, stratify=labels, random_state=42) 
 # using train_test_split to split our data to test and training, here we use 20% test and 80% to train
# construct the training image generator for data augmentation, basically createing more datasets with the images we have
# referenced from online code (i cannot find the link where i got this from)
aug = ImageDataGenerator(
	rotation_range=20,
	zoom_range=0.15,
	width_shift_range=0.2,
	height_shift_range=0.2,
	shear_range=0.15,
	horizontal_flip=True,
	fill_mode="nearest")


# load the MobileNetV2 network, ensuring the head FC layer sets are
# left off
baseModel = MobileNetV2(weights="imagenet", include_top=False,
	input_tensor=Input(shape=(224, 224, 3))) #input tensor is shape of the image(3 is the three channels, red green and blue), include fully connected layer at top of our network is set to false

# construct the head of the model that will be placed on top of the the base model
headModel = baseModel.output
headModel = AveragePooling2D(pool_size=(7, 7))(headModel)
headModel = Flatten(name="flatten")(headModel)
headModel = Dense(128, activation="relu")(headModel) #relu because we are dealing with images
headModel = Dropout(0.5)(headModel) # to preventing overfitting
headModel = Dense(2, activation="softmax")(headModel)  # 2 because we have 2 type of images

# place the head FC model on top of the base model (this will become
# the actual model we will train)
model = Model(inputs=baseModel.input, outputs=headModel)

# looping over all layers in the base model and freeze them so they will not be updated during the first training process
for layer in baseModel.layers:
	layer.trainable = False

# compile our model
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
model.compile(loss="binary_crossentropy", optimizer=opt,
	metrics=["accuracy"])

# train the head of the network
H = model.fit(
	aug.flow(trainX, trainY, batch_size=BS),
	steps_per_epoch=len(trainX) // BS,
	validation_data=(testX, testY),
	validation_steps=len(testX) // BS,
	epochs=EPOCHS)




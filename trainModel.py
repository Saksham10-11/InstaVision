import os
import cv2
import pickle
import numpy as np
from sklearn.svm import SVC
from keras_facenet import FaceNet
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.calibration import CalibratedClassifierCV

# Load the requiresd images 
def loadImages(DIRPath):
    images = []
    lables = []
    for filename in os.scandir(DIRPath):
        img = cv2.imread(filename.path)
        images.append(img)
        lables.append(0)
    falseImgDIRPath = "Drop_Your_Training_Images_HERE/false_images"
    for filename in os.scandir(falseImgDIRPath):
        img = cv2.imread(filename.path)
        images.append(img)
        lables.append(1)
    return images,lables

# Get the multidimesional vector space of images
def get_embeddings(images):
    embedder = FaceNet()
    embedded_images = []
    for image in images:
        image = image.astype('float32')
        # Convert the 3D image to 4D image
        image = np.expand_dims(image, axis=0) # 4D (Nonex160x160x3)
        yhat= embedder.embeddings(image)  # Returns a list of lsit
        embedded_images.append(yhat[0])
    # Convert into numpy array
    embedded_images=np.asarray(embedded_images)
    return embedded_images

# Trainig the actual model
def train_model(embedded_images,lables,searchParam):
    # Path to save the model
    DIR = "Saved_Models/"+searchParam
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    SVM_model_path = "Saved_Models/"+searchParam+"/SVM_model.pkl"
    Calibrated_SVC_path = "Saved_Models/"+searchParam+"/Calibrated_SVC.pkl"
    encoder = LabelEncoder()
    encoder.fit(lables)
    y = encoder.transform(lables)
    X_train, X_test, y_train, y_test = train_test_split(embedded_images, y, test_size=0.2, random_state=42)
    model = SVC(kernel = "linear",probability=True)    
    model.fit(X_train,y_train)
    #save the model
    with open(SVM_model_path,'wb') as f:
        pickle.dump(model,f)
    yPreds_test = model.predict(X_test)
    conf = accuracy_score(y_test,yPreds_test)
    print("Model's accuracy score : ",conf)
    calibrated_svc = CalibratedClassifierCV(model, method='sigmoid', cv='prefit')
    calibrated_svc.fit(X_train, y_train)
    with open(Calibrated_SVC_path,'wb') as f:
        pickle.dump(calibrated_svc,f)

def automateTrainingModel(DIRPath,searchParam):
    images,lables = loadImages(DIRPath)
    embedded_images=get_embeddings(images)
    train_model(embedded_images,lables,searchParam)
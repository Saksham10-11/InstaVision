import cv2
from ultralytics import YOLO
from utils import createDIR,copyFiles,getFilePaths,checkIfAvailable
from prepareImages import processImage
import os
import cv2
import pickle
import numpy as np
from ultralytics import YOLO
from keras_facenet import FaceNet

# ID's of objects that pre-trained YOLO model can detect
MAX_DEFAULT_SUPPORTED_ID = 79

def organize(dirPath,searchParam):
    imageFilePaths,vidFilePaths = getFilePaths(dirPath)
    ID , isValid = checkIfAvailable(searchParam)
    if isValid==True:
        if len(imageFilePaths)>0:
            organizeImages(ID,imageFilePaths,dirPath,searchParam)
        if len(vidFilePaths)>0:
            organizeVids(ID,vidFilePaths,dirPath,searchParam)

def organizeImages(ID,filePaths,dirPath,searchParam):
    if(ID <= MAX_DEFAULT_SUPPORTED_ID):
        organizeImagesUsingDefaultModel(ID,filePaths,dirPath)
    else :
        organizeImagesUsingCustomModel(ID,filePaths,dirPath,searchParam)

def organizeVids(ID,filePaths,dirPath,searchParam):
    if(ID <= MAX_DEFAULT_SUPPORTED_ID):
        organizeVideosUsingDefaultModel(ID,filePaths,dirPath)
    else:
        pass

def organizeImagesUsingDefaultModel(ID,filePaths,dirPath):
    filteredImages = getFilteredImagesUsingDefaultModel(ID,filePaths)
    if(len(filteredImages)>0):
        destinationFolder = createDIR(dirPath,ID,"Images")
        copyFiles(filteredImages,destinationFolder)
    else:
        print("No matches found !!")
    print("Done Organizing Images !!")

def organizeVideosUsingDefaultModel(ID,filePaths,dirPath):
    filteredVideos = getFilteredVideosUsingDefaultModel(ID,filePaths)
    if(len(filteredVideos)>0):
        destinationFolder = createDIR(dirPath,ID,"Videos")
        copyFiles(filteredVideos,destinationFolder)
    else:
        print("No matches found !!")
    print("Done Organizing Videos !!")

def getFilteredImagesUsingDefaultModel(ID,filePaths):
    model = YOLO('Saved_Models/yolov8m.pt')
    filteredImagePaths = []
    for filePath in filePaths:
        results = model(filePath)
        boxs = results[0].boxes
        for box in boxs:
            class_id = box.cls[0].item()
            class_id = int(class_id)
            conf = round(box.conf[0].item(), 2)
            if class_id==ID and conf > 0.7 :
                print("Added images")
                filteredImagePaths.append(filePath)
        print("Processed Image : ",filePath)
    return filteredImagePaths

def getFilteredVideosUsingDefaultModel(ID,filePaths):
    model = YOLO('Saved_Models/yolov8m.pt')
    filteredVideoPaths= []
    for filePath in filePaths:
        cap = cv2.VideoCapture(filePath)
        fps = cap.get(cv2.CAP_PROP_FPS)
        fps = int(fps)
        totalFramesTested = 0
        validFrames = 0
        while cap.isOpened():
            success, frame = cap.read()
            if success and validFrames < 5:
                totalFramesTested = totalFramesTested + 1
                result = model(frame)
                boxs = result[0].boxes
                for box in boxs:
                    class_id = box.cls[0].item()
                    class_id = int(class_id)
                    conf = round(box.conf[0].item(), 2)
                    if class_id==ID and conf > 0.6 :
                        validFrames = validFrames + 1
                        break
                for _ in range(fps):
                    success,_ = cap.read()
                    if not success :
                        break
            else :
                break
        if (validFrames >= 5) or (totalFramesTested<8 and validFrames > 1):
            filteredVideoPaths.append(filePath)
        print("Processed Video : ",filePath)
    return filteredVideoPaths

def organizeImagesUsingCustomModel(ID,filePaths,dirPath,searchParam):
    filteredImages = getFilteredImagesUsingCustomModel(ID,filePaths,searchParam)
    if(len(filteredImages)>0):
        destinationFolder = createDIR(dirPath,ID,"Images")
        copyFiles(filteredImages,destinationFolder)
    else:
        print("No matches found !!")
    print("Done Organizing Images !!")

def organizeVideosUsingCustomModel(ID,filePaths,dirPath):
    filteredVideos = getFilteredVideosUsingCustomModel(ID,filePaths)
    if(len(filteredVideos)>0):
        destinationFolder = createDIR(dirPath,ID,"Videos")
        copyFiles(filteredVideos,destinationFolder)
    else:
        print("No matches found !!")
    print("Done Organizing Videos !!")

def getFilteredImagesUsingCustomModel(ID,filePaths,searchParam):
    filteredImagePaths = []
    SVM_model_path = "Saved_Models/"+searchParam+"/SVM_model.pkl"
    Caliberated_SVC_path = "Saved_Models/"+searchParam+"/Calibrated_SVC.pkl"
    model = pickle.load(open(SVM_model_path, 'rb'))
    probablity_model = pickle.load(open(Caliberated_SVC_path, 'rb'))
    faceDetector = YOLO("Saved_Models/face-detector.pt")
    facenet = FaceNet()
    for filePath in filePaths:
        frame = cv2.imread(filePath)
        results = faceDetector(frame)
        box_list = []
        probability_list = []
        for box in results[0].boxes:
            x_min,y_min,x_max,y_max= ((box.xyxy).tolist())[0]
            img = processImage(frame,int(x_min),int(x_max),int(y_min),int(y_max))
            img = np.expand_dims(img,axis=0)
            ypred = facenet.embeddings(img)
            face_name = model.predict(ypred)
            probabilities = probablity_model.predict_proba(ypred)
            probablity = probabilities[0][0]
            if face_name == 0 :
                probability_list.append(probablity)
        max_probablity = 0
        if len(probability_list)>0:
            max_probablity = max(probability_list)
        if(max_probablity > 0.75) :
            filteredImagePaths.append(filePath)
        print("Processed Image : ",filePath)
    return filteredImagePaths

def getFilteredVideosUsingCustomModel(ID,filePaths):
    pass
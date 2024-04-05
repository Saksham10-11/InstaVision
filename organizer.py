import cv2
from ultralytics import YOLO
from utils import createDIR,copyFiles

# ID's of objects that pre-trained YOLO model can detect
MAX_DEFAULT_SUPPORTED_ID = 79

def organizeImages(ID,filePaths,dirPath):
    if(int(ID) <= 79):
        organizeImagesUsingDefaultModel(ID,filePaths,dirPath)
    else :
        pass

def organizeVids(ID,filePaths,dirPath):
    if(int(ID) <= 79):
        organizeVideosUsingDefaultModel(ID,filePaths,dirPath)
    else:
        pass

def organizeImagesUsingDefaultModel(ID,filePaths,dirPath):
    filteredPaths = getFilteredImagesUsingDefaultModel(ID,filePaths)
    if(len(filteredPaths)>0):
        destinationFolder = createDIR(dirPath,ID,"Images")
        copyFiles(filteredPaths,destinationFolder)
    else:
        print("No matches found !!")
    print("Done Organizing Images !!")

def organizeVideosUsingDefaultModel(ID,filePaths,dirPath):
    filteredPaths = getFilteredVideosUsingDefaultModel(ID,filePaths)
    if(len(filteredPaths)>0):
        destinationFolder = createDIR(dirPath,ID,"Videos")
        copyFiles(filteredPaths,destinationFolder)
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
        if (validFrames >= 5) or (totalFramesTested<8 and validFrames > 0):
            filteredVideoPaths.append(filePath)
        print("Processed Video : ",filePath)
    return filteredVideoPaths
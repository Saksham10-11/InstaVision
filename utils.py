from ultralytics import YOLO
import pathlib
import shutil
import json
import yaml
import cv2
import os

def getAvailableOptions():
    json_filePath = "available_options.json"
    with open(json_filePath, 'r') as json_file:
        data = json.load(json_file)
    return data

def getFileExtension(path):
    file_extension = pathlib.Path(path).suffix
    return file_extension

def getFilePaths(dirPath):
    supported_vid_extensions=['.asf', '.avi', '.gif', '.m4v', '.mkv', '.mov', '.mp4', '.mpeg', '.mpg', '.ts', '.wmv', '.webm']
    supported_pic_extensions=['.bmp', '.dng', '.jpeg', '.jpg', '.mpo', '.png', '.tif', '.tiff', '.webp', '.pfm']
    imgFilePaths = []
    vidFilePaths = []
    for filename in os.scandir(dirPath):
        if filename.is_file():
            file_extension = getFileExtension(filename.path)
            if file_extension in supported_pic_extensions:
                imgFilePaths.append(filename.path)
            elif file_extension in supported_vid_extensions:
                vidFilePaths.append(filename.path)
            else : # Files other than images or videos are ignored
                pass
    return imgFilePaths,vidFilePaths

def checkIfAvailable(searchParam):
    availableOptions = getAvailableOptions();
    for ID in availableOptions.keys():
        if availableOptions[ID].lower() == searchParam.lower():
            return ID,True
    return -1,False

def createDIR(dirPath,ID,type):
    availableOptions = getAvailableOptions()
    newpath = dirPath+"/"+availableOptions[ID]+"/"+type
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

def copyFiles(filePaths,destinationFolder):
    for filePath in filePaths:
        shutil.copy(filePath, destinationFolder)

def createTrainingDIR():
    os.makedirs("data")
    # Creating DIR for training
    os.makedirs("data/training_data")
    training_imageDIR_path = "data/training_data/images"
    training_lableDIR_path = "data/training_data/labels"
    os.makedirs(training_imageDIR_path)
    os.makedirs(training_lableDIR_path)
    # Creating DIR for validation
    os.makedirs("data/validation_data")
    validation_imageDIR_path = "data/validation_data/images"
    validation_lableDIR_path = "data/validation_data/labels"
    os.makedirs(validation_imageDIR_path)
    os.makedirs(validation_lableDIR_path)

    return training_imageDIR_path,training_lableDIR_path,validation_imageDIR_path,validation_lableDIR_path

def gatherTrainingData():
    training_imageDIR_path,training_lableDIR_path,validation_imageDIR_path,validation_lableDIR_path=createTrainingDIR()
    model = YOLO("Saved_Models/face-detector.pt")
    cap = cv2.VideoCapture(0)
    counter = 1
    while(cap.isOpened()):
        # Provide buffer
        for _ in range(5):
            _,_=cap.read()
        sucess, frame = cap.read()
        if sucess and counter<50:
            frame = cv2.flip(frame,1)
            results = model(frame)
            conf=0
            boxs=results[0].boxes
            if len(boxs)>0:
                conf=round(boxs[0].conf[0].item(),2)
            if conf>0.4:
                if counter < 40:
                    currLablePath = training_lableDIR_path+"/"+str(counter)+".txt"
                    currImagePath = training_imageDIR_path+"/"+str(counter)+".jpg"
                    cv2.imwrite(currImagePath,frame)
                    results[0].save_txt(currLablePath,save_conf=False)
                else :
                    currLablePath = validation_lableDIR_path+"/"+str(counter)+".txt"
                    currImagePath = validation_imageDIR_path+"/"+str(counter)+".jpg"
                    cv2.imwrite(currImagePath,frame)
                    results[0].save_txt(currLablePath,save_conf=False)
                counter=counter+1
            annotated_frame = results[0].plot()
            cv2.imshow("Camera",annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else :
            break
    cv2.destroyAllWindows()

def createConfigFile(searchParam):
    current_directory = os.getcwd()
    config_dict = {
        "path" : current_directory,
        "train":"data/training_data",
        "val":"data/validation_data",
        "names":{0:searchParam}
    }
    with open("custom-config.yaml","w") as f:
        yaml.dump(config_dict,f,default_flow_style=False)

def trainCustomModel(searchParam):
    gatherTrainingData()
    createConfigFile(searchParam)
    model = YOLO('Saved_Models/yolov8m.pt')
    model.train(data="custom-config.yaml",epochs=5)

import os
import cv2
import time
from ultralytics import YOLO

# Prepare the images
def gatherImages(DIRPath , imageCounter):
    model = YOLO("Saved_Models/yolov8n-face.pt")
    cap = cv2.VideoCapture(0)
    imagesCaptured = 0
    while(cap.isOpened() and imagesCaptured<10):
        sucess, frame = cap.read()
        if sucess:
            frame = cv2.flip(frame,1)
            results = model(frame)
            annotated_frame = results[0].plot()
            cv2.imshow("Camera",annotated_frame)
            key = cv2.waitKey(1)
            if key & 0xFF == ord("q"):
                break
            elif key == ord(" "):  # Captures the frame
                dirPath = os.getcwd()
                path = DIRPath+"/"+str(imageCounter)+".jpg"
                x_min,y_min,x_max,y_max= (((results[0].boxes)[0].xyxy).tolist())[0]
                processed_frame = processImage(frame,int(x_min),int(x_max),int(y_min),int(y_max))
                cv2.imwrite(path, processed_frame)
                print("FrameCaptured")
                time.sleep(1)
                imagesCaptured=imagesCaptured+1
                imageCounter=imageCounter+1
    cv2.destroyAllWindows()

def processPresentImages(DIRPath):
    model = YOLO("Saved_Models/yolov8m-face.pt")
    imageCounter = 0
    for filename in os.scandir(DIRPath):
        imgPath = filename.path
        frame = cv2.imread(imgPath)
        results = model(imgPath)
        newImgPath = DIRPath+"/"+str(imageCounter)+".jpg"
        boxs = results[0].boxes
        if len(boxs) == 0:
            print("No face detected : ",imgPath)
            continue
        for box in boxs:
            conf = round(box.conf[0].item(), 2)
            if conf>0.4:
                x_min,y_min,x_max,y_max= ((box.xyxy).tolist())[0]
                processed_frame = processImage(frame,int(x_min),int(x_max),int(y_min),int(y_max))
                cv2.imwrite(newImgPath, processed_frame)
                imageCounter=imageCounter+1
        os.remove(imgPath)
    return imageCounter

def processImage(frame,x_min,x_max,y_min,y_max):
    cropped_image = frame[y_min:y_max,x_min:x_max]
    resized_image = cv2.resize(cropped_image,(160,160))
    return resized_image

# Creates DIR if not explicitly created by user
def createDIR(searchParam): 
    DIRPath = "Drop_Your_Training_Images_HERE"+"/"+searchParam
    if not os.path.exists(DIRPath):
        os.makedirs(DIRPath)
    return DIRPath

def automatePreparingImages(searchParam):
    DIRPath = createDIR(searchParam)
    imageCounter=processPresentImages(DIRPath)
    gatherImages(DIRPath,imageCounter)
    return DIRPath
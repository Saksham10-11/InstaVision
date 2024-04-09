from tkinter import messagebox;
import pathlib
import shutil
import json
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
            return int(ID),True
    return -1,False

def createDIR(dirPath,ID,type):
    availableOptions = getAvailableOptions()
    newpath = dirPath+"/"+availableOptions[str(ID)]+"/"+type
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

def copyFiles(filePaths,destinationFolder):
    for filePath in filePaths:
        shutil.copy(filePath, destinationFolder)

def updateJSON(searchParam):
    availableOptions = getAvailableOptions()
    ID = len(availableOptions)
    availableOptions[str(ID)] = searchParam
    with open("available_options.json", 'w') as file:
        json.dump(availableOptions, file)

def checkPath(DIRPath):
    return os.path.exists(DIRPath)

def chooseModel():
    result = messagebox.askquestion("Choose Option", "There are two models available for organizing you stuff ... the medium model is comparatively slower but more accurate than the nano model ... Do you want to continue with the medium sized model ? ",
                                    icon='question', type='yesno')
    choice = ""
    if result == 'yes':
        choice = "m"
    else:
        choice = "n"
    return choice;
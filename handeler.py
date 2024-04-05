from tkinter import messagebox
from utils import getFilePaths,trainCustomModel,checkIfAvailable
from organizer import organizeImages,organizeVids

def updateScreen(searchParam):
    trainCustomModel(searchParam)

def handelInputCommands(dirPath , searchParam):
    imageFilePaths,vidFilePaths = getFilePaths(dirPath)
    ID , isValid = checkIfAvailable(searchParam)
    if isValid==True and len(imageFilePaths)>0:
        organizeImages(ID,imageFilePaths,dirPath)
        organizeVids(ID,vidFilePaths,dirPath)
    else:
        response = messagebox.askquestion("Message","Do you want to train the model for detecting custom face ?")
        if response == 'yes':
            updateScreen(searchParam)
        else :
            pass
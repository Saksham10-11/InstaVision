from tkinter import messagebox
from trainModel import automateTrainingModel
from utils import updateJSON,checkIfAvailable
from organizer import organize
from prepareImages import automatePreparingImages

def updateScreen(dirPath,searchParam):
    DIRPath = automatePreparingImages(searchParam)
    automateTrainingModel(DIRPath,searchParam)
    updateJSON(searchParam)
    organize(dirPath,searchParam)

def handelInputCommands(dirPath , searchParam):
    ID , isValid = checkIfAvailable(searchParam)
    if isValid==True:
        organize(dirPath,searchParam)
    else:
        response = messagebox.askquestion("Message","Do you want to train the model for detecting custom face ?")
        if response == 'yes':
            updateScreen(dirPath,searchParam)
        else :
            pass
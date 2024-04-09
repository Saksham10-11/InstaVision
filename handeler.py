from tkinter import messagebox
from trainModel import automateTrainingModel
from utils import updateJSON,checkIfAvailable,checkPath
from organizer import organize
from prepareImages import automatePreparingImages

def updateScreen(dirPath,searchParam):
    DIRPath = automatePreparingImages(searchParam)
    automateTrainingModel(DIRPath,searchParam)
    updateJSON(searchParam)
    organize(dirPath,searchParam)

def handelInputCommands(dirPath , searchParam):
    if not checkPath(dirPath) :
        messagebox.showerror("Error","Please enter a valid directory path ...")
        return 
    if searchParam == "":
        messagebox.showerror("Error","Search parameter cannot be empty ...")
        return
    ID , isValid = checkIfAvailable(searchParam)
    if isValid==True:
        organize(dirPath,searchParam)
        messagebox.showinfo("Message","Done Organizing Photos and Videos !!")
    else:
        response = messagebox.askquestion("Message","Do you want to train the model for detecting custom face ?")
        if response == 'yes':
            messagebox.showinfo("Message","Now another window will open. The controls for it are: 'space bar' to capture, 'q' to quit.")
            updateScreen(dirPath,searchParam)
            messagebox.showinfo("Message","Done Organizing Photos and Videos !!")
        else :
            pass
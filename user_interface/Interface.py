import tkinter
from tkinter import font
from tkinter.constants import LEFT
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import *
from matplotlib.animation import FuncAnimation
from matplotlib.pyplot import colorbar, xlabel, ylabel
import numpy as np
import random
import time
import serial
import serial.tools.list_ports
from PIL import Image, ImageTk

#Function to check if the user wants to close window
def Destruir_Ventana():
    if tkinter.messagebox.askokcancel("Salir", "¿Desea cerrar el programa?"):
        window.destroy()

#Global variable to check if the device is currently doing a calibration
calibrating = False

#Function to begin right calibration
def Calibration(direction):
    try:
        serialDevice.write(bytes(direction,'utf-8'))
    except:
        tkinter.messagebox.showerror(title="Failed to send data", message= "Connection with the device failed")
    global calibrating
    calibrating = direction
    print("calibratring " + str(direction) + " side")
    if direction == "C":
        label_centerCalibration["text"] = "Calibrating..."
    elif direction == "L":
        label_leftCalibration["text"] = "Calibrating..."
    elif direction == "R":
        label_rightCalibration["text"] = "Calibrating..."
    elif direction == "U":
        label_upperCalibration["text"] = "Calibrating..."
    else:
        label_downCalibration["text"] = "Calibrating..."
    
#Iniciar ventana
window = tkinter.Tk()
window.geometry("640x480")
window.title("Focus Tool")
window.resizable(0,0)
window.protocol("WM_DELETE_WINDOW", Destruir_Ventana)

#Status
label_status = tkinter.Label(window)
label_status.place(x = 220, y = 65, width = 200, height = 20)

#first connect to the bluetooth device
#check connection and then proceed to change COM to the 
#indicated number
try:
    serialDevice = serial.Serial("COM9", 9600)
except:
    label_status["text"] = "Status: Device not found"

#Title
label_title = tkinter.Label(window, text = "Focus Tool", font="Calibri 20")
label_title.place(x = 260, y = 0, width = 120, height = 30)
#Warning comment
label_userComment = tkinter.Label(window, text =u'Make sure you are wearing the device before calibrating', font="Calibri 14")
label_userComment.place(x = 100, y = 35, width = 440, height = 20) 

#First step
label_firstStep = tkinter.Label(window, text = "1. Calibrate your normal head movement:", font="Calibri 12")
label_firstStep.place(x = 5, y = 90, width = 300, height = 20 )

#Button to begin center point calibration
button_centerCalibration = tkinter.Button(window, text = "Calibrate center point", command = lambda: Calibration("C"))
button_centerCalibration.place(x = 40, y = 120, width = 130, height = 25)

#Center point calibration state label
label_centerCalibration = tkinter.Label(window, text = "Not calibrated")
label_centerCalibration.place(x = 180, y = 120, width = 100, height = 25)

#Button to begin left side calibration
button_leftCalibration = tkinter.Button(window, text = "Calibrate left side", command =lambda: Calibration('L'))
button_leftCalibration.place(x = 40, y = 150, width = 130, height = 25)

#Left side calibration state label
label_leftCalibration = tkinter.Label(window, text = "Not calibrated")
label_leftCalibration.place(x = 180, y = 150, width = 100, height = 25)

#Button to begin right side calibration
button_rightCalibration = tkinter.Button(window, text = "Calibrate right side", command = lambda: Calibration('R'))
button_rightCalibration.place(x = 40, y = 180, width = 130, height = 25)

#Right side calibration state label
label_rightCalibration = tkinter.Label(window, text = "Not calibrated")
label_rightCalibration.place(x = 180, y = 180, width = 100, height = 25)

#Button to begin upper side calibration
button_upperCalibration = tkinter.Button(window, text = "Calibrate upper side", command = lambda: Calibration('U'))
button_upperCalibration.place(x = 40, y = 210, width = 130, height = 25)

#upper calibration state label
label_upperCalibration = tkinter.Label(window, text = "Not calibrated")
label_upperCalibration.place(x = 180, y = 210, width = 100, height = 25)

#Button to begin down side calibration
button_downCalibration = tkinter.Button(window, text = "Calibrate down side", command = lambda: Calibration('D'))
button_downCalibration.place(x = 40, y = 240, width = 130, height = 25)

#Down side calibration state label
label_downCalibration = tkinter.Label(window, text = "Not calibrated")
label_downCalibration.place(x = 180, y = 240, width = 100, height = 25)

calibrationcomplete = str()

def eyeCalibration(type, current_image):
    try:
        serialDevice.write(bytes(type,'utf-8'))
        def closeEyeCalib():
            if tkinter.messagebox.askokcancel("Close eye calibration", "Do you want to stop the calibration?"):
                eyeCalibWindow.destroy()

        eyeCalibWindow = tkinter.Toplevel(window)
        eyeCalibWindow.title("Eye calibration")
        eyeCalibWindow.state('zoomed')
        eyeCalibWindow.protocol("WM_DELETE_WINDOW", closeEyeCalib)
        while True:
            if current_image == 0:
                img_eyecalib = ImageTk.PhotoImage(Image.open("CenterDot.png"))
                show_eyecalib = tkinter.Label(eyeCalibWindow, image = img_eyecalib)
                show_eyecalib.pack(side = "bottom", fill = "both", expand = "yes")
            elif current_image == 1:
                img_eyecalib = ImageTk.PhotoImage(Image.open("UpperDot.png"))
                show_eyecalib["image"] = img_eyecalib
                print("Hello There")
            elif current_image == 2:
                img_eyecalib = ImageTk.PhotoImage(Image.open("CenterDot.png"))
                show_eyecalib["image"] = img_eyecalib
            elif current_image == 3:
                img_eyecalib = ImageTk.PhotoImage(Image.open("RightDot.png"))
                show_eyecalib["image"] = img_eyecalib
                print("Hello There")
            elif current_image == 4:
                img_eyecalib = ImageTk.PhotoImage(Image.open("CenterDot.png"))
                show_eyecalib["image"] = img_eyecalib
            eyeCalibWindow.update_idletasks()   
            eyeCalibWindow.update()
            time.sleep(4)
            if current_image == 2:
                label_eyeVerticalCalibration["text"] = 'done'
                eyeCalibWindow.destroy()
                break
            elif current_image == 4:
                label_eyeHorizontalCalibration["text"] = 'done'
                eyeCalibWindow.destroy()
                break
            if type == 'V':
                if current_image == 1:
                    current_image = 2
                else:
                    current_image = 1
                print("Hallo")
            elif type == 'H':
                if current_image == 3:
                    current_image = 4
                else:
                    current_image = 3
    except:
        tkinter.messagebox.showerror(title="Failed to send data", message= "Connection with the device failed")

        

#Second Step
label_secondStep = tkinter.Label(window, text = "2. Calibrate your eyes movements", font = "Calibri 12")
label_secondStep.place(x = 320, y = 90, width = 300, height = 20)

#Horizontal eye movement calibration button
button_eyeHorizontalCalibration = tkinter.Button(window, text = "Calibrate horizontal movement", command =lambda: eyeCalibration('H',0))
button_eyeHorizontalCalibration.place(x = 350, y = 130, width = 180, height = 25)

#Horizontal eye movement calibration state label
label_eyeHorizontalCalibration = tkinter.Label(window, text = "Not calibrated")
label_eyeHorizontalCalibration.place(x = 540, y = 130, width = 100, height = 25)

#Vertical eye movement calibration button
button_eyeVerticalCalibration = tkinter.Button(window, text = "Calibrate vertical movement", command =lambda: eyeCalibration('V',0))
button_eyeVerticalCalibration.place(x = 350, y = 160, width = 180, height = 25)

#Vertical eye movement calibration state label
label_eyeVerticalCalibration = tkinter.Label(window, text = "Not calibrated")
label_eyeVerticalCalibration.place(x = 540, y = 160, width = 100, height = 25)

#Eye boundaries function
def eyeBoundaries(type):
    global calibrating
    try:
        serialDevice.write(bytes(type, 'utf-8'))
        calibrating = True
        if type == 'v':
            label_eyeVerticalBoundariesSet["text"] = 'defining'
        elif type == 'h':
            label_eyeHorizontalBoundariesSet["text"] = 'defining'
    except:
        tkinter.messagebox.showerror(title="Failed to send data", message="Connection with the device failed")

#Horizontal eye movement boundaries set button
button_eyeHorizontalBoundariesSet = tkinter.Button(window, text = "Define eye horizontal boundary", command = lambda: eyeBoundaries('h'))
button_eyeHorizontalBoundariesSet.place(x = 350, y = 190, width = 180, height = 25)

#Horizontal eye movement boundaries set state label
label_eyeHorizontalBoundariesSet = tkinter.Label(window, text = "Not defined")
label_eyeHorizontalBoundariesSet.place(x = 540, y = 190, width = 100, height = 25)

#Vertical eye movement boundaries set button
button_eyeVerticalBoundariesSet = tkinter.Button(window, text = "Define eye vertical boundary", command = lambda: eyeBoundaries('v'))
button_eyeVerticalBoundariesSet.place(x = 350, y = 220, width = 180, height = 25)

#Vertical eye movement boundaries set state label
label_eyeVerticalBoundariesSet = tkinter.Label(window, text = "Not defined")
label_eyeVerticalBoundariesSet.place(x = 540, y = 220, width = 100, height = 25)

#Third Step
label_ThirdStep = tkinter.Label(window, text = "3. Begin monitor and focus: ", font = "Calibri 12")
label_ThirdStep.place(x = 220, y = 300, width = 200, height = 25)

def start_monitoring():
    try:
        serialDevice.write(bytes('O','utf-8'))
        label_beginMonitoring["text"] = 'done'
    except:
        tkinter.messagebox.showerror(title= "Failed to send data", message="Connection with the device failed")

#Begin monitoring
button_beginMonitoring = tkinter.Button(window, text = "Start Monitoring", command = start_monitoring)
button_beginMonitoring.place(x = 270, y = 330, width = 100, height = 25)

#Begin monitoring label
label_beginMonitoring = tkinter.Label(window)
label_beginMonitoring.place(x = 270, y = 360, width = 100, height = 25)

while True:
    window.update_idletasks()
    window.update()
    if calibrating != False:
        try:
            n = 0
            attempts = 0
            while n == 0:
                n = serialDevice.inWaiting()
                window.update_idletasks()
                window.update()
                time.sleep(0.05)
            calibrationcomplete += serialDevice.read(n).decode('UTF-8') # read n bytes from the serial device
            print(calibrationcomplete)
            if calibrationcomplete == 'RC':
                label_centerCalibration["text"] = 'done'
                calibrationcomplete = ''
                calibrating = False
            elif calibrationcomplete == 'RL':
                label_leftCalibration["text"] = 'done'
                calibrationcomplete = '' 
                calibrating = False
            elif calibrationcomplete == 'RR':
                label_rightCalibration["text"] = 'done'
                calibrationcomplete = ''
                calibrating = False
            elif calibrationcomplete == 'RU':
                label_upperCalibration["text"] = 'done'
                calibrationcomplete = ''
                calibrating = False
            elif calibrationcomplete == 'RD':
                label_downCalibration["text"] = 'done'
                calibrationcomplete = ''
                calibrating = False
            elif calibrationcomplete == 'Rh':
                label_eyeHorizontalBoundariesSet["text"] = 'done'
                calibrating = False
            elif calibrationcomplete == 'Rv':
                label_eyeVerticalBoundariesSet["text"] = 'done'
                calibrating = False
            time.sleep(0.05)
        except:
            tkinter.messagebox.showerror(title = "Failed to receive data", message = "Connection with the device failed")
            if calibrating == 'C':
                label_centerCalibration["text"] = 'Not calibrated'
            elif calibrating == 'L':
                label_leftCalibration["text"] = 'Not calibrated'
            elif calibrating == 'R':
                label_rightCalibration["text"] = 'Not calibrated'
            elif calibrating == 'U':
                label_upperCalibration["text"] = 'Not calibrated'
            elif calibrating == 'D':
                label_downCalibration["text"] = 'Not calibrated'
            calibrating = False

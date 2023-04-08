#Authors - Harsh Athavale & Abdul Samadh Azath

from tkinter import Canvas, Button, Label, Text, PhotoImage 
from constants import * # importing from constants.py
from copy import deepcopy
from recognizer import *

from time import strftime, sleep
import json
import os
from shutil import rmtree
from xml.dom import minidom
import os

class Board:
    def __init__(self, root, mode):
        self.root = root
        self.mode = mode
        # Recognition mode will recognize user inputs
        if self.mode == 'recognition':
            
            # Create canvas, clear button and label to show predicted gesture, confidence and time taken to predict
            self.createCanvas()
            self.createClearButton()
            self.createPredictionLabels()
            self.points = []
            self.temp=[]
            self.createSubmitButton()

            # Invoking the recognizer module
            # self.recognizer = Recognizer()
            self.startPointX = 0
            self.startPointY = 0
        # Collection mode will only store user input as it is
        elif self.mode == 'collection':

            # Current working directory will be used to load gesture image as a reference
            self.currentWorkingDirectory = os.getcwd()
            
            # Flags which will indicate the user added status and collection start status
            self.userAdded = False
            self.readyToStore = False
            
            # Creating variables to track current user parameters
            self.gestureList = GESTURE_LIST
            self.currentUser = ''
            self.userDrawCount = 0
            self.gestureIndex = 0
            self.currentUserId = ''
            self.currentGesture = ''
            self.points = []
            self.startPointX = 0
            self.startPointY = 0

            # Create canvas for drawing
            self.createCanvas()

            # Create clear button to enable user to clear the canvas
            self.createClearButton()

          
            # Added submit button to enable user to submit their drawing
            self.createSubmitButton()

            # Label to prompt the user
            self.createPromptLabel()
            self.setPromptLabel('Please Enter User ID!',1)
            
            # Text box to get user ID
            self.createUserIdTextBox()

            # Label to show reference gesture image to user
            self.createGestureImageLabel()
    
    # def collectFromUser(self, userId):
    #     # Delete any existing user with same userId in DB and start fresh
    #     self.db.addUser(userId)
    #     for iteration in range(10):
    #         shuffle(self.gestureList)
    #         for gesture in self.gestureList:
    #             self.setPromptLabel('Please draw a {}'.format(gesture))

    
    # Function to create the canvas - drawing board
    # Creates the drawing board and sets mouse bindings to track user click and drag movements
    def createCanvas(self):
        self.board = Canvas(self.root, width=BOARD_WIDTH, height=BOARD_HEIGHT, bg=BOARD_BG)
        self.setMouseBindings()
        self.board.pack()

    # Function to create user ID Text box to get user ID from the user
    def createUserIdTextBox(self):
        self.userIdTextBox = Text(self.root, width=TEXT_BOX_WITDH, height=TEXT_BOX_HEIGHT)
        self.userIdTextBox.pack(side='top')

    # Function to create clear button to enable user to clear the drawing board
    def createClearButton(self):
        self.clearButton = Button(self.root, text=CLEAR_BUTTON_TEXT)
        self.clearButton.configure(command=self.onClearButtonClick)
        self.clearButton.pack(side = 'left')

    # Function to create a submit button to enable user to submit their drawing
    def createSubmitButton(self):
        self.submitButton = Button(self.root, text=SUBMIT_BUTTON_TEXT)
        self.submitButton.configure(command=self.onSubmitButtonClick)
        self.submitButton.pack(side = 'left')
    
    # Function to create lable to show user a reference of the gesture to be drawn
    def createGestureImageLabel(self):
        self.gestureImageLabel = Label(self.root)

    # Function to create labels to show predicted gesture, confidence and time taken to predict
    def createPredictionLabels(self):
        self.predictedGestureLabel = Label(self.root)
        self.confidenceLabel = Label(self.root)
        self.timelabel = Label(self.root)
        # Create bindings for predicted gesture label and confidence label
        self.predictedGestureLabel.pack()
        self.confidenceLabel.pack()
        self.timelabel.pack()
    
    # Function to set image to show the user as a reference
    def setGestureImageLabel(self, img):
        self.gestureImageLabel.configure(image = img)
        self.gestureImageLabel.image = img # type: ignore
        self.gestureImageLabel.pack(side='right')

    # Function to clear the gesture reference image when user has finished drawing
    def clearGestureImageLabel(self):
        self.gestureImageLabel.destroy()
    
    # Function to set values to prediction labels
    def setPredictionLabels(self, recognizedGesture, score, time):
        self.predictedGestureLabel.configure(text="Predicted Gesture = "  + str(recognizedGesture))
        self.confidenceLabel.configure(text="Confidence = "  + str(round(score,2))) 
        self.timelabel.configure(text="Time = "  + str(round(time*1000,2)) + " ms" )

    # Function to clear prediction labels
    def clearPredictionLables(self):
        self.predictedGestureLabel.configure(text="")
        self.timelabel.configure(text="")
        self.confidenceLabel.configure(text="")
    
    def createPromptLabel(self):
        self.promptLabel1 = Label(self.root)
        self.promptLabel1.pack()

        self.promptLabel2 = Label(self.root)
        self.promptLabel2.pack()
    
    def setPromptLabel(self,message, id):
        if id == 1:
            self.promptLabel1.configure(text=message)
        else:
            self.promptLabel2.configure(text=message)

    def loadImage(self, gestureName):
        return PhotoImage(file = "{}/gestures/{}.gif".format(self.currentWorkingDirectory,gestureName))

    def setMouseBindings(self):
        # Creating bindings for board (draw handles mouse down and drag events)
        self.board.bind(MOUSE_CLICK,self.getLastCoordinates)
        self.board.bind(MOUSE_DRAG_MODE, self.draw)
        if self.mode == 'recognition':
            self.board.bind(MOUSE_UP_MODE, self.mouseUp)
        
    # Handler for clear button click
    def onClearButtonClick(self):
        self.points.clear() 
        # Clears everything on the canvas
        self.board.delete(BOARD_DELETE_MODE)
        print(LOG_BOARD_CLEARED)
    
    def onSubmitButtonClick(self):
        # NDollarRecognizer(True)
        NDollarRecognizer.Recognize(self,self.points,True,False,False)

    # Function to return last coordinates of the mouse click
    def getLastCoordinates(self,event):
        self.startPointX,self.startPointY=event.x,event.y

    # Draws when mouse drag or screen touch event occurs
    def draw(self, event):
        
        self.board.create_line((self.startPointX, self.startPointY, event.x, event.y),fill=BLUE,width=5)

        self.temp.append([event.x,event.y])
        self.startPointX, self.startPointY = event.x,event.y

    # Draws different states of user input (resampled,rotated,scaled)
    def reDraw(self, points, color,fxn):
        if fxn == "resample":
            for i in range(len(points)):
                x1, y1, x2, y2 = points[i][0]-2, points[i][1]-2, points[i][0]+2, points[i][1]+2
                self.board.create_oval(x1+200, y1, x2+200, y2, fill=color, outline=color)

        if fxn == "rotated":
            for i in range(len(points)):
                x1, y1, x2, y2 = points[i][0]-2, points[i][1]-2, points[i][0]+2, points[i][1]+2
                self.board.create_oval(x1+400, y1+100, x2+400, y2+100, fill=color, outline=color)
        
        if fxn == "scaled":
             for i in range(len(points)):
                x1, y1, x2, y2 = points[i][0]-2, points[i][1]-2, points[i][0]+2, points[i][1]+2
                self.board.create_oval(x1+400, y1, x2+400, y2, fill=color, outline=color)

    # Mouse up event handler
    def mouseUp(self, event):
        self.points.append(self.temp)
        self.temp=[]
        # resampledPoints = self.recognizer.resample(deepcopy(self.points), SAMPLING_POINTS)
        # # self.reDraw(resampledPoints, RED,"resample")
        # rotatedPoints = self.recognizer.rotate(resampledPoints)
        # # self.reDraw(rotatedPoints, ORANGE,"rotated")
        # scaledPoints = self.recognizer.scale(rotatedPoints, SCALE_FACTOR)
        # translatedPoints = self.recognizer.translate(scaledPoints, ORIGIN)
        # self.reDraw(translatedPoints, GREEN,"scaled")

        # # recognizedGesture, score, time , _= self.recognizer.recognizeGesture(translatedPoints)
        # self.setPredictionLabels(recognizedGesture, score, time)
        print(self.points)
    
    def createXMLUserLogs(self):
        # Open the JSON file containing the user data and load it into a dictionary
        file = open('database.json')
        user_data = json.load(file)
        file.close()

        # Get the current working directory
        root = os.getcwd()

        # Define the name and path of the directory where the XML logs will be saved
        log_directory_name = 'xml_collected_logs'
        log_directory_path = os.path.join(root, log_directory_name)

        # If the directory already exists, delete it and create a new one
        if os.path.isdir(log_directory_path):
            rmtree(log_directory_path)
        os.makedirs(log_directory_path)

        # Iterate over the users in the user data dictionary
        for user in user_data:

            # Create a directory for the user in the XML logs directory
            user_path = os.path.join(log_directory_path, user)
            os.makedirs(user_path)

            # Iterate over the gestures of the user
            for gesture in user_data[user]:

                # Iterate over each set of points for the gesture
                for i in range(0,len(user_data[user][gesture])):

                    # Get the list of points for the gesture
                    pointList = user_data[user][gesture][i]

                    # Create a new XML document
                    root = minidom.Document()
                    gestureChild = root.createElement('Gesture')

                    # Set the attributes of the gesture element
                    gestureChild.setAttribute('User', str(user))
                    gestureChild.setAttribute('Gesture', '{}{}'.format(gesture,i+1))
                    gestureChild.setAttribute('Number', str(i+1))
                    gestureChild.setAttribute('NumPts', str(len(pointList)))
                    gestureChild.setAttribute('Date', strftime("%d-%m-%Y"))
                    gestureChild.setAttribute('Time', strftime("%H:%M:%S"))

                    # Append the gesture element to the root element
                    root.appendChild(gestureChild)

                    # Iterate over the points of the gesture and create a new point element for each point
                    for point in pointList:
                        pointChild = root.createElement('Point')
                        pointChild.setAttribute('X', str(point[0]))
                        pointChild.setAttribute('Y', str(point[1]))
                        gestureChild.appendChild(pointChild)

                    # Get the string representation of the XML document and write it to a file
                    gestureRootString = root.toprettyxml(indent= "\t")
                    file_name = '{}{}.xml'.format(gesture,'0{}'.format(i+1) if i+1<10 else str(i+1))
                    file_path = os.path.join(user_path, file_name)
                    with open(file_path, "w") as file:
                        file.write(gestureRootString)

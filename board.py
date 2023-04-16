#Authors - Harsh Athavale & Abdul Samadh Azath

from tkinter import Canvas, Button, Label, Text, PhotoImage 
from constants import * # importing from constants.py
from copy import deepcopy
from recognizerV2 import NDollarRecognizer
from commonUtils import *
from database import Database
from time import strftime, sleep
import json
import os
from shutil import rmtree
from xml.dom import minidom
import os
from segment import Segment

class Board:
    def __init__(self, root, mode, inputMethod='Mouse'):
        self.root = root
        self.mode = mode
        self.calc=[]
        self.points = []
        self.multistrokepoints = []
        self.startPoint = Point(0,0)
        self.allPoints = []
        self.inputMethod = inputMethod
        self.ignoreDrag = True if self.inputMethod == 'Touch' else False
        # Recognition mode will recognize user inputs
        if self.mode == 'recognition' or self.mode == 'segmentation':
            
            # Create canvas, clear button and label to show predicted gesture, confidence and time taken to predict
            self.createCanvas()
            self.createClearButton()
            self.createPredictionLabels()
            self.createSubmitButton()
            self.recognizer = NDollarRecognizer(True)

            # Invoking the recognizer module
            # self.recognizer = Recognizer()
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
            # Create canvas for drawing
            self.createCanvas()

            # Create clear button to enable user to clear the canvas
            self.createClearButton()

            # Invoking DB module to store user points with user id in a json
            self.db = Database()

            # Added submit button to enable user to submit their drawing
            self.createSubmitButton()

            # Label to prompt the user
            self.createPromptLabel()
            self.setPromptLabel('Please Enter User ID!',1)
            
            # Text box to get user ID
            self.createUserIdTextBox()

            # Label to show reference gesture image to user
            # self.createGestureImageLabel()
    
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
        self.clearButton.place(x=20,y=610)
        # self.clearButton.pack()

    # Function to create a submit button to enable user to submit their drawing
    def createSubmitButton(self):
        self.submitButton = Button(self.root, text=SUBMIT_BUTTON_TEXT)
        self.submitButton.configure(command=self.onSubmitButtonClick)
        # self.submitButton.pack(side = 'left')
        self.submitButton.place(x=150,y=610)
    
    # Function to create lable to show user a reference of the gesture to be drawn
    def createGestureImageLabel(self):
        self.gestureImageLabel = Label(self.root)

    # Function to create labels to show predicted gesture, confidence and time taken to predict
    def createPredictionLabels(self):
       
        self.predictedGestureLabel = Label(self.root)
        self.confidenceLabel = Label(self.root)
        self.timelabel = Label(self.root)
        self.resultLabel = Label(self.root)
        self.resultLabel.place(x=800,y=610)
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
    def setPredictionLabels(self, recognizedGesture, score=None, time=None):
        self.predictedGestureLabel.configure(text="Predicted Gesture = "  + str(recognizedGesture))

        if score:
            self.confidenceLabel.configure(text="Confidence = "  + str(round(score,2))) 
        if time:
            self.timelabel.configure(text="Time = "  + str(round(time*1000,2)) + " ms" )

    
    def calculation(self, gestureList):
        st=""
        for s in gestureList:
         
            if s=="X":
                st+="*"
                continue
            st+=s
        print(st)
        result =eval(str(st))
        self.resultLabel.configure(text="Result = "  + str(result))
        
        
        



        
       


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
        self.board.bind(MOUSE_UP_MODE, self.mouseUp)
        
    # Handler for clear button click
    def onClearButtonClick(self):
        self.points.clear()
        self.multistrokepoints.clear()
        self.allPoints.clear()
        # Clears everything on the canvas
        self.board.delete(BOARD_DELETE_MODE)
        print(LOG_BOARD_CLEARED)

    # Mouse up event handler
    def mouseUp(self, event):
        self.ignoreDrag = True
        self.multistrokepoints.append(deepcopy(self.points))
        self.allPoints.append(deepcopy(self.points))
        self.points.clear()
        print(MOUSE_UP)
    
    def onSubmitButtonClick(self):
        if self.mode == 'collection':
            # Check if a user has been added
            if not self.userAdded:
                # Get the user ID from a text box
                userId = self.userIdTextBox.get(1.0, "end-1c")
                # Set the current user and add them to the database
                self.currentUser = userId
                self.db.addUser(userId)
                # Display a welcome message to the user
                self.setPromptLabel('Welcome {}!'.format(userId), 1)
                # Set userAdded to True to indicate that a user has been added
                self.userAdded = True
            
            # Check if the system is ready to store the gesture drawing
            if self.readyToStore:
                num = self.userDrawCount/(len(self.gestureList))
                print(num)
                num = int(num)
                # Get the index of the current gesture and add the gesture drawing to the database
                gestureIndex = (self.gestureIndex - 1)%len(self.gestureList)
                self.db.addGesture(self.currentUser, self.gestureList[gestureIndex], deepcopy(self.multistrokepoints),num+1)
                # Clear the drawing board and points list
                self.multistrokepoints.clear()
                self.board.delete(BOARD_DELETE_MODE)
            
            # Check if the user has completed all their drawings
            if self.userDrawCount < 10*(len(self.gestureList)):
                # Get the name of the current gesture awnd prompt the user to draw it
                gestureName = self.gestureList[self.gestureIndex]
                self.setPromptLabel('Please draw a {}'.format(gestureName), 2)
                # Display an image of the gesture
                # self.setGestureImageLabel(self.loadImage(gestureName))
                # Update the userDrawCount and gestureIndex variables
                self.userDrawCount += 1
                self.gestureIndex = (self.gestureIndex + 1)%len(self.gestureList)
                # Set readyToStore to True to indicate that the system is ready to store the next drawing
                self.readyToStore = True
            else:
                # If the user has completed all the drawings, display a message and clear the gesture image label
                self.setPromptLabel('Saving your contribution!', 1)
                self.setPromptLabel('Thank you for participating, {}!'.format(self.currentUser), 2)
                # self.createXMLUserLogs()
                # self.clearGestureImageLabel()
                self.root.update()
                sleep(2)
                self.setPromptLabel('', 2)
                # Create an XML file with the collected user logs, reset userDrawCount and gestureIndex, and display a prompt to start again
                self.createXMLUserLogs()
                self.userDrawCount = 0
                self.gestureIndex = 0
                self.setPromptLabel('Please enter user ID and click Submit to Start!', 1)
                # Set userAdded and readyToStore to False to indicate that a new user needs to be added and the system is not ready to store a drawing yet
                self.userAdded = False
                self.readyToStore = False
        elif self.mode == 'recognition':
            for gesture in self.multistrokepoints:
                for point in gesture:
                    print(point.display(), end = '')
                print()
            # print("ye hai points bc")
            # print(self.multistrokepoints)
            result = self.recognizer.Recognize(self.multistrokepoints)
            result.display()
            # print(self.multistrokepoints)
            self.multistrokepoints.clear()
            print(LOG_DRAWING_FINISHED)
        elif self.mode == 'segmentation':
            print(len(self.allPoints))
            for gesture in self.allPoints:
                for point in gesture:
                    print(point.display(),end=' ')
                print()
            
            segment = Segment(deepcopy(self.allPoints))
            self.allPoints.clear()
            gestureList = segment.getRecognizedSymbols()
            print("ye le ")
            print(gestureList)
            self.setPredictionLabels(str(gestureList))
            self.calculation(gestureList)
            # Get list of segmented gestures
            # Recognize each gesture
            # Calculate value and return


    # Function to return last coordinates of the mouse click
    def getLastCoordinates(self,event):
        self.ignoreDrag = False
        print("Mouse Down")
        self.startPoint.set(event.x, event.y)


    # Draws when mouse drag or screen touch event occurs
    def draw(self, event):
        if self.ignoreDrag:
            return
        print("Mouse Drag")
        self.board.create_line((self.startPoint.X, self.startPoint.Y, event.x, event.y),fill=BLUE,width=3)
        self.points.append(Point(event.x, event.y))
        self.startPoint.set(event.x, event.y)
    
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
        subject = 0
        # Iterate over the users in the user data dictionary
        for user in user_data:
            subject+=1
            print(user)

            # Create a directory for the user in the XML logs directory
            user_path = os.path.join(log_directory_path, user)
            os.makedirs(user_path)

            # Iterate over the gestures of the user
            for gesture in user_data[user]:
                # print(gesture)
                ind = len(user_data[user][gesture])
                print(ind)
                pointsum=0
                root = minidom.Document()
                gestureChild = root.createElement('Gesture')

                # Set the attributes of the gesture element
                gestureChild.setAttribute('Subject', str(subject))
                
                gestureChild.setAttribute('InputType', "Touch")
                
                gestureChild.setAttribute('Speed', "Medium")
                o=0
                # # Iterate over each set of points for the gesture
                for i in range(0,len(user_data[user][gesture])):

                    # Get the list of points for the gesture
                    pointList = user_data[user][gesture][i]
                    pointsum+=len(pointList)
                    

                    # Create a new XML document
                    gestureChild.setAttribute('Name', '{}'.format(gesture))
                    gestureChild.setAttribute('NumPts', str(pointsum))
                    
                    # gestureChild.setAttribute('Date', strftime("%d-%m-%Y"))
                    # gestureChild.setAttribute('Time', strftime("%H:%M:%S"))

                    # Append the gesture element to the root element
                    root.appendChild(gestureChild)

                    # Iterate over the points of the gesture and create a new point element for each point
                    

                    # for j in range(1,ind+1):
                    stroke = root.createElement('Stroke')
                    stroke.setAttribute('index',str(i+1))
                    gestureChild.appendChild(stroke)

                    for point in pointList:
                        o+=1
                        pointChild = root.createElement('Point')
                        pointChild.setAttribute('X', str(point[0]))
                        pointChild.setAttribute('Y', str(point[1]))
                        pointChild.setAttribute('T', str(o))
                        pointChild.setAttribute('Pressure', "128")
                        stroke.appendChild(pointChild)

                    # Get the string representation of the XML document and write it to a file
                    gestureRootString = root.toprettyxml(indent= "\t")
                    # file_name = '{}{}.xml'.format(gesture,'0{}'.format(i+1) if i+1<10 else str(i+1))
                    if "/" in gesture:
                        newgesture =gesture.replace('/','div')
                        
                        # print(gesture)
                        file_name = '{}.xml'.format(newgesture)

                    else:

                        file_name = '{}.xml'.format(gesture)
                    file_path = os.path.join(user_path, file_name)
                    with open(file_path, "w") as file:
                        file.write(gestureRootString)

    
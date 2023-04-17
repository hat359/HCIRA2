from math import sqrt
from commonUtils import *
from recognizerV2 import NDollarRecognizer

class Segment():
    def __init__(self, gestures):
        """
        Constructor of the Segment class.

        Args:
            gestures (list): List of gestures, each represented as a list of points (x, y).
        """
        self.gestures = gestures
        self.recognitionObjects = [] # List to store the recognition objects after segmentation
        self.recognizedEquation = [] # List to store the recognized equations after recognition
        self.recognizer = NDollarRecognizer(True) # NDollarRecognizer object for performing recognition
        self.startSegmentation() # Start the segmentation process
        self.startRecognition() # Start the recognition process
        # for objects in self.recognitionObjects:
        #     print(objects)
        #     print()

    def isOverlapping(self, gestureA, gestureB, threshold=10):
        """
        Checks if two gestures overlap based on the Euclidean distance between their points.

        Args:
            gestureA (list): List of points representing the first gesture.
            gestureB (list): List of points representing the second gesture.
            threshold (int): Threshold distance for considering two points as overlapping (default=10).

        Returns:
            bool: True if the two gestures overlap, False otherwise.
        """
        for pointA in gestureA:
            for pointB in gestureB:
                distance = self.getEucledianDistance(pointA, pointB)
                if distance <= threshold:
                    return True
        return False

    def getEucledianDistance(self, pointA, pointB):
        """
        Calculates the Euclidean distance between two points.

        Args:
            pointA (tuple): Tuple representing the coordinates of the first point (x, y).
            pointB (tuple): Tuple representing the coordinates of the second point (x, y).

        Returns:
            float: The Euclidean distance between the two points.
        """
        return sqrt((pointA[0] - pointB[0])**2 + (pointA[1] - pointB[1])**2)

    def startSegmentation(self):
        """
        Performs segmentation of gestures to identify overlapping gestures and single gestures.
        """
        skipEvaluation = False
        for i in range(0,len(self.gestures)-1):
            if skipEvaluation:
                skipEvaluation = False
                continue
            gestureA = self.gestures[i]
            gestureB = self.gestures[i+1]

            recognitionObjects = []
            if self.isOverlapping(gestureA, gestureB):
                print('{} and {} overlap!'.format(i,i+1))
                recognitionObjects.append(gestureA)
                recognitionObjects.append(gestureB)
                skipEvaluation = True
            else:
                print('{} is single'.format(i))
                recognitionObjects.append(gestureA)
            self.recognitionObjects.append(recognitionObjects)
        if skipEvaluation is False:
            print('{} is single'.format(len(self.gestures)-1))
            self.recognitionObjects.append([self.gestures[-1]])

    def startRecognition(self):
        """
        Performs recognition of gestures using the NDollarRecognizer object.
        """
        for recognitionObject in self.recognitionObjects:
            result = self.recognizer.Recognize(recognitionObject)
            self.recognizedEquation.append(result.Name[0])

    def getRecognizedSymbols(self):
        """
        Returns the recognized equations as a list of symbols.

        Returns:
            list: List of recognized symbols.
        """
        return self.recognizedEquation
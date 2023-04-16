from math import sqrt
from commonUtils import *
from recognizerV2 import NDollarRecognizer

class Segment():
    def __init__(self, gestures):
        self.gestures = gestures
        self.recognitionObjects = []
        self.recognizedEquation = []
        self.recognizer = NDollarRecognizer(True)
        self.startSegmentation()
        self.startRecognition()
        # for objects in self.recognitionObjects:
        #     print(objects)
        #     print()

    def isOverlapping(self, gestureA, gestureB, threshold=10):
        for pointA in gestureA:
            for pointB in gestureB:
                distance = self.getEucledianDistance(pointA, pointB)
                if distance <= threshold:
                    return True
        return False

    def getEucledianDistance(self, pointA, pointB):
        return sqrt((pointA[0] - pointB[0])**2 + (pointA[1] - pointB[1])**2)

    def startSegmentation(self):
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
        for recognitionObject in self.recognitionObjects:
            result = self.recognizer.Recognize(recognitionObject)
            self.recognizedEquation.append(result.Name)

    def getRecognizedSymbols(self):
        return self.recognizedEquation
#Authors - Harsh Athavale & Abdul Samadh Azath

from recognizerV2Utils import *    # Import necessary utility functions
from math import sqrt, sin, cos   # Import necessary math functions
from time import time             # Import necessary time function
from online_template import template    # Import template data for training set
from copy import deepcopy        # Import deepcopy function for deep copying objects

NumMultistrokes = 16    # Number of multistrokes in the recognizer
NumPoints = 96          # Number of points in a unistroke
SquareSize = 250.0      # Size of the square bounding box for resampling
OneDThreshold = 0.25    # Threshold for 1D gesture recognition
Origin = [0,0]          # Origin point for translating points
Diagonal = sqrt(SquareSize * SquareSize + SquareSize * SquareSize)   # Diagonal length of the square bounding box
HalfDiagonal = 0.5 * Diagonal    # Half of the diagonal length
AngleRange = Deg2Rad(45.0)       # Range of rotation angles for recognizing gestures
AnglePrecision = Deg2Rad(2.0)    # Precision of rotation angles for recognizing gestures
Phi = 0.5 * (-1.0 + sqrt(5.0))   # Phi value for calculating golden ratio
StartAngleIndex = int(NumPoints / 8)   # Index of starting angle for calculating start unit vector
AngleSimilarityThreshold = Deg2Rad(30.0)  # Threshold for angle similarity between start unit vectors

class Unistroke:
    def __init__(self,name, use_bounded_rotation_invariance, points):
        self.Name = name   # Name of the unistroke gesture
        self.Points = Resample(points, NumPoints)   # Resample points to fixed number of points
        self.radians = IndicativeAngle(self.Points)  # Calculate the indicative angle of the unistroke
        self.Points = RotateBy(self.Points, -self.radians)  # Rotate points by negative indicative angle
        self.Points = ScaleDimTo(self.Points, SquareSize, OneDThreshold)  # Scale points to a square bounding box
        if use_bounded_rotation_invariance:
            self.Points = RotateBy(self.Points, self.radians)   # Restore points to original rotation if bounded rotation invariance is used
        self.Points = TranslateTo(self.Points, Origin)   # Translate points to the origin
        self.StartUnitVector = CalcStartUnitVector(self.Points, StartAngleIndex)   # Calculate start unit vector of the unistroke
        self.Vector = Vectorize(self.Points, use_bounded_rotation_invariance)    # Vectorize points for Protractor
class Multistroke:
    def __init__(self, name, useBoundedRotationInvariance, strokes):
        self.Name = name  # Name of the multistroke gesture
        self.NumStrokes = len(strokes)  # Number of individual strokes in the multistroke gesture

        order = list(range(len(strokes)))  # Array of integer indices to represent the order of strokes
        orders = []  # Array of integer arrays to store all possible stroke order permutations
        HeapPermute(len(strokes), order, orders)

        unistrokes = MakeUnistrokes(strokes, orders)
        self.Unistrokes = []  # List to store unistrokes for this multistroke gesture
        for unistroke in unistrokes:
            self.Unistrokes.append(Unistroke(name, useBoundedRotationInvariance, unistroke))

class NDollarRecognizer:
    def __init__(self, useBoundedRotationInvariance, training_set=None):
        self.Multistrokes = []  # List to store multistroke gestures
        multiStrokePointSet = []  # Temporary list to store point sets of unistrokes for each multistroke gesture
        if training_set is None:
            training_set = template  # If no training set is provided, use the template
        for gesture, unistrokepointsList in training_set.items():  # Iterate through the training set
            unistrokePointSet = []  # Temporary list to store point sets for each unistroke of a multistroke gesture
            for pointSet in unistrokepointsList:  # Iterate through the point sets of a unistroke gesture
                for point in pointSet:
                    unistrokePointSet.append([point[0], point[1]])  # Convert points to a 2D list and append to unistroke point set
                multiStrokePointSet.append(deepcopy(unistrokePointSet))  # Deep copy the unistroke point set and append to the multistroke point set
                unistrokePointSet.clear()  # Clear the unistroke point set for the next iteration
            self.Multistrokes.append(Multistroke(gesture, useBoundedRotationInvariance, deepcopy(multiStrokePointSet)))  # Create Multistroke objects and append to the Multistrokes list
            multiStrokePointSet.clear()  # Clear the multistroke point set for the next iteration
        self.useBoundedRotationInvariance = useBoundedRotationInvariance  # Set the flag for bounded rotation invariance
    
    def Recognize(self, strokes, requireSameNoOfStrokes=False, useProtractor=False, with_Nbest = False):
        t0 = time()
        points = CombineStrokes(strokes) # make one connected unistroke from the given strokes
        candidate = Unistroke("", self.useBoundedRotationInvariance, points)

        u = -1
        b = float('inf')
        n_best_list = {}
        for i in range(len(self.Multistrokes)): # for each multistroke template
            if not requireSameNoOfStrokes or len(strokes) == self.Multistrokes[i].NumStrokes: # only attempt match when same # of component strokes
                min_d = 1
                for j in range(len(self.Multistrokes[i].Unistrokes)): # for each unistroke within this multistroke
                    if AngleBetweenUnitVectors(candidate.StartUnitVector, self.Multistrokes[i].Unistrokes[j].StartUnitVector) <= AngleSimilarityThreshold: # strokes start in the same direction
                        d = 0
                        if useProtractor:
                            d = OptimalCosineDistance(self.Multistrokes[i].Unistrokes[j].Vector, candidate.Vector) # Protractor
                        else:
                            d = DistanceAtBestAngle(candidate.Points, self.Multistrokes[i].Unistrokes[j], -AngleRange, +AngleRange, AnglePrecision) # Golden Section Search (original $N)
                        if d < min_d:
                            min_d = d
                        if d < b:
                            b = d # best (least) distance
                            u = i # multistroke owner of unistroke
                        if self.Multistrokes[i].Name not in n_best_list:
                            n_best_list[self.Multistrokes[i].Name] = round(1.0-d/HalfDiagonal,3)
                        else:
                            n_best_list[self.Multistrokes[i].Name] = max(n_best_list[self.Multistrokes[i].Name],round(1.0-d/HalfDiagonal,3))
        t1 = time()
        Nbest = dict(sorted(n_best_list.items(), key=lambda x:x[1], reverse=True))
        if with_Nbest:
            return Result("No match.", 0.0, t1-t0) if u == -1 else Result(self.Multistrokes[u].Name, 1.0 - b if useProtractor else 1.0 - b / HalfDiagonal, t1-t0), Nbest
        else:
            return Result("No match.", 0.0, t1-t0) if u == -1 else Result(self.Multistrokes[u].Name, 1.0 - b if useProtractor else 1.0 - b / HalfDiagonal, t1-t0)

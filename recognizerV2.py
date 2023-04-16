from recognizerV2Utils import *
from math import sqrt, sin, cos
from time import time
from online_template import template
from copy import deepcopy

NumMultistrokes = 16
NumPoints = 96
SquareSize = 250.0
OneDThreshold = 0.25
Origin = [0,0]
Diagonal = sqrt(SquareSize * SquareSize + SquareSize * SquareSize)
HalfDiagonal = 0.5 * Diagonal
AngleRange = Deg2Rad(45.0)
AnglePrecision = Deg2Rad(2.0)
Phi = 0.5 * (-1.0 + sqrt(5.0))
StartAngleIndex = int(NumPoints / 8)
AngleSimilarityThreshold = Deg2Rad(30.0)

class Unistroke:
    def __init__(self,name, use_bounded_rotation_invariance, points):
        self.Name = name
        self.Points = Resample(points, NumPoints)
        self.radians = IndicativeAngle(self.Points)
        self.Points = RotateBy(self.Points, -self.radians)
        self.Points = ScaleDimTo(self.Points, SquareSize, OneDThreshold)
        if use_bounded_rotation_invariance:
            self.Points = RotateBy(self.Points, self.radians) # restore
        self.Points = TranslateTo(self.Points, Origin)
        self.StartUnitVector = CalcStartUnitVector(self.Points, StartAngleIndex)
        self.Vector = Vectorize(self.Points, use_bounded_rotation_invariance) # for Protractor

class Multistroke:
    def __init__(self, name, useBoundedRotationInvariance, strokes):
        self.Name = name
        self.NumStrokes = len(strokes)  # number of individual strokes

        order = list(range(len(strokes)))  # array of integer indices
        orders = []  # array of integer arrays
        HeapPermute(len(strokes), order, orders)  # assuming HeapPermute is defined elsewhere

        unistrokes = MakeUnistrokes(strokes, orders)  # assuming MakeUnistrokes is defined elsewhere
        self.Unistrokes = []  # unistrokes for this multistroke
        for unistroke in unistrokes:
            self.Unistrokes.append(Unistroke(name, useBoundedRotationInvariance, unistroke))  # assuming Unistroke class is defined elsewhere


class NDollarRecognizer:
    def __init__(self, useBoundedRotationInvariance, training_set=None):
        self.Multistrokes = [] # array of multistrokes
        multiStrokePointSet = []
        if training_set is None:
            training_set = template
        for gesture,unistrokepointsList in training_set.items():
            unistrokePointSet = []
            for pointSet in unistrokepointsList:
                for point in pointSet:
                    unistrokePointSet.append([point[0],point[1]])
                multiStrokePointSet.append(deepcopy(unistrokePointSet))
                unistrokePointSet.clear()
            self.Multistrokes.append(Multistroke(gesture,useBoundedRotationInvariance, deepcopy(multiStrokePointSet)))
            multiStrokePointSet.clear()
        self.useBoundedRotationInvariance = useBoundedRotationInvariance
    
    def Recognize(self, strokes, requireSameNoOfStrokes=False, useProtractor=False):
        t0 = time()
        points = CombineStrokes(strokes) # make one connected unistroke from the given strokes
        candidate = Unistroke("", self.useBoundedRotationInvariance, points)

        u = -1
        b = float('inf')
        for i in range(len(self.Multistrokes)): # for each multistroke template
            if not requireSameNoOfStrokes or len(strokes) == self.Multistrokes[i].NumStrokes: # optional -- only attempt match when same # of component strokes
                for j in range(len(self.Multistrokes[i].Unistrokes)): # for each unistroke within this multistroke
                    if AngleBetweenUnitVectors(candidate.StartUnitVector, self.Multistrokes[i].Unistrokes[j].StartUnitVector) <= AngleSimilarityThreshold: # strokes start in the same direction
                        d = 0
                        if useProtractor:
                            d = OptimalCosineDistance(self.Multistrokes[i].Unistrokes[j].Vector, candidate.Vector) # Protractor
                        else:
                            d = DistanceAtBestAngle(candidate.Points, self.Multistrokes[i].Unistrokes[j], -AngleRange, +AngleRange, AnglePrecision) # Golden Section Search (original $N)
                        if d < b:
                            b = d # best (least) distance
                            u = i # multistroke owner of unistroke
        t1 = time()
        return Result("No match.", 0.0, t1-t0) if u == -1 else Result(self.Multistrokes[u].Name, 1.0 - b if useProtractor else 1.0 - b / HalfDiagonal, t1-t0)
    
    def AddGesture(self, name, strokes):
        self.Multistrokes.append(Multistroke(name, self.useBoundedRotationInvariance, strokes))
        num = sum(1 for m in self.Multistrokes if m.Name == name)
        return num
    
    def DeleteUserGestures(self):
        self.Multistrokes = self.Multistrokes[:NumMultistrokes] # clear any beyond the original set
        return NumMultistrokes

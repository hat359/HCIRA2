import math
from helper import * 
from point import Point,Rectangle
import time



class Unistroke:
    def __init__(self, name, use_bounded_rotation_invariance, points):
        self.Name = name
        # print(len(points))
        self.Points = Resample(points, NumPoints) # undefined function
        # print(len(self.Points))
        radians = IndicativeAngle(self.Points) # undefined function
        # for p in self.Points:
        #     print(p.X,p.Y)
        self.Points = RotateBy(self.Points, -radians) # undefined function
        
        self.Points = ScaleDimTo(self.Points, SquareSize, OneDThreshold) # undefined variable
        
        if use_bounded_rotation_invariance:
            self.Points = RotateBy(self.Points, +radians) # undefined function
        self.Points = TranslateTo(self.Points, Origin) # undefined variable
        # sti = int(len(self.Points)/8)
        self.StartUnitVector = calc_start_unit_vector(self.Points, StartAngleIndex) 
        # self.StartUnitVector = calc_start_unit_vector(self.Points, sti)
        self.Vector = Vectorize(self.Points, use_bounded_rotation_invariance) # undefined function


class Multistroke:
    def __init__(self, name, use_bounded_rotation_invariance, strokes):
        self.Name = name
        self.NumStrokes = len(strokes)

        order = list(range(len(strokes)))
        orders = [] # array of integer arrays
        HeapPermute(len(strokes), order, orders) # undefined function

        unistrokes = MakeUnistrokes(strokes, orders) # undefined function
        self.Unistrokes = []
        for j in range(len(unistrokes)):
            self.Unistrokes.append(Unistroke(name, use_bounded_rotation_invariance, unistrokes[j]))



class Result:
    def __init__(self, name, score, ms):
        self.Name = name
        self.Score = score
        self.Time = ms

# NDollarRecognizer constants
NumMultistrokes = 16
NumPoints = 96
SquareSize = 250.0
OneDThreshold = 0.25 # customize to desired gesture set (usually 0.20 - 0.35)
Origin = Point(0, 0)
Diagonal = math.sqrt(SquareSize * SquareSize + SquareSize * SquareSize)
HalfDiagonal = 0.5 * Diagonal
AngleRange = deg2rad(45.0)
AnglePrecision = deg2rad(2.0)
Phi = 0.5 * (-1.0 + math.sqrt(5.0)) # Golden Ratio
StartAngleIndex = int(NumPoints / 8) # eighth of gesture length
AngleSimilarityThreshold = deg2rad(30.0)



class NDollarRecognizer:
    def __init__(self, useBoundedRotationInvariance):
        self.Multistrokes = [None] * NumMultistrokes
        self.Multistrokes[0] = Multistroke("T", useBoundedRotationInvariance, [
            [Point(30,7),Point(103,7)],
            [Point(66,7),Point(66,87)]
        ])
        self.Multistrokes[1] = Multistroke("N", useBoundedRotationInvariance, [
            [Point(177,92),Point(177,2)],
            [Point(182,1),Point(246,95)],
            [Point(247,87),Point(247,1)]
        ])
        self.Multistrokes[2] = Multistroke("D", useBoundedRotationInvariance, [
            [Point(345,9),Point(345,87)],
            [Point(351,8),Point(363,8),Point(372,9),Point(380,11),Point(386,14),Point(391,17),Point(394,22),Point(397,28),Point(399,34),Point(400,42),Point(400,50),Point(400,56),Point(399,61),Point(397,66),Point(394,70),Point(391,74),Point(386,78),Point(382,81),Point(377,83),Point(372,85),Point(367,87),Point(360,87),Point(355,88),Point(349,87)]
        ])
        self.Multistrokes[3] = Multistroke("P", useBoundedRotationInvariance, [
            [Point(507,8),Point(507,87)],
            [Point(513,7),Point(528,7),Point(537,8),Point(544,10),Point(550,12),Point(555,15),Point(558,18),Point(560,22),Point(561,27),Point(562,33),Point(561,37),Point(559,42),Point(556,45),Point(550,48),Point(544,51),Point(538,53),Point(532,54),Point(525,55),Point(519,55),Point(513,55),Point(510,55)]
        ])
        self.Multistrokes[4] = Multistroke("X", useBoundedRotationInvariance, [
            [Point(30,146),Point(106,222)],
            [Point(30,225),Point(106,146)]
        ])
        self.Multistrokes[5] = Multistroke("H", useBoundedRotationInvariance, [
            [Point(188,137),Point(188,225)],
            [Point(188,180),Point(241,180)],
            [Point(241,137),Point(241,225)]
        ])
        self.Multistrokes[6] = Multistroke("I", useBoundedRotationInvariance, [
            [Point(371,149),Point(371,221)],
            [Point(341,149),Point(401,149)],
            [Point(341,221),Point(401,221)]
        ])
        self.Multistrokes[7] = Multistroke("exclamation", useBoundedRotationInvariance, [
            [Point(526,142),Point(526,204)],
            [Point(526,221)]
        ])
       
        self.Multistrokes[8] = Multistroke("line", useBoundedRotationInvariance, [
            [Point(12,347),Point(119,347)]
        ])

        self.Multistrokes[9] = Multistroke("five-point star", useBoundedRotationInvariance, [
            [Point(177,396),Point(223,299),Point(262,396),Point(168,332),Point(278,332),Point(184,397)]
        ])
        self.Multistrokes[10] = Multistroke("null", useBoundedRotationInvariance, [
            [Point(382,310),Point(377,308),Point(373,307),Point(366,307),Point(360,310),Point(356,313),Point(353,316),Point(349,321),Point(347,326),Point(344,331),Point(342,337),Point(341,343),Point(341,350),Point(341,358),Point(342,362),Point(344,366),Point(347,370),Point(351,374),Point(356,379),Point(361,382),Point(368,385),Point(374,387),Point(381,387),Point(390,387),Point(397,385),Point(404,382),Point(408,378),Point(412,373),Point(416,367),Point(418,361),Point(419,353),Point(418,346),Point(417,341),Point(416,336),Point(413,331),Point(410,326),Point(404,320),Point(400,317),Point(393,313),Point(392,312)],
            [Point(418,309),Point(337,390)]
        ])
        self.Multistrokes[11] = Multistroke("arrowhead", useBoundedRotationInvariance, [
            [Point(506,349),Point(574,349)],
            [Point(525,306),Point(584,349),Point(525,388)]
        ])
        self.Multistrokes[12] = Multistroke("pitchfork", useBoundedRotationInvariance, [
            [Point(38,470),Point(36,476),Point(36,482),Point(37,489),Point(39,496),Point(42,500),Point(46,503),Point(50,507),Point(56,509),Point(63,509),Point(70,508),Point(75,506),Point(79,503),Point(82,499),Point(85,493),Point(87,487),Point(88,480),Point(88,474),Point(87,468)],
            [Point(62,464),Point(62,571)]
        ])
        self.Multistrokes[13] = Multistroke("six-point star", useBoundedRotationInvariance, [
            [Point(177,554),Point(223,476),Point(268,554),Point(183,554)],
            [Point(177,490),Point(223,568),Point(268,490),Point(183,490)]
        ])
        self.Multistrokes[14] = Multistroke("asterisk", useBoundedRotationInvariance, [
            [Point(325,499),Point(417,557)],
            [Point(417,499),Point(325,557)],
            [Point(371,486),Point(371,571)]
        ])


        self.Multistrokes[15] = Multistroke("half-note", useBoundedRotationInvariance, [
            [Point(546, 465), Point(546, 531)],
            [Point(540, 530), Point(536, 529), Point(533, 528), Point(529, 529), Point(524, 530), 
            Point(520, 532), Point(515, 535), Point(511, 539), Point(508, 545), Point(506, 548),
            Point(506, 554), Point(509, 558), Point(512, 561), Point(517, 564), Point(521, 564),
            Point(527, 563), Point(531, 560), Point(535, 557), Point(538, 553), Point(542, 548),
            Point(544, 544), Point(546, 540), Point(546, 536)]
        ])



    def Recognize(self, strokes, use_bounded_rotation_invariance, require_same_no_of_strokes, use_protractor):
        t0 = time.time()
        points = CombineStrokes(strokes) # make one connected unistroke from the given strokes
        print(len(points))
        for p in points:
            print(p.X,p.Y)
        candidate = Unistroke("", use_bounded_rotation_invariance, points)

        u = -1
        b = float('inf')
        # print("hehehjefjfeefefefe")
        # print(len(self.Multistrokes))
        NDollarRecognizer(True)
        for i in range(len(self.Multistrokes)): # for each multistroke template
            if not require_same_no_of_strokes or len(strokes) == self.Multistrokes[i].NumStrokes: # optional -- only attempt match when same # of component strokes
                for j in range(len(self.Multistrokes[i].Unistrokes)): # for each unistroke within this multistroke
                    if angle_between_unit_vectors(candidate.StartUnitVector, self.Multistrokes[i].Unistrokes[j].StartUnitVector) <= AngleSimilarityThreshold: # strokes start in the same direction
                        d = None
                        if use_protractor:
                            d = OptimalCosineDistance(self.Multistrokes[i].Unistrokes[j].Vector, candidate.Vector) # Protractor
                        else:
                            d = DistanceAtBestAngle(candidate.Points, self.Multistrokes[i].Unistrokes[j], -AngleRange, +AngleRange, AnglePrecision) # Golden Section Search (original $N)
                        if d < b:
                            b = d # best (least) distance
                            u = i # multistroke owner of unistroke

        t1 = time.time()
        return Result("No match.", 0.0, t1-t0) if u == -1 else Result(self.Multistrokes[u].Name, 1.0 - b if use_protractor else 1.0 - b / HalfDiagonal, t1-t0)

    def AddGesture(self, name, use_bounded_rotation_invariance, strokes):
        self.Multistrokes.append(Multistroke(name, use_bounded_rotation_invariance, strokes))
        num = 0
        for i in range(len(self.Multistrokes)):
            if self.Multistrokes[i].Name == name:
                num += 1
        return num

    def DeleteUserGestures(self):
        self.Multistrokes = self.Multistrokes[:NumMultistrokes] # clear any beyond the original set
        return NumMultistrokes



# Private helper functions from here on down
def HeapPermute(n, order, orders):
    if n == 1:
        orders.append(order.copy()) # append copy
    else:
        for i in range(n):
            HeapPermute(n - 1, order, orders)
            if n % 2 == 1: # swap 0, n-1
                tmp = order[0]
                order[0] = order[n - 1]
                order[n - 1] = tmp
            else: # swap i, n-1
                tmp = order[i]
                order[i] = order[n - 1]
                order[n - 1] = tmp




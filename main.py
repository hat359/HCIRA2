class Point:
    def __init__(self, x, y):
        self.X = x
        self.Y = y


class Rectangle:
    def __init__(self, x, y, width, height):
        self.X = x
        self.Y = y
        self.Width = width
        self.Height = height


class Unistroke:
    def __init__(self, name, use_bounded_rotation_invariance, points):
        self.Name = name
        self.Points = Resample(points, NumPoints) # undefined function
        radians = IndicativeAngle(self.Points) # undefined function
        self.Points = RotateBy(self.Points, -radians) # undefined function
        self.Points = ScaleDimTo(self.Points, SquareSize, OneDThreshold) # undefined variable
        if use_bounded_rotation_invariance:
            self.Points = RotateBy(self.Points, +radians) # undefined function
        self.Points = TranslateTo(self.Points, Origin) # undefined variable
        self.StartUnitVector = CalcStartUnitVector(self.Points, StartAngleIndex) # undefined function
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
AngleRange = Deg2Rad(45.0)
AnglePrecision = Deg2Rad(2.0)
Phi = 0.5 * (-1.0 + math.sqrt(5.0)) # Golden Ratio
StartAngleIndex = int(NumPoints / 8) # eighth of gesture length
AngleSimilarityThreshold = Deg2Rad(30.0)



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


        self.Multistrokes[15] = Multistroke("half-note", use_bounded_rotation_invariance, [
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
        candidate = Unistroke("", use_bounded_rotation_invariance, points)

        u = -1
        b = float('inf')
        for i in range(len(self.Multistrokes)): # for each multistroke template
            if not require_same_no_of_strokes or len(strokes) == self.Multistrokes[i].NumStrokes: # optional -- only attempt match when same # of component strokes
                for j in range(len(self.Multistrokes[i].Unistrokes)): # for each unistroke within this multistroke
                    if AngleBetweenUnitVectors(candidate.StartUnitVector, self.Multistrokes[i].Unistrokes[j].StartUnitVector) <= AngleSimilarityThreshold: # strokes start in the same direction
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



# Helper function

def MakeUnistrokes(strokes, orders):
    unistrokes = [] # array of point arrays
    for r in range(len(orders)):
        for b in range(2 ** len(orders[r])): # use b's bits for directions
            unistroke = [] # array of points
            for i in range(len(orders[r])):
                pts = []
                if ((b >> i) & 1) == 1:  # is b's bit at index i on?
                    pts = strokes[orders[r][i]][::-1].copy() # copy and reverse
                else:
                    pts = strokes[orders[r][i]].copy() # copy
                for p in range(len(pts)):
                    unistroke.append(pts[p]) # append points
            unistrokes.append(unistroke) # add one unistroke to set
    return unistrokes

def CombineStrokes(strokes):
    points = []
    for s in range(len(strokes)):
        for p in range(len(strokes[s])):
            points.append(Point(strokes[s][p].X, strokes[s][p].Y))
    return points

def Resample(points, n):
    I = PathLength(points) / (n - 1) # interval length
    D = 0.0
    newpoints = [points[0]]
    for i in range(1, len(points)):
        d = Distance(points[i-1], points[i])
        if (D + d) >= I:
            qx = points[i-1].X + ((I - D) / d) * (points[i].X - points[i-1].X)
            qy = points[i-1].Y + ((I - D) / d) * (points[i].Y - points[i-1].Y)
            q = Point(qx, qy)
            newpoints.append(q) # append new point 'q'
            points.insert(i, q) # insert 'q' at position i in points s.t. 'q' will be the next i
            D = 0.0
        else:
            D += d
    if len(newpoints) == n - 1: # somtimes we fall a rounding-error short of adding the last point, so add it if so
        newpoints.append(Point(points[len(points) - 1].X, points[len(points) - 1].Y))
    return newpoints

def IndicativeAngle(points):
    c = Centroid(points)
    return math.atan2(c.Y - points[0].Y, c.X - points[0].X)



def Centroid(points):
    n = len(points)
    sx = sum([p.X for p in points])
    sy = sum([p.Y for p in points])
    return Point(sx / n, sy / n)

def BoundingBox(points):
    minX = minY = float('inf')
    maxX = maxY = float('-inf')
    for p in points:
        if p.X < minX: minX = p.X
        if p.X > maxX: maxX = p.X
        if p.Y < minY: minY = p.Y
        if p.Y > maxY: maxY = p.Y
    return Point(minX, minY), Point(maxX, maxY)

def RotateBy(points, radians):
    c = Centroid(points)
    cos = math.cos(radians)
    sin = math.sin(radians)
    newpoints = []
    for p in points:
        qx = (p.X - c.X) * cos - (p.Y - c.Y) * sin + c.X
        qy = (p.X - c.X) * sin + (p.Y - c.Y) * cos + c.Y
        newpoints.append(Point(qx, qy))
    return newpoints

def ScaleDimTo(points, size, ratio1D):
    (minX, minY), (maxX, maxY) = BoundingBox(points)
    uniformly = min(maxX - minX, maxY - minY) / max(maxX - minX, maxY - minY) <= ratio1D
    newpoints = []
    for p in points:
        qx = p.X * (size / (maxX - minX if uniformly else maxX))
        qy = p.Y * (size / (maxY - minY if uniformly else maxY))
        newpoints.append(Point(qx, qy))
    return newpoints

def TranslateTo(points, pt):
    c = Centroid(points)
    newpoints = []
    for p in points:
        qx = p.X + pt.X - c.X
        qy = p.Y + pt.Y - c.Y
        newpoints.append(Point(qx, qy))
    return newpoints

def Vectorize(points, useBoundedRotationInvariance):
    cos = 1.0
    sin = 0.0
    if useBoundedRotationInvariance:
        iAngle = math.atan2(points[0].Y, points[0].X)
        baseOrientation = (math.pi / 4.0) * math.floor((iAngle + math.pi / 8.0) / (math.pi / 4.0))
        cos = math.cos(baseOrientation - iAngle)
        sin = math.sin(baseOrientation - iAngle)
    sum = 0.0
    vector = []
    for p in points:
        newX = p.X * cos - p.Y * sin
        newY = p.Y * cos + p.X * sin
        vector.extend([newX, newY])
        sum += newX * newX + newY * newY
    magnitude = math.sqrt(sum)
    for i in range(len(vector)):
        vector[i] /= magnitude
    return vector
    

# calculate the optimal cosine distance between two vectors using the protractor method
def OptimalCosineDistance(v1, v2):
    a = 0.0
    b = 0.0
    for i in range(0, len(v1), 2):
        a += v1[i] * v2[i] + v1[i+1] * v2[i+1]
        b += v1[i] * v2[i+1] - v1[i+1] * v2[i]
    angle = math.atan(b / a)
    return math.acos(a * math.cos(angle) + b * math.sin(angle))

# find the distance at the best angle between two vectors
def DistanceAtBestAngle(points, T, a, b, threshold):
    x1 = Phi * a + (1.0 - Phi) * b
    f1 = DistanceAtAngle(points, T, x1)
    x2 = (1.0 - Phi) * a + Phi * b
    f2 = DistanceAtAngle(points, T, x2)
    while abs(b - a) > threshold:
        if f1 < f2:
            b = x2
            x2 = x1
            f2 = f1
            x1 = Phi * a + (1.0 - Phi) * b
            f1 = DistanceAtAngle(points, T, x1)
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = (1.0 - Phi) * a + Phi * b
            f2 = DistanceAtAngle(points, T, x2)
    return min(f1, f2)

# find the distance at a given angle between two vectors
def DistanceAtAngle(points, T, radians):
    newpoints = RotateBy(points, radians)
    return PathDistance(newpoints, T.Points)



def path_distance(pts1, pts2):
    # average distance between corresponding points in two paths
    d = 0.0
    for i in range(len(pts1)):
        # assumes pts1.length == pts2.length
        d += distance(pts1[i], pts2[i])
    return d / len(pts1)

def path_length(points):
    # length traversed by a point path
    d = 0.0
    for i in range(1, len(points)):
        d += distance(points[i-1], points[i])
    return d

def distance(p1, p2):
    # distance between two points
    dx = p2['X'] - p1['X']
    dy = p2['Y'] - p1['Y']
    return math.sqrt(dx * dx + dy * dy)

def calc_start_unit_vector(points, index):
    # start angle from points[0] to points[index] normalized as a unit vector
    v = {'X': points[index]['X'] - points[0]['X'], 'Y': points[index]['Y'] - points[0]['Y']}
    len_v = math.sqrt(v['X'] * v['X'] + v['Y'] * v['Y'])
    return {'X': v['X'] / len_v, 'Y': v['Y'] / len_v}

def angle_between_unit_vectors(v1, v2):
    # gives acute angle between unit vectors from (0,0) to v1, and (0,0) to v2
    n = v1['X'] * v2['X'] + v1['Y'] * v2['Y']
    c = max(-1.0, min(1.0, n))  # ensure [-1,+1]
    return math.acos(c)  # arc cosine of the vector dot product

def deg2rad(d):
    return d * math.pi / 180.0

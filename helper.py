# Helper function
import math
from point import Point,Rectangle

Phi = 0.5 * (-1.0 + math.sqrt(5.0)) # Golden Ratio

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
            points.append(Point(strokes[s][p][0], strokes[s][p][1]))
    return points

def Resample(points, n):
    I = path_length(points) / (n - 1) # interval length
    D = 0.0
    # print(len(points),I,path_length(points))
    newpoints = [points[0]]
    for i in range(1, len(points)):
        d = distance(points[i-1], points[i])
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
    return points

def IndicativeAngle(points):
    c = Centroid(points)
    return math.atan2(c.Y - points[0].Y, c.X - points[0].X)



def Centroid(points):
    n = len(points)
    sx = sum([p.X for p in points])
    sy = sum([p.Y for p in points])
    return Point(sx / n, sy / n)

def BoundingBox(points):
    
    minX, maxX, minY, maxY = float('inf'), float('-inf'), float('inf'), float('-inf')
    for point in points:
        minX = min(minX, point.X)
        minY = min(minY, point.Y)
        maxX = max(maxX, point.X)
        maxY = max(maxY, point.Y)
        # print(minX,minY,maxX,maxY)
    return Rectangle(minX, minY, maxX - minX, maxY - minY)

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
    B = BoundingBox(points)
    print(B.Height)
    uniformly = min(B.Width / B.Height, B.Height / B.Width) <= ratio1D  # 1D or 2D gesture test
    newpoints = []
    for i in range(len(points)):
        qx = points[i].X * (size / max(B.Width, B.Height)) if uniformly else points[i].X * (size / B.Width)
        qy = points[i].Y * (size / max(B.Width, B.Height)) if uniformly else points[i].Y * (size / B.Height)
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
    return path_distance(newpoints, T.Points)



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
    dx = p2.X - p1.X
    dy = p2.Y - p1.Y
    return math.sqrt(dx * dx + dy * dy)

def calc_start_unit_vector(points, index):
    print(index)
    # start angle from points[0] to points[index] normalized as a unit vector
    v = {'X': points[index].X - points[0].X, 'Y': points[index].Y - points[0].Y}
    len_v = math.sqrt(v['X'] * v['X'] + v['Y'] * v['Y'])
    return {'X': v['X'] / len_v, 'Y': v['Y'] / len_v}

def angle_between_unit_vectors(v1, v2):
    # gives acute angle between unit vectors from (0,0) to v1, and (0,0) to v2
    n = v1.X * v2.X + v1.Y * v2.Y
    c = max(-1.0, min(1.0, n))  # ensure [-1,+1]
    return math.acos(c)  # arc cosine of the vector dot product

def deg2rad(d):
    return d * math.pi / 180.0



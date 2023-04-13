from math import pi, sqrt, atan2, cos, sin, floor, acos, atan
from commonUtils import *
Phi = 0.5 * (-1.0 + sqrt(5.0))

def Resample(points, n):
    I = PathLength(points) / (n - 1) # interval length
    D = 0.0
    newpoints = [Point(points[0].X, points[0].Y)]
    i = 1
    while i < len(points):
        d = Distance(points[i-1], points[i])
        if (D + d) >= I:
            qx = points[i-1].X + ((I - D) / d) * (points[i].X - points[i-1].X)
            qy = points[i-1].Y + ((I - D) / d) * (points[i].Y - points[i-1].Y)
            q = Point(qx, qy)
            newpoints.append(q) # append new point 'q'
            points.insert(i, q) # insert 'q' at position i in points so that 'q' will be the next i
            D = 0.0
        else:
            D += d
        i += 1
    if len(newpoints) == n - 1: # sometimes we fall a rounding-error short of adding the last point, so add it if so
        newpoints.append(Point(points[-1].X, points[-1].Y))
    return newpoints

def IndicativeAngle(points):
    c = Centroid(points)
    return atan2(c.Y - points[0].Y, c.X - points[0].X)

def RotateBy(points, radians):
    c = Centroid(points)
    cosine = cos(radians)
    sine = sin(radians)
    newpoints = []
    for p in points:
        qx = (p.X - c.X) * cosine - (p.Y - c.Y) * sine + c.X
        qy = (p.X - c.X) * sine + (p.Y - c.Y) * cosine + c.Y
        newpoints.append(Point(qx, qy))
    return newpoints

def ScaleDimTo(points, size, ratio1D):
    R = BoundingBox(points)
    uniformly = min(R.Width / R.Height, R.Height / R.Width) <= ratio1D  # 1D or 2D gesture test
    newpoints = []
    for p in points:
        qx = p.X * (size / max(R.Width, R.Height)) if uniformly else p.X * (size / R.Width)
        qy = p.Y * (size / max(R.Width, R.Height)) if uniformly else p.Y * (size / R.Height)
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

def Deg2Rad(d):
    return (d * pi / 180.0)

def PathLength(points):
    length = 0.0
    for i in range(1, len(points)):
        length += Distance(points[i-1], points[i])
    return length

def Distance(p1, p2):
    dx = p2.X - p1.X
    dy = p2.Y - p1.Y
    return sqrt(dx*dx + dy*dy)

def LogPoints(points):
    for point in points:
        print(point.display(),end=' ')

def Centroid(points):
    x = 0.0
    y = 0.0
    for p in points:
        x += p.X
        y += p.Y
    x /= len(points)
    y /= len(points)
    return Point(x, y)

def BoundingBox(points):
    minX = float('inf')
    maxX = float('-inf')
    minY = float('inf')
    maxY = float('-inf')
    for p in points:
        minX = min(minX, p.X)
        minY = min(minY, p.Y)
        maxX = max(maxX, p.X)
        maxY = max(maxY, p.Y)
    return Rectangle(minX, minY, maxX - minX, maxY - minY)

def CalcStartUnitVector(points, index):
    v = Point(points[index].X - points[0].X, points[index].Y - points[0].Y)
    len = ((v.X ** 2) + (v.Y ** 2)) ** 0.5
    return Point(v.X / len, v.Y / len)

def Vectorize(points, useBoundedRotationInvariance):
    cosine = 1.0
    sine = 0.0
    if useBoundedRotationInvariance:
        iAngle = atan2(points[0].Y, points[0].X)
        baseOrientation = (pi / 4.0) * floor((iAngle + pi / 8.0) / (pi / 4.0))
        cosine = cos(baseOrientation - iAngle)
        sine = sin(baseOrientation - iAngle)
    sum = 0.0
    vector = []
    for i in range(len(points)):
        newX = points[i].X * cosine - points[i].Y * sine
        newY = points[i].Y * cosine + points[i].X * sine
        vector.append(newX)
        vector.append(newY)
        sum += newX * newX + newY * newY
    magnitude = sqrt(sum)
    for i in range(len(vector)):
        vector[i] /= magnitude
    return vector

def HeapPermute(n, order, orders):
    if n == 1:
        orders.append(order.copy())  # append copy
    else:
        for i in range(n):
            HeapPermute(n - 1, order, orders)
            if n % 2 == 1:  # swap 0, n-1
                order[0], order[n - 1] = order[n - 1], order[0]
            else:  # swap i, n-1
                order[i], order[n - 1] = order[n - 1], order[i]

def MakeUnistrokes(strokes, orders):
    unistrokes = []  # array of point arrays
    for r in range(len(orders)):
        for b in range(2 ** len(orders[r])):  # use b's bits for directions
            unistroke = []  # array of points
            for i in range(len(orders[r])):
                pts = []
                if ((b >> i) & 1) == 1:  # is b's bit at index i on?
                    pts = strokes[orders[r][i]].copy()[::-1]  # copy and reverse
                else:
                    pts = strokes[orders[r][i]].copy()  # copy
                unistroke += pts  # append points
            unistrokes.append(unistroke)  # add one unistroke to set
    return unistrokes

def CombineStrokes(strokes):
    points = []
    for s in range(len(strokes)):
        for p in range(len(strokes[s])):
            points.append(Point(strokes[s][p].X, strokes[s][p].Y))
    return points


def AngleBetweenUnitVectors(v1, v2):
    n = (v1.X * v2.X + v1.Y * v2.Y)
    c = max(-1.0, min(1.0, n)) # ensure [-1,+1]
    return acos(c) # arc cosine of the vector dot product

def OptimalCosineDistance(v1, v2):
    a = 0.0
    b = 0.0
    for i in range(0, len(v1), 2):
        a += v1[i] * v2[i] + v1[i+1] * v2[i+1]
        b += v1[i] * v2[i+1] - v1[i+1] * v2[i]
    angle = atan(b / a)
    return acos(a * cos(angle) + b * sin(angle))

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

def DistanceAtAngle(points, T, radians):
	newpoints = RotateBy(points, radians)
	return PathDistance(newpoints, T.Points)

def PathDistance(pts1, pts2):
    d = 0.0
    for i in range(len(pts1)):  # assumes len(pts1) == len(pts2)
        d += Distance(pts1[i], pts2[i])
    return d / len(pts1)

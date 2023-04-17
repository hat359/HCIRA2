from math import pi, sqrt, atan2, cos, sin, floor, acos, atan
from commonUtils import *
Phi = 0.5 * (-1.0 + sqrt(5.0))

# Function to resample points to a specified number of points
def Resample(points, n):
    I = PathLength(points) / (n - 1) # interval length
    D = 0.0
    newpoints = [[points[0][0], points[0][1]]] # start with the first point in the list of points
    i = 1
    while i < len(points):
        d = Distance(points[i-1], points[i]) # compute distance between consecutive points
        if (D + d) >= I:
            qx = points[i-1][0] + ((I - D) / d) * (points[i][0] - points[i-1][0]) # interpolate x-coordinate
            qy = points[i-1][1] + ((I - D) / d) * (points[i][1] - points[i-1][1]) # interpolate y-coordinate
            q = [qx,qy]
            newpoints.append(q) # append new point 'q'
            points.insert(i, q) # insert 'q' at position i in points so that 'q' will be the next i
            D = 0.0
        else:
            D += d
        i += 1
    if len(newpoints) == n - 1: # sometimes we fall a rounding-error short of adding the last point, so add it if so
        newpoints.append([points[-1][0], points[-1][1]])
    return newpoints

# Function to compute the indicative angle of a set of points
def IndicativeAngle(points):
    c = Centroid(points) # compute centroid of points
    return atan2(c[1] - points[0][1], c[0] - points[0][0]) # compute angle between centroid and the first point

# Function to rotate points by a specified angle
def RotateBy(points, radians):
    c = Centroid(points) # compute centroid of points
    cosine = cos(radians)
    sine = sin(radians)
    newpoints = []
    for p in points:
        qx = (p[0] - c[0]) * cosine - (p[1] - c[1]) * sine + c[0] # apply rotation formula for x-coordinate
        qy = (p[0] - c[0]) * sine + (p[1] - c[1]) * cosine + c[1] # apply rotation formula for y-coordinate
        newpoints.append([qx,qy]) # append rotated point to newpoints list
    return newpoints

def ScaleDimTo(points, size, ratio1D):
    R = BoundingBox(points)  # Calculate the bounding box of the points
    R.Height = 0.1 if R.Height == 0 else R.Height  # Set height to a small value if it is 0
    R.Width = 0.1 if R.Width == 0 else R.Width  # Set width to a small value if it is 0
    uniformly = min(R.Width / R.Height, R.Height / R.Width) <= ratio1D  # 1D or 2D gesture test - determine if the gesture is 1D or 2D based on ratio1D
    newpoints = []
    for p in points:
        qx = p[0] * (size / max(R.Width, R.Height)) if uniformly else p[0] * (size / R.Width)  # Scale x coordinate uniformly or non-uniformly based on the gesture type
        qy = p[1] * (size / max(R.Width, R.Height)) if uniformly else p[1] * (size / R.Height)  # Scale y coordinate uniformly or non-uniformly based on the gesture type
        newpoints.append([qx,qy])  # Add the scaled point to the newpoints list
    return newpoints

def TranslateTo(points, pt):
    c = Centroid(points)  # Calculate the centroid of the points
    newpoints = []
    for p in points:
        qx = p[0] + pt[0] - c[0]  # Translate x coordinate by the difference between the translation point and centroid
        qy = p[1] + pt[1] - c[1]  # Translate y coordinate by the difference between the translation point and centroid
        newpoints.append([qx,qy])  # Add the translated point to the newpoints list
    return newpoints

def Deg2Rad(d):
    return (d * pi / 180.0)  # Convert angle from degrees to radians

def PathLength(points):
    length = 0.0
    for i in range(1, len(points)):
        length += Distance(points[i-1], points[i])  # Calculate the distance between consecutive points and add it to the total length
    return length

def Distance(p1, p2):
    dx = p2[0] - p1[0]  # Calculate the difference in x coordinates
    dy = p2[1] - p1[1]  # Calculate the difference in y coordinates
    return sqrt(dx*dx + dy*dy)  # Calculate the Euclidean distance between the two points

def Centroid(points):
    x = 0.0
    y = 0.0
    for p in points:
        x += p[0]  # Sum up x coordinates
        y += p[1]  # Sum up y coordinates
    x /= len(points)  # Divide sum of x coordinates by total number of points to get average x coordinate
    y /= len(points)  # Divide sum of y coordinates by total number of points to get average y coordinate
    return [x,y]  # Return the centroid as a list containing the average x and y coordinates

def BoundingBox(points):
    minX = float('inf')  # Initialize the minimum x-coordinate with positive infinity
    maxX = float('-inf')  # Initialize the maximum x-coordinate with negative infinity
    minY = float('inf')  # Initialize the minimum y-coordinate with positive infinity
    maxY = float('-inf')  # Initialize the maximum y-coordinate with negative infinity
    for p in points:  # Iterate through each point in the input points
        minX = min(minX, p[0])  # Update the minimum x-coordinate if a smaller value is found
        minY = min(minY, p[1])  # Update the minimum y-coordinate if a smaller value is found
        maxX = max(maxX, p[0])  # Update the maximum x-coordinate if a larger value is found
        maxY = max(maxY, p[1])  # Update the maximum y-coordinate if a larger value is found
    return Rectangle(minX, minY, maxX - minX, maxY - minY)  # Return a rectangle object representing the bounding box


def CalcStartUnitVector(points, index):
    v = [points[index][0] - points[0][0], points[index][1] - points[0][1]]  # Calculate the vector between the index-th point and the first point
    len = ((v[0] ** 2) + (v[1] ** 2)) ** 0.5  # Calculate the length of the vector
    return [v[0] / len, v[1] / len]  # Return the normalized vector as a list


def Vectorize(points, useBoundedRotationInvariance):
    cosine = 1.0  # Initialize cosine with 1.0
    sine = 0.0  # Initialize sine with 0.0
    if useBoundedRotationInvariance:  # If bounded rotation invariance is enabled
        iAngle = atan2(points[0][1], points[0][0])  # Calculate the angle between the first point and the origin
        baseOrientation = (pi / 4.0) * floor((iAngle + pi / 8.0) / (pi / 4.0))  # Calculate the base orientation angle
        cosine = cos(baseOrientation - iAngle)  # Calculate cosine of the angle difference
        sine = sin(baseOrientation - iAngle)  # Calculate sine of the angle difference
    sum = 0.0  # Initialize sum with 0.0
    vector = []  # Initialize an empty list for storing the vector components
    for i in range(len(points)):  # Iterate through each point in the input points
        newX = points[i][0] * cosine - points[i][1] * sine  # Rotate the point's x-coordinate
        newY = points[i][1] * cosine + points[i][0] * sine  # Rotate the point's y-coordinate
        vector.append(newX)  # Append the rotated x-coordinate to the vector
        vector.append(newY)  # Append the rotated y-coordinate to the vector
        sum += newX * newX + newY * newY  # Add the squared components to the sum
    magnitude = sqrt(sum)  # Calculate the magnitude of the vector
    for i in range(len(vector)):  # Iterate through each component of the vector
        vector[i] /= magnitude  # Normalize the vector components by dividing them by the magnitude
    return vector  # Return the normalized vector as a list


def HeapPermute(n, order, orders):
    if n == 1:
        orders.append(order.copy())  # append copy of order to orders list when n == 1
    else:
        for i in range(n):
            HeapPermute(n - 1, order, orders)  # recursively generate permutations
            if n % 2 == 1:  # swap 0, n-1 if n is odd
                order[0], order[n - 1] = order[n - 1], order[0]
            else:  # swap i, n-1 if n is even
                order[i], order[n - 1] = order[n - 1], order[i]

def MakeUnistrokes(strokes, orders):
    unistrokes = []  # array of point arrays
    for r in range(len(orders)):
        for b in range(2 ** len(orders[r])):  # use b's bits for directions
            unistroke = []  # array of points
            for i in range(len(orders[r])):
                pts = []
                if ((b >> i) & 1) == 1:  # check if b's bit at index i is on
                    pts = strokes[orders[r][i]].copy()[::-1]  # copy and reverse the stroke points
                else:
                    pts = strokes[orders[r][i]].copy()  # copy the stroke points
                unistroke += pts  # append points to unistroke
            unistrokes.append(unistroke)  # add one unistroke to the set of unistrokes
    return unistrokes

def CombineStrokes(strokes):
    points = []
    for s in range(len(strokes)):
        for p in range(len(strokes[s])):
            points.append([strokes[s][p][0], strokes[s][p][1]])  # extract x, y coordinates from strokes and append to points list
    return points

def AngleBetweenUnitVectors(v1, v2):
    n = (v1[0] * v2[0] + v1[1] * v2[1])  # calculate dot product of v1 and v2
    c = max(-1.0, min(1.0, n)) # ensure dot product is within [-1,+1]
    return acos(c) # calculate arc cosine of the dot product, which gives the angle between the unit vectors

def OptimalCosineDistance(v1, v2):
    a = 0.0
    b = 0.0
    for i in range(0, len(v1), 2):
        a += v1[i] * v2[i] + v1[i+1] * v2[i+1]  # calculate dot product of v1 and v2 at corresponding indices and accumulate to a
        b += v1[i] * v2[i+1] - v1[i+1] * v2[i]  # calculate cross product of v1 and v2 at corresponding indices and accumulate to b
    angle = atan(b / a)  # calculate arctangent of the ratio of cross product to dot product to get the angle
    return acos(a * cos(angle) + b * sin(angle))  # calculate arc cosine of the sum of dot product and scaled cross product using trigonometric identities

def DistanceAtBestAngle(points, T, a, b, threshold):
    x1 = Phi * a + (1.0 - Phi) * b  # calculate a new angle x1 by interpolating between a and b using the golden ratio
    f1 = DistanceAtAngle(points, T, x1)  # calculate the distance at angle x1
    x2 = (1.0 - Phi) * a + Phi * b  # calculate a new angle x2 by interpolating between a and b using the golden ratio
    f2 = DistanceAtAngle(points, T, x2)  # calculate the distance at angle x2
    while abs(b - a) > threshold:  # repeat until the difference between a and b is smaller than the threshold
        if f1 < f2:  # if the distance at angle x1 is smaller than the distance at angle x2
            b = x2  # update b to x2
            x2 = x1  # set x2 to x1
            f2 = f1  # set f2 to f1
            x1 = Phi * a + (1.0 - Phi) * b  # calculate a new angle x1 by interpolating between a and b using the golden ratio
            f1 = DistanceAtAngle(points, T, x1)  # calculate the distance at angle x1
        else:
            a = x1  # update a to x1
            x1 = x2  # set x1 to x2
            f1 = f2  # set f1 to f2
            x2 = (1.0 - Phi) * a + Phi * b  # calculate a new angle x2 by interpolating between a and b using the golden ratio
            f2 = DistanceAtAngle(points, T, x2)  # calculate the distance at angle x2
    return min(f1, f2)  # return the smaller of the two distances

def DistanceAtAngle(points, T, radians):
    """
    Calculates the distance between two sets of points after rotating one set of points by a given angle in radians.

    Args:
        points (list): List of points (x, y) to be rotated.
        T (object): Object representing the target points to compare against.
        radians (float): Angle in radians by which the points are rotated.

    Returns:
        float: The calculated distance between the rotated points and the target points.
    """
    newpoints = RotateBy(points, radians) # Rotate the points by the given angle
    return PathDistance(newpoints, T.Points) # Calculate the distance between the rotated points and target points using PathDistance function

def PathDistance(pts1, pts2):
    """
    Calculates the path distance between two sets of points.

    Args:
        pts1 (list): List of points representing one set of points.
        pts2 (list): List of points representing another set of points.

    Returns:
        float: The calculated path distance between the two sets of points.
    """
    d = 0.0
    for i in range(len(pts1)): # Loop through each point in the sets of points (assumes len(pts1) == len(pts2))
        d += Distance(pts1[i], pts2[i]) # Calculate the distance between corresponding points and add to the total distance
    return d / len(pts1) # Return the average distance by dividing the total distance by the number of points in the set pts1.


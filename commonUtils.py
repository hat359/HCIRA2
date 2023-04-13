class Point:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def display(self):
        return '({},{})'.format(int(self.X), int(self.Y))
    
    def set(self,x,y):
        self.X = x
        self.Y = y
    
    def getList(self):
        return [self.X, self.Y]

class Rectangle:
    def __init__(self, x, y, width, height):
        self.X = x
        self.Y = y
        self.Width = width
        self.Height = height

class Result:
    def __init__(self, name, score, ms):
        self.Name = name
        self.Score = score
        self.Time = ms

    def display(self):
        print("Recognized Gesture: {}, Confidence Score:{}, Time:{}".format(self.Name, self.Score, self.Time))

    def getResult(self):
        return self.Name, self.Score, self.Time
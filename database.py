import json

class Database():
    def __init__(self):
        self.filename = 'database.json'
        self.data = {}
        self.loadData()

    def loadData(self):
        with open(self.filename, 'r') as file:
            self.data = json.load(file)

    def addUser(self, userId):
        # Delete any user with userID which already exists in database
        if userId in self.data:
            del self.data[userId]
        # Add user to database
        self.data[userId] = {}

    def addGesture(self, userId, gesture, points,drawCount):
        gesture = gesture+'-'+str(drawCount)
        if gesture not in self.data[userId]:
            # print("gesture not in database and user")
            self.data[userId][gesture] = []
        for unistrokepoints in points:
            self.data[userId][gesture].append([point.getList() for point in unistrokepoints])
        self.dumpData()

    def getData(self):
        return self.data

    def clearData(self):
        with open(self.filename, 'w') as file:
            json.dump({}, file)

    def dumpData(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file)
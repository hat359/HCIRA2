import json

class Database():
    def __init__(self):
        self.filename = 'database.json'  # File name to store the database in JSON format
        self.data = {}  # Data dictionary to store the database
        self.loadData()  # Load data from the JSON file when initializing the database object

    def loadData(self):
        """
        Load data from the JSON file and update the data dictionary.
        """
        with open(self.filename, 'r') as file:
            self.data = json.load(file)

    def addUser(self, userId):
        """
        Add a user to the database with a given user ID. If the user ID already exists, delete the existing user and add
        the new user.
        """
        if userId in self.data:
            del self.data[userId]  # Delete any existing user with the same user ID
        self.data[userId] = {}  # Add the new user to the data dictionary

    def addGesture(self, userId, gesture, points, drawCount):
        """
        Add a gesture to the database for a given user ID. The gesture is associated with a list of points, which
        represent the coordinates of the gesture on the canvas, and a draw count, which indicates the number of times
        the gesture has been drawn by the user.
        """
        gesture = gesture + '-' + str(drawCount)  # Append the draw count to the gesture name to make it unique
        if gesture not in self.data[userId]:
            self.data[userId][gesture] = []  # Create a new list for the gesture if it doesn't exist in the database
        for unistrokepoints in points:
            self.data[userId][gesture].append([point.getList() for point in unistrokepoints])  # Append the list of points to the gesture data in the database
        self.dumpData()  # Save the updated data to the JSON file

    def getData(self):
        """
        Get the data dictionary containing the entire database.
        """
        return self.data

    def clearData(self):
        """
        Clear all data in the database by writing an empty dictionary to the JSON file.
        """
        with open(self.filename, 'w') as file:
            json.dump({}, file)

    def dumpData(self):
        """
        Save the updated data dictionary to the JSON file.
        """
        with open(self.filename, 'w') as file:
            json.dump(self.data, file)

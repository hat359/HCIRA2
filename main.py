from tkinter import Tk  # Import the Tkinter library for GUI
from board import Board  # Import the Board class from board.py which contains all the functions
from xmlparser import Parser  # Import the Parser class from xmlparser.py
from offline_recognizer import OfflineRecognizer  # Import the OfflineRecognizer class from offline_recognizer.py

def main():
    startOnlineRecognizer()  # Call the function to start the online recognizer
    # startOfflineRecognizer()  # Call the function to start the offline recognizer
    # self.parser = Parser()  # Initialize the Parser object

        # Load offline data
    # self.offlineData = Parser.getOfflineData()  # Call the method to get offline data from the Parser class

def startOnlineRecognizer():
    root = Tk()  # Initialize the Tkinter library
    board = Board(root, 'segmentation', 'Touch')  # Create a Board object with root window, segmentation mode, and touch input mode
    root.mainloop()  # Start the main event loop of Tkinter

def startOfflineRecognizer():
    offlineRecognizer = OfflineRecognizer()  # Create an OfflineRecognizer object

if __name__ == '__main__':
    main()  # Call the main function if the script is run as the main module

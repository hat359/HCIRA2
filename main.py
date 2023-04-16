from tkinter import Tk #tkinter library for GUI 
from board import Board #board.py contains all the functions. 
from xmlparser import Parser
from offline_recognizer import OfflineRecognizer

def main():
    # startOnlineRecognizer()
    startOfflineRecognizer()
    # self.parser = Parser()
    
        # Load offline data
    # self.offlineData = Parser.getOfflineData()

def startOnlineRecognizer():
    root = Tk() #initializig the tkinter lib. 
    board = Board(root, 'recognition','Touch') 
    root.mainloop()


def startOfflineRecognizer():
    offlineRecognizer = OfflineRecognizer()



if __name__ == '__main__':
    main()
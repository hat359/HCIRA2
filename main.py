from tkinter import Tk #tkinter library for GUI 
from board import Board #board.py contains all the functions. 
from parser import Parser

def main():
    startOnlineRecognizer()
    # startOfflineRecognizer()
    # self.parser = Parser()
    
        # Load offline data
    self.offlineData = self.parser.getOfflineData()

def startOnlineRecognizer():
    root = Tk() #initializig the tkinter lib. 
    board = Board(root, 'segmentation','Touch') 
    root.mainloop()


if __name__ == '__main__':
    main()
from BaseDisplayer import BaseDisplayer
import platform
import os

colorMap = { 0: 100,
             1: 102,
             2: 105,
             -1: 40}

cTemp = "\x1b[%dm%7s\x1b[0m "

class Displayer(BaseDisplayer):
    def __init__(self):
        if "Windows" == platform.system():
            self.display = self.winDisplay
        else:
            self.display = self.unixDisplay

    def display(self, grid):
        pass

    def winDisplay(self, grid):
        for i in range(7):
            print("------" *7)
            for j in range(7):
                print("|", end="")
                v = grid.map[int(i )][j]
                if v == -1:
                    string = "x"
                elif v == 0:
                    string = " "
                else:
                    string = str(int(v))
                print("  "+ string + "  ", end="")
            print("|")
        print("------" *7)

    def unixDisplay(self, grid):
        
        for i in range(7):
            for j in range(7):
                v = grid.map[int(i )][j]
                if v == 0:
                    string = ""
                elif v == -1:
                    string = "x".center(7, " ")
                else:
                    string = str(int(v)).center(7, " ")

                print(cTemp %  (colorMap[v], string), end="")
            print("")
            print("")
        print("")
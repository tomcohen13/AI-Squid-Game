
import tkinter as tk

class Game(tk.Frame):

    """
    """

    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title()

        self.main_grid = tk.Frame(
            self, bd = 3, width=600, height=800
        )
        self.main_grid.grid(pady=(100,0))


    def make_GUI(self):

        self.cells = []

        for i in range(7):
            row = []
            for j in range(7):
                cell_frame = tk.Frame(self.main_grid, width = 150, height = 150)
                cell_frame.grid(row = i, column = j, padx= 5, pady=5)
                cell_number = tk.Label(self.main_grid)
                cell_number.grid(row = i, column = j)
                cell_data = {"frame" : cell_frame , 
                             "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y = 45, anchor="center")
        tk.Label(
            score_frame, 
            text = "Score"
        )
                
                             





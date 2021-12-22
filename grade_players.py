import pandas as pd
import os 
import sys
import re
import glob
import pyautogui

from test_players.EasyAI import EasyAI
from test_players.MediumAI import MediumAI
from test_players.HardAI import HardAI
from Game import Game
from importlib import util
from Displayer import Displayer

ROUNDS = 10
LEVEL = "medium"

PLAYERS = {"easy": EasyAI(), "medium": MediumAI(), "hard": HardAI()}
WINS_NEEDED = {"easy": 6, "medium": 4, "hard": 2}
SCORES = {"easy": 20, "medium": 30, "hard": 34}

COLUMNS = {"easy": "2: EasyAI (20.0 pts)",
            "medium": "3: MediumAI (30.0 pts)",
            "hard": "4: HardAI (34.0 pts)"}

submissions_path = os.getcwd() + "/submissions/"


all_files = os.listdir(submissions_path)
all_files = list(filter(lambda s: re.match("^submission_[0-9]{9}$", s), all_files))

grades = pd.read_csv("grades_updated.csv")

try:
    id = sys.argv[1]
except:
    id = None

def is_hall_of_fame(game : Game):
    return len(game.grid.getAvailableCells()) < 5 or len(game.grid.getAvailableCells()) > 30

HALL_OF_FAME = []

def simulate_game(student_player, level, report = None):
    """
    """
    global PLAYERS
    opponent = PLAYERS[level] 
    score = 0.0
    
    for round in range(1, ROUNDS + 1):
        # every third round, change positions
        print(f"Round : {round}/{ROUNDS}")
        report.write(f"\nRound {round}/{ROUNDS}: ")
        if round % 3 != 0:
            game = Game(playerAI = student_player, computerAI = opponent, N = 7, displayer=Displayer())
            result = game.play()
            if result == 1:
                report.write("PlayerAI won. ")
                score += int(SCORES[level] // WINS_NEEDED[level]) + 1
                if game.dim ** 2 - len(game.grid.getAvailableCells()) <= 20:
                    report.write("Bonus 1 point for early defeat.")
                    score += 1
                if is_hall_of_fame(game):
                    HALL_OF_FAME.append((game, subid))

            else:
                report.write(f"{level.capitalize()}AI won. ")
                if len(game.grid.getAvailableCells()) <= 10:
                    report.write("Bonus 1 point for close match.")
                    score += 1
        else:
            game = Game(playerAI = opponent, computerAI = student_player, N = 7, displayer=Displayer())
            result = game.play()

            if result == 2:
                report.write("PlayerAI won. ")
                score += int(SCORES[level] // WINS_NEEDED[level]) + 1
                
                if game.dim ** 2 - len(game.grid.getAvailableCells()) <= 20:
                    report.write("Bonus 1 point for early defeat.")
                    score += 1

                if is_hall_of_fame(game):
                    HALL_OF_FAME.append((game, subid))
            
            else:
                report.write(f"{level.capitalize()}AI won. ")
                if len(game.grid.getAvailableCells()) <= 10:
                    report.write("Bonus 1 point for close match.")
                    score += 1

        if score >= SCORES[level]:
            print(f"\nTotal Score: {score}")
            report.write(f"\nTotal Score: {score}")
            return min(score, SCORES[level] + 1)

    score = min(score, SCORES[level] + 1)

    report.write(f"\nTotal Score: {score}")

    return score

for submission in all_files[100:]:
    
    subid = submission.split('_')[1]
    subpath = submissions_path + submission

    #if specific submission is specified, skip other submissions.
    if (id and subid != id): #or os.path.exists(subpath + "/report.txt"):
        continue

    print(f"Grading Submission {subid}")
    
    report = open(subpath + "/report.txt", "a") if os.path.exists(subpath + "/report.txt") else open(subpath + "/report.txt", "w+")

    try:
        # load PlayerAI from student submission
        # if not "PlayerAI.py" in os.listdir(subpath):
        file_path = glob.glob(subpath + "/**/PlayerAI.py", recursive=True)[0]
        spec = util.spec_from_file_location("PlayerAI", file_path)
        player = util.module_from_spec(spec)
        spec.loader.exec_module(player)

        score = simulate_game(player.PlayerAI(), level = LEVEL, report = report)
        print(f"Total score: {score}")
        grades.loc[grades["Submission ID"] == int(subid), COLUMNS[LEVEL]] = score
        grades.to_csv("grades_updated.csv")
    except:
        continue

for game, subid in HALL_OF_FAME:
    print(f"Submission: {subid}")
    Displayer().display(game.grid)


        
    